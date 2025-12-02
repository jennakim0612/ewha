import streamlit as st
import random
from typing import Dict, List

# -----------------------------
# 자리 배정 함수
# -----------------------------
def assign_seats(students: List[str], student_prefs: Dict[str, List[int]], total_seats: int) -> Dict[str, int]:
    available_seats: List[int] = list(range(1, total_seats + 1))
    assigned_seats: Dict[str, int] = {}

    for priority in range(3):
        hubo: Dict[int, List[str]] = {}

        for student in students:
            if student in assigned_seats:
                continue
            if len(student_prefs[student]) > priority:
                target_seat = student_prefs[student][priority]
                if target_seat in available_seats:
                    if target_seat not in hubo:
                        hubo[target_seat] = []
                    hubo[target_seat].append(student)

        for seat, hubo_stu in hubo.items():
            chosen_student = random.choice(hubo_stu)
            assigned_seats[chosen_student] = seat
            available_seats.remove(seat)

    # 남은 학생에게 무작위 배정
    for student in students:
        if student not in assigned_seats:
            chosen_seat = random.choice(available_seats)
            assigned_seats[student] = chosen_seat
            available_seats.remove(chosen_seat)

    return assigned_seats

# -----------------------------
# Streamlit 앱
# -----------------------------
st.title("학생 자리 배정 시스템")

# 좌석 수 입력
total_seats = st.number_input("총 좌석 수 입력", min_value=1, value=37, step=1)

# 탭 생성
tab1, tab2 = st.tabs(["학생 입력", "관리자"])

with tab1:
    st.header("학생 이름 및 3지망 입력")

    # 학생 입력
    student_prefs: Dict[str, List[int]] = {}
    students_list: List[str] = []

    # 학생 수 입력
    num_students = st.number_input("학생 수 입력", min_value=1, value=10, step=1)

    for i in range(num_students):
        st.subheader(f"학생 {i+1}")
        name = st.text_input(f"학생 이름", key=f"name_{i}")
        students_list.append(name if name else f"학생{i+1}")
        # 3지망 입력
        prefs = st.text_input(f"{name}의 자리 지망 (예: 1 2 3)", key=f"prefs_{i}")
        if prefs:
            prefs_list = [int(x) for x in prefs.strip().split() if x.isdigit()]
            student_prefs[students_list[-1]] = prefs_list
        else:
            student_prefs[students_list[-1]] = []

    # 제출자 명단 표시 (지망은 비공개)
    st.subheader("제출자 명단")
    submitted_students = [s for s, prefs in student_prefs.items() if prefs]
    st.write(submitted_students)

with tab2:
    st.header("관리자용 자리 배정")
    if st.button("자리 배정"):
        assigned_seats = assign_seats(students_list, student_prefs, total_seats)
        st.success("자리 배정 완료!")

        # 결과 출력
        st.subheader("배정 결과")
        for student in students_list:
            st.write(f"{student}: {assigned_seats[student]}번")
