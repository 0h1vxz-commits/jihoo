import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="수행평가 마감 알리미", page_icon="📅", layout="centered")
st.title("📅 수행평가 마감 알리미 챗봇")
st.caption("과목별 수행평가 마감일과 준비물, 팁을 꼼꼼하게 챙겨드릴게요! (Gemini 2.5 Flash-Lite 구동)")

# 2. Streamlit Secrets에서 API 키 불러오기 및 설정
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.error("🔑 Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
        st.stop()
        
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API 키를 설정하는 중 오류가 발생했습니다: {e}")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "안녕하세요! 수행평가 마감일 알리미입니다. 📝\n놓치기 쉬운 수행평가 일정이나 과제 준비물에 대해 물어보세요!"
        }
    ]

# 4. 이전 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if prompt := st.chat_input("예: '다음 주 국어 수행평가 마감일이 언제지?' 또는 새로운 일정 등록"):
    # 사용자 메시지를 화면에 표시 및 저장
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 6. Gemini 모델을 통한 답변 생성 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # 페르소나 및 지침 부여 (System Instruction)
            system_instruction = (
                "당신은 학생들의 수행평가 일정을 관리하고 안내하는 '학습 비서'입니다. "
                "사용자가 수행평가 마감일, 과제 내용, 준비물 등을 물어보면 친절하고 명확하게 안내하세요. "
                "답변할 때는 가독성을 위해 마감일과 중요 사항을 이모지와 굵은 글씨(**)를 사용해 눈에 띄게 정리해 주세요. "
                "사용자가 새로운 일정을 기억해 달라고 하면 기억하겠다고 다정하게 답변하세요."
            )
            
            # gemini-2.5-flash-lite 모델 설정
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction=system_instruction
            )
            
            # 대화 기록 형식 변환 (Gemini API 형식에 맞춤)
            formatted_history = []
            for msg in st.session_state.messages[:-1]:  # 현재 입력 직전까지의 대화
                role = "user" if msg["role"] == "user" else "model"
                formatted_history.append({"role": role, "parts": [msg["content"]]})
            
            # 이어지는 대화 시작
            chat = model.start_chat(history=formatted_history)
            
            # AI 답변 생성
            with st.spinner("답변을 생각하고 있어요..."):
                response = chat.send_message(prompt)
                full_response = response.text
                
            message_placeholder.markdown(full_response)
            
            # AI 답변을 세션 상태에 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"❌ 답변을 생성하는 중에 오류가 발생했습니다: {e}\n잠시 후 다시 시도해 주세요."
            message_placeholder.markdown(error_msg)
