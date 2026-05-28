import streamlit as st
from datetime import date

st.title("📚 수행평가 마감일 알림 앱")

# 입력 받기
subject = st.text_input("수행평가 과목 입력")

deadline = st.date_input(
    "마감일 선택",
    min_value=date.today()
)

# 버튼 클릭
if st.button("확인"):

    today = date.today()
    days_left = (deadline - today).days

    st.write(f"과목: {subject}")
    st.write(f"마감일까지 {days_left}일 남았습니다.")

    # 알림 조건
    if days_left == 7:
        st.warning("⚠️ 수행평가 마감 7일 전입니다!")

    elif days_left == 3:
        st.warning("⚠️ 수행평가 마감 3일 전입니다!")

    elif days_left == 1:
        st.error("🚨 수행평가 마감 하루 전입니다!")

    elif days_left == 0:
        st.success("✅ 오늘이 마감일입니다!")

    else:
        st.info("아직 여유가 있습니다.")
