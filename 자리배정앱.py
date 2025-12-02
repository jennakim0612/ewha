import streamlit as st
import random
from typing import Dict, List

st.set_page_config(page_title="🪑 자리 배정 시스템", layout="wide")
st.title("🪑 자리 배정 시스템")

# ----------------------------
# 1️⃣ 학생용 페이지
# ----------------------------
st.header("학생용: 학년·반·이름·희망 좌석 입력")

student_grade = st.number_input("학년 입력 (예: 2)", min_value=1, max_value=6, step=1, key="stu_grade")
student_class = st.number_input("반 입력 (예: 9)", min_value=1, max_value=99, step=1, key="stu_class")
student_name = st.text_input("학생 이름 입력", key="stu_name")

st.subheader("희망 좌석 입력 (키보드로 직접 숫자 입력)")

col1, col2, col3 = st.columns(3)
with col1:
    first_choice_str = st.text_input("1지망", key="first_choice")
with col2:
    second_choice_str = st.text_input("2지망", key="second_choice")
with col3:
    third_choice_str = st.text_input("3지망", key="third_choice")

if st.button("지망 제출"):
    if not student_name:
        st.warning("학생 이름을 입력해주세요.")
    else:
        try:
            first_choice = int(first_choice_str)
            second_choice = int(second_choice_str)
            third_choice = int(third_choice_str)
            seat_list = [first_choice, second_choice, third_choice]

            # 세션 상태에 저장
            class_key = f"{student_grade:1d}{student_class:02d}"
            if "seat_data" not in st.session_state:
                st.session_state.seat_data = {}
            if class_key not in st.session_state.seat_data:
                st.session_state.seat_data[class_key] = {}
            # 이전 제출값 덮어쓰기
            st.session_state.seat_data[class_key][student_name] = seat_list

            st.success(f"{student_name}님의 지망이 저장되었습니다 ✅")
        except ValueError:
            st.warning("각 지망은 숫자로 입력해야 합니다.")

st.markdown("---")

# ----------------------------
# 2️⃣ 관리자용 페이지
# ----------------------------
st.header("관리자용: 학년·반 입력 후 제출자 확인 및 자리 배정")

admin_grade = st.number_input("학년 입력", min_value=1, max_value=6, step=1, key="admin_grade")
admin_class = st.number_input("반 입력", min_value=1, max_value=99, step=1, key="admin_class")
class_key = f"{admin_grade:1d}{admin_class:02d}"

if st.button("제출자 확인"):
    if "seat_data" in st.session_state and class_key in st.session_state.seat_data:
        submitted_students = list(st.session_state.seat_data[class_key].keys())
        st.write(f"{admin_grade}학년 {admin_class}반 제출자 명단:")
        st.write(submitted_students)
    else:
        st.info("제출자가 없습니다.")

st.markdown("---")

# ----------------------------
# 3️⃣ 자리 배정
# ----------------------------
if st.button("자리 배정 실행"):
    if "seat_data" in st.session_state and class_key in st.session_state.seat_data:
        all_students = list(st.session_state.seat_data[class_key].keys())
        preferences = st.session_state.seat_data[class_key]

        total_seats = len(all_students)
        available_seats = list(range(1, total_seats + 1))
        assigned_seats: Dict[str, int] = {}

        # 1~3지망 순서대로 배정
        for priority in range(3):
            seat_and_students: Dict[int, List[str]] = {}
            for student in all_students:
                if student in assigned_seats:
                    continue
                if len(preferences[student]) > priority:
                    choice = preferences[student][priority]
                    if choice in available_seats:
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
        st.subheader(f"{admin_grade}학년 {admin_class}반 배정 결과")
        for student in all_students:
            st.write(f"{student}: {assigned_seats[student]}번")
    else:
        st.info("제출자가 없습니다.")
