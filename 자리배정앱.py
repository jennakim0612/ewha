import streamlit as st
import random

st.set_page_config(page_title="🪑 반별 자리 배정 시스템", layout="wide")
st.title("🪑 반별 자리 배정 시스템")

# ----------------------------
# 1️⃣ 총 학생 수 입력 (좌석 수 = 학생 수)
# ----------------------------
st.header("총 학생 수 설정")
num_students = st.number_input("총 학생 수", min_value=1, value=10, step=1)
total_seats = num_students  # 좌석 수 = 학생 수
flat_seats = list(range(1, total_seats + 1))

st.markdown("---")

# ----------------------------
# 2️⃣ 학생 이름 및 3지망 입력
# ----------------------------
st.header("학생 이름 및 3지망 입력")

students_list = []
student_prefs = {}

for i in range(num_students):
    st.subheader(f"학생 {i+1}")
    name = st.text_input(f"학생 이름", key=f"name_{i}")
    if not name:
        name = f"학생{i+1}"
    students_list.append(name)

    col1, col2, col3 = st.columns(3)
    with col1:
        first_choice = st.selectbox("1지망", options=flat_seats, key=f"first_{i}")
    with col2:
        second_choice = st.selectbox("2지망", options=flat_seats, key=f"second_{i}")
    with col3:
        third_choice = st.selectbox("3지망", options=flat_seats, key=f"third_{i}")

    student_prefs[name] = [first_choice, second_choice, third_choice]

st.markdown("---")

# ----------------------------
# 3️⃣ 자리 배정 실행
# ----------------------------
st.header("자리 배정 실행")

if st.button("자리 배정"):
    available_seats = flat_seats.copy()
    assigned_seats = {}

    # 1~3지망 순서대로 배정
    for priority in range(3):
        seat_and_students = {}
        for student in students_list:
            if student in assigned_seats:
                continue
            if len(student_prefs[student]) > priority:
                choice = student_prefs[student][priority]
                if choice in available_seats:
                    seat_and_students.setdefault(choice, []).append(student)
        for seat, students_who_want in seat_and_students.items():
            chosen_student = random.choice(students_who_want)
            assigned_seats[chosen_student] = seat
            available_seats.remove(seat)

    # 남은 학생 랜덤 배정
    for student in students_list:
        if student not in assigned_seats:
            seat = random.choice(available_seats)
            assigned_seats[student] = seat
            available_seats.remove(seat)

    # 결과 출력
    st.subheader("배정 결과")
    for student in students_list:
        st.write(f"{student}: {assigned_seats[student]}번")
