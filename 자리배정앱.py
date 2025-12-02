import streamlit as st
import random
from typing import Dict, List

st.set_page_config(page_title="🪑 반별 자리 배정 시스템", layout="wide")
st.title("🪑 반별 자리 배정 시스템")

# ----------------------------
# 세션 상태 초기화
# ----------------------------
if "all_data" not in st.session_state:
    st.session_state.all_data = {}  # {"학년-반": [{학생, 1지망,2지망,3지망}, ...]}

# ----------------------------
# 탭 생성
# ----------------------------
tab1, tab2 = st.tabs(["학생 제출", "관리자"])

# ----------------------------
# 1️⃣ 학생 제출
# ----------------------------
with tab1:
    st.header("학생: 학년, 반, 이름, 3지망 제출")

    grade = st.number_input("학년 입력 (예: 2)", min_value=1, max_value=6, step=1)
    class_num = st.number_input("반 입력 (예: 9)", min_value=1, step=1)
    student_name = st.text_input("학생 이름 입력")

    col1, col2, col3 = st.columns(3)
    with col1:
        first_choice = st.number_input("1지망", min_value=1, value=1, step=1)
    with col2:
        second_choice = st.number_input("2지망", min_value=1, value=2, step=1)
    with col3:
        third_choice = st.number_input("3지망", min_value=1, value=3, step=1)

    if st.button("제출"):
        if grade and class_num and student_name:
            class_key = f"{grade}-{class_num:02d}"  # 예: 2-09
            if class_key not in st.session_state.all_data:
                st.session_state.all_data[class_key] = []

            # 중복 제출 방지
            names_in_class = [d["학생"] for d in st.session_state.all_data[class_key]]
            if student_name in names_in_class:
                st.warning("이미 제출하셨습니다.")
            else:
                st.session_state.all_data[class_key].append({
                    "학생": student_name,
                    "1지망": first_choice,
                    "2지망": second_choice,
                    "3지망": third_choice
                })
                st.success(f"{student_name}님의 지망이 제출되었습니다 ✅")

# ----------------------------
# 2️⃣ 관리자 페이지
# ----------------------------
with tab2:
    st.header("관리자: 제출자 확인 및 자리 배정")

    admin_grade = st.number_input("학년 입력", min_value=1, max_value=6, step=1, key="admin_grade")
    admin_class = st.number_input("반 입력", min_value=1, step=1, key="admin_class")
    class_key = f"{admin_grade}-{admin_class:02d}"

    if class_key in st.session_state.all_data:
        all_students_data = st.session_state.all_data[class_key]
        all_students = [d["학생"] for d in all_students_data]
        submitted_names = all_students
        st.subheader("제출자 명단")
        st.write(submitted_names)

        if st.button("자리 배정"):
            student_prefs: Dict[str, List[int]] = {d["학생"]: [d["1지망"], d["2지망"], d["3지망"]] for d in all_students_data}
            available_seats: List[int] = list(range(1, len(all_students) + 1))
            assigned_seats: Dict[str, int] = {}

            # 1~3지망 순서대로 배정
            for priority in range(3):
                hubo: Dict[int, List[str]] = {}
                for student in all_students:
                    if student in assigned_seats:
                        continue
                    if len(student_prefs[student]) > priority:
                        target_seat = student_prefs[student][priority]
                        if target_seat in available_seats:
                            hubo.setdefault(target_seat, []).append(student)
                for seat, hubo_stu in hubo.items():
                    chosen_student = random.choice(hubo_stu)
                    assigned_seats[chosen_student] = seat
                    available_seats.remove(seat)

            # 남은 학생 랜덤 배정
            for student in all_students:
                if student not in assigned_seats:
                    target_seat = random.choice(available_seats)
                    assigned_seats[student] = target_seat
                    available_seats.remove(target_seat)

            # 결과 출력
            st.subheader(f"{class_key} 반 배정 결과")
            for student in all_students:
                st.write(f"{student}: {assigned_seats[student]}번")
    else:
        st.info("해당 학년반 제출 데이터가 없습니다.")
