import streamlit as st
import random
from typing import Dict, List

st.set_page_config(page_title="🪑 반별 자리 배정 시스템", layout="wide")
st.title("🪑 반별 자리 배정 시스템")

# ----------------------------
# 세션 상태 초기화
# ----------------------------
if "all_data" not in st.session_state:
    st.session_state.all_data = {}  # 학년-반 별 학생 지망 데이터 저장

# ----------------------------
# 탭 생성
# ----------------------------
tab1, tab2 = st.tabs(["학생 제출", "관리자"])

# ----------------------------
# 1️⃣ 학생 제출 탭
# ----------------------------
with tab1:
    st.header("학생: 학년, 반, 이름, 3지망 제출")

    # 학년: 키보드 입력
    grade = st.text_input("학년 입력 (예: 2)")
    try:
        grade_int = int(grade)
    except:
        grade_int = None

    # 반: +- 조절
    class_num = st.number_input("반 입력", min_value=1, max_value=99, step=1)

    student_name = st.text_input("학생 이름 입력")

    # 좌석은 키보드 입력
    first_choice = st.text_input("1지망 좌석 입력 (숫자)", value="1")
    second_choice = st.text_input("2지망 좌석 입력 (숫자)", value="2")
    third_choice = st.text_input("3지망 좌석 입력 (숫자)", value="3")

    if st.button("제출"):
        if grade_int and class_num and student_name:
            class_key = f"{grade_int}-{class_num:02d}"  # 예: 2-09
            if class_key not in st.session_state.all_data:
                st.session_state.all_data[class_key] = []

            # 입력값 숫자로 변환
            try:
                first_choice_int = int(first_choice)
                second_choice_int = int(second_choice)
                third_choice_int = int(third_choice)
            except:
                st.warning("좌석은 숫자로 입력해주세요.")
                st.stop()

            # 기존 제출자 있으면 갱신, 없으면 새로 추가
            existing_index = next((i for i, d in enumerate(st.session_state.all_data[class_key]) if d["학생"] == student_name), None)
            new_entry = {
                "학생": student_name,
                "1지망": first_choice_int,
                "2지망": second_choice_int,
                "3지망": third_choice_int
            }
            if existing_index is not None:
                st.session_state.all_data[class_key][existing_index] = new_entry
                st.success(f"{student_name}님의 지망이 갱신되었습니다 ✅")
            else:
                st.session_state.all_data[class_key].append(new_entry)
                st.success(f"{student_name}님의 지망이 제출되었습니다 ✅")

# ----------------------------
# 2️⃣ 관리자 탭
# ----------------------------
with tab2:
    st.header("관리자: 제출자 확인 및 자리 배정")

    admin_grade = st.number_input("학년 입력", min_value=1, max_value=6, step=1)
    admin_class = st.number_input("반 입력", min_value=1, max_value=99, step=1)

    class_key = f"{admin_grade}-{admin_class:02d}"

    if class_key in st.session_state.all_data and st.session_state.all_data[class_key]:
        st.subheader("제출자 명단")
        submitted_students = [d["학생"] for d in st.session_state.all_data[class_key]]
        st.write(submitted_students)

        if st.button("자리 배정 실행"):
            all_students = submitted_students.copy()
            preferences = {d["학생"]: [d["1지망"], d["2지망"], d["3지망"]] for d in st.session_state.all_data[class_key]}

            # 좌석 수: 제출자 수만큼
            available_seats = list(range(1, len(all_students)+1))
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

            # 결과 표시
            st.subheader(f"{admin_grade}-{admin_class:02d}반 배정 결과")
            result_list = [{"학생": name, "배정석": seat} for name, seat in assigned_seats.items()]
            st.table(result_list)

    else:
        st.warning(f"{admin_grade}-{admin_class:02d}반 제출자가 없습니다.")
