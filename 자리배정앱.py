import streamlit as st
import pandas as pd
import random
import os
from typing import Dict, List

st.set_page_config(page_title="🪑 반별 자리 배정 시스템", layout="wide")
st.title("🪑 반별 자리 배정 시스템")

# ----------------------------
# 1️⃣ 학생 지망 입력
# ----------------------------
st.header("학생: 학년/반/이름과 지망 입력")

col1, col2 = st.columns(2)
with col1:
    student_grade = st.number_input("학년 입력 (예: 2)", min_value=1, max_value=6, step=1, key="grade")
with col2:
    student_class = st.number_input("반 입력 (예: 9)", min_value=1, max_value=99, step=1, key="class")

student_name = st.text_input("학생 이름 입력", key="name")

st.subheader("희망 좌석 번호 입력")
col1, col2, col3 = st.columns(3)
with col1:
    first_choice = st.text_input("1지망", key="first_choice")
with col2:
    second_choice = st.text_input("2지망", key="second_choice")
with col3:
    third_choice = st.text_input("3지망", key="third_choice")

DATA_FILE = f"seat_preferences_{student_grade:1d}{student_class:02d}.csv"

if st.button("지망 제출"):
    if not (student_name and first_choice and second_choice and third_choice):
        st.warning("모든 항목을 입력해주세요.")
    else:
        # CSV 불러오기 또는 새로 생성
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
        else:
            df = pd.DataFrame(columns=["학년", "반", "학생", "1지망", "2지망", "3지망"])

        # 중복 제출 시 덮어쓰기
        df = df[df["학생"] != student_name]
        new_row = {
            "학년": student_grade,
            "반": student_class,
            "학생": student_name,
            "1지망": int(first_choice),
            "2지망": int(second_choice),
            "3지망": int(third_choice)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"{student_name}님의 지망이 저장되었습니다!")
        st.info(f"데이터는 {DATA_FILE}에 저장됩니다.")

st.markdown("---")

# ----------------------------
# 2️⃣ 관리자용 자리 배정
# ----------------------------
st.header("관리자: 제출자 확인 및 자리 배정")

admin_grade = st.number_input("학년 입력", min_value=1, max_value=6, step=1, key="admin_grade")
admin_class = st.number_input("반 입력", min_value=1, max_value=99, step=1, key="admin_class")

DATA_FILE_ADMIN = f"seat_preferences_{admin_grade:1d}{admin_class:02d}.csv"

if os.path.exists(DATA_FILE_ADMIN)
