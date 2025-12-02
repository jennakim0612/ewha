import streamlit as st
import pandas as pd
import random
import os
from typing import Dict, List

st.set_page_config(page_title="🪑 3지망 자리 배정 시스템 (21009김제나)", layout="wide")
st.title("🪑 3지망 자리 배정 시스템(21009김제나)")

# ----------------------------
# 1️⃣ 학생: 지망 입력
# ----------------------------
st.header("학생용 | 학년/반, 이름, 지망 좌석 입력")

student_grade = st.number_input("학년 입력 (예: 2)", min_value=1, max_value=6, step=1)
student_class = st.number_input("반 입력 (예: 9)", min_value=1, max_value=20, step=1)
student_name = st.text_input("학생 이름 입력")

if student_grade and student_class and student_name:
    DATA_FILE = f"seat_preferences_{student_grade}_{student_class}.csv"

    st.subheader("1, 2, 3지망 좌석 입력")
    col1, col2, col3 = st.columns(3)
    with col1:
        first_choice = st.text_input("1지망")
    with col2:
        second_choice = st.text_input("2지망")
    with col3:
        third_choice = st.text_input("3지망")

    if st.button("지망 제출"):
        # CSV 불러오기 또는 새로 생성
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
        else:
            df = pd.DataFrame(columns=["학년", "반", "학생", "1지망", "2지망", "3지망"])

        # 이미 제출했으면 값 대체
        if student_name in df["학생"].values:
            df.loc[df["학생"] == student_name, ["1지망", "2지망", "3지망"]] = [first_choice, second_choice, third_choice]
            st.success(f"{student_name}님의 지망이 업데이트되었습니다")
        else:
            new_row = {
                "학년": student_grade,
                "반": student_class,
                "학생": student_name,
                "1지망": first_choice,
                "2지망": second_choice,
                "3지망": third_choice
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"{student_name}님의 지망이 저장되었습니다")

        df.to_csv(DATA_FILE, index=False)
        st.info(f"데이터는 {DATA_FILE}에 저장됩니다. 다른 학생은 볼 수 없습니다.")

st.markdown("---")

# ----------------------------
# 2️⃣ 관리자 | 제출자 확인 / 초기화 / 배정
# ----------------------------
st.header("관리자용")

admin_grade = st.number_input("배정할 학년", min_value=1, max_value=6, step=1, key="admin_grade")
admin_class = st.number_input("배정할 반", min_value=1, max_value=20, step=1, key="admin_class")
DATA_FILE_ADMIN = f"seat_preferences_{admin_grade}_{admin_class}.csv"

# 제출자 확인
if st.button("제출자 확인"):
    if os.path.exists(DATA_FILE_ADMIN):
        df_admin = pd.read_csv(DATA_FILE_ADMIN)
        st.subheader(f"{admin_grade}학년 {admin_class}반 제출자 명단")
        st.write(df_admin["학생"].tolist())
    else:
        st.warning("학생 제출 데이터가 없습니다.")

# 초기화 버튼
if st.button("학생 명단 초기화"):
    if os.path.exists(DATA_FILE_ADMIN):
        os.remove(DATA_FILE_ADMIN)
        st.success("학생 명단이 초기화 되었습니다!")
    else:
        st.info("파일이 존재하지 않습니다.")

# 자리 배정
if st.button("자리 배정 실행"):
    if os.path.exists(DATA_FILE_ADMIN):
        df_admin = pd.read_csv(DATA_FILE_ADMIN)
        all_students = df_admin["학생"].tolist()
        preferences = {row["학생"]: [row["1지망"], row["2지망"], row["3지망"]] for _, row in df_admin.iterrows()}
        available_seats = list(range(1, len(all_students) + 1))
        assigned_seats: Dict[str, int] = {}

        # 1~3지망 순서대로 배정
        for priority in range(3):
            seat_and_students: Dict[int, List[str]] = {}
            for student in all_students:
                if student in assigned_seats:
                    continue
                choice = preferences[student][priority]
                if choice not in available_seats:
                    continue
                seat_and_students.setdefault(choice, []).append(student)
            for seat, students_who_want in seat_and_students.items():
                chosen_student = random.choice(students_who_want)
                assigned_seats[chosen_student] = seat
                available_seats.remove(seat)

        # 남은 학생 랜덤 배정
        for student in all_students:
            if student not in assigned_seats:
                seat = random.choice(available_seats)
                assigned_seats[student] = seat
                available_seats.remove(seat)

        # 결과 출력
        result_df = pd.DataFrame({"학생": all_students})
        result_df["배정 좌석"] = result_df["학생"].map(assigned_seats)
        st.subheader(f"{admin_grade}학년 {admin_class}반 자리 배정 결과")
        st.dataframe(result_df)
    else:
        st.warning("학생 제출 데이터가 없습니다... 학급 전원의 지망 제출을 확인한 후 버튼을 누르세요")
