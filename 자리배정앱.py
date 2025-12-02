import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="🪑 반별 자리 배정 시스템", layout="wide")
st.title("🪑 반별 자리 배정 시스템")

# ----------------------------
# 1️⃣ 학생용: 학년/반, 이름, 지망 제출
# ----------------------------
st.header("학생: 학년/반, 이름, 지망 좌석 제출")

grade = st.number_input("학년 입력", min_value=1, max_value=3, value=1, step=1)
class_num = st.number_input("반 입력", min_value=1, max_value=20, value=1, step=1)
student_name = st.text_input("학생 이름 입력")

if student_name:
    st.subheader("1지망, 2지망, 3지망 입력 (좌석 번호)")
    col1, col2, col3 = st.columns(3)
    with col1:
        first_choice = st.text_input("1지망", key="first_choice")
    with col2:
        second_choice = st.text_input("2지망", key="second_choice")
    with col3:
        third_choice = st.text_input("3지망", key="third_choice")

    if st.button("지망 제출"):
        DATA_FILE = f"seat_preferences_{grade}_{class_num:02}.csv"

        # CSV 불러오기 또는 새로 생성
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
        else:
            df = pd.DataFrame(columns=["학년", "반", "학생", "1지망", "2지망", "3지망"])

        # 중복 제출 처리: 이름이 이미 있으면 덮어쓰기
        if student_name in df["학생"].values:
            df.loc[df["학생"] == student_name, ["1지망", "2지망", "3지망"]] = [first_choice, second_choice, third_choice]
            st.success(f"{student_name}님의 지망이 업데이트 되었습니다 ✅")
        else:
            new_row = {
                "학년": grade,
                "반": class_num,
                "학생": student_name,
                "1지망": first_choice,
                "2지망": second_choice,
                "3지망": third_choice
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"{student_name}님의 지망이 저장되었습니다 ✅")

        df.to_csv(DATA_FILE, index=False)
        st.info(f"데이터는 {DATA_FILE}에 저장됩니다. 다른 학생들은 볼 수 없습니다.")

st.markdown("---")

# ----------------------------
# 2️⃣ 관리자용: 제출자 확인 및 자리 배정
# ----------------------------
st.header("관리자: 제출자 확인 및 자리 배정")

admin_grade = st.number_input("학년 선택", min_value=1, max_value=3, value=1, step=1, key="admin_grade")
admin_class = st.number_input("반 선택", min_value=1, max_value=20, value=1, step=1, key="admin_class")

DATA_FILE_ADMIN = f"seat_preferences_{admin_grade}_{admin_class:02}.csv"

if os.path.exists(DATA_FILE_ADMIN):
    df_admin = pd.read_csv(DATA_FILE_ADMIN)
    st.subheader(f"{admin_grade}학년 {admin_class:02}반 제출자 명단")
    st.dataframe(df_admin[["학생"]])  # 지망 좌석은 비공개

    if st.button("자리 배정 실행"):
        all_students = df_admin["학생"].tolist()
        # 지망을 정수 리스트로 변환
        preferences = {
            row["학생"]: [int(row["1지망"]), int(row["2지망"]), int(row["3지망"])]
            for _, row in df_admin.iterrows()
        }

        # 전체 좌석 수 = 학생 수
        total_seats = list(range(1, len(all_students) + 1))
        available_seats = total_seats.copy()
        assigned_seats = {}

        # 1~3지망 순서대로 배정
        for priority in range(3):
            seat_and_students = {}
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
        result_df = pd.DataFrame({"학생": all_students, "배정 좌석": [assigned_seats[s] for s in all_students]})
        st.subheader(f"{admin_grade}학년 {admin_class:02}반 배정 결과")
        st.dataframe(result_df)

else:
    st.warning("해당 학년/반의 제출자 데이터가 없습니다. 학생들이 먼저 지망을 제출해야 합니다.")
