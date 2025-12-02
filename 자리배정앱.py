import streamlit as st
import random
from typing import Dict, List

st.set_page_config(page_title="🪑 반별 자리 배정 시스템", layout="wide")
st.title("🪑 반별 자리 배정 시스템")

# ----------------------------
# 1️⃣ 학생용 페이지
# ----------------------------
st.header("학생 페이지: 학년, 반, 이름, 희망 좌석 입력")

with st.form("student_form"):
    student_grade = st.number_input("학년 입력", min_value=1, max_value=3, step=1, key="student_grade")
    student_class = st.number_input("반 입력", min_value=1, max_value=99, step=1, key="student_class")
    student_name = st.text_input("학생 이름 입력", key="student_name")
    first_choice = st.number_input("1지망 좌석 번호 입력", min_value=1, step=1, key="first_choice")
    second_choice = st.number_input("2지망 좌석 번호 입력", min_value=1, step=1, key="second_choice")
    third_choice = st.number_input("3지망 좌석 번호 입력", min_value=1, step=1, key="third_choice")
    
    submitted = st.form_submit_button("지망 제출")

    if submitted:
        class_key = f"{student_grade:1d}{student_class:02d}"
        if "seat_data" not in st.session_state:
            st.session_state.seat_data = {}
        if class_key not in st.session_state.seat_data:
            st.session_state.seat_data[class_key] = {}
        
        # 이전 제출한 학생은 덮어쓰기
        st.session_state.seat_data[class_key][student_name] = [
            first_choice, second_choice, third_choice
        ]
        st.success(f"{student_name}님의 지망이 저장되었습니다 ✅")

st.markdown("---")

# ----------------------------
# 2️⃣ 관리자용 페이지
# ----------------------------
st.header("관리자 페이지: 제출자 확인 및 자리 배정")

with st.form("admin_form"):
    admin_grade = st.number_input("학년 입력", min_value=1, max_value=3, step=1, key="admin_grade")
    admin_class = st.number_input("반 입력", min_value=1, max_value=99, step=1, key="admin_class")
    total_seats = st.number_input("총 좌석 수 입력", min_value=1, step=1, key="total_seats")
    
    assign_button = st.form_submit_button("자리 배정 실행")

if assign_button:
    class_key = f"{admin_grade:1d}{admin_class:02d}"
    if "seat_data" not in st.session_state or class_key not in st.session_state.seat_data:
        st.warning("해당 반의 제출 데이터가 없습니다. 학생들이 지망을 제출했는지 확인하세요.")
    else:
        preferences = st.session_state.seat_data[class_key]
        all_students = list(preferences.keys())
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

        # 제출자 이름 표시
        st.subheader(f"{admin_grade}학년 {admin_class:02d}반 제출자 명단")
        st.write(all_students)

        # 배정 결과 출력
        st.subheader("배정 결과")
        for student in all_students:
            st.write(f"{student}: {assigned_seats[student]}번")
