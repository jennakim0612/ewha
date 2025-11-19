import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="🪑 반별 자리 배정 시스템", layout="wide")
st.title("🪑 반별 자리 배정 시스템")

# ----------------------------
# 1️⃣ 좌석 설정 (교사용)
# ----------------------------
st.header("관리자: 좌석 행×열 설정")

rows = st.number_input("좌석 행 수", min_value=1, value=6)
cols = st.number_input("좌석 열 수", min_value=1, value=6)

# 좌석 번호 자동 생성
seat_numbers = [[row*cols + col + 1 for col in range(cols)] for row in range(rows)]
flat_seats = [seat for row in seat_numbers for seat in row]

st.subheader("좌석 번호 예시")
st.table(seat_numbers)

# 미사용 좌석 선택
unused_seats = st.multiselect(
    "사용하지 않을 좌석 선택 (비워둘 좌석)",
    options=flat_seats
)
available_seats = [seat for seat in flat_seats if seat not in unused_seats]


st.markdown("---")

# ----------------------------
# 2️⃣ 학생 지망 입력
# ----------------------------
st.header("학생: 정보 및 지망 입력")

date_input = st.text_input("날짜 입력 (yymmdd)")
student_name = st.text_input("이름 입력")
student_id = st.text_input("학번 입력 (5자리)")

if date_input and student_name and student_id:
    st.subheader("1지망, 2지망, 3지망 선택")
    col1, col2, col3 = st.columns(3)
    with col1:
        first_choice = st.selectbox("1지망", options=available_seats, key="first")
    with col2:
        second_choice = st.selectbox("2지망", options=available_seats, key="second")
    with col3:
        third_choice = st.selectbox("3지망", options=available_seats, key="third")

    if st.button("지망 제출"):
        #CSV 파일 이름: 날짜 + 학번 앞2자리 그룹
        group_key = f"{date_input}{student_id[:2]}"
        DATA_FILE = f"seat_preferences_{group_key}.csv"

        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
        else:
            df = pd.DataFrame(columns=["날짜", "학번", "학생 이름", "1지망", "2지망", "3지망"])

        if student_name in df["학생 이름"].values:
            st.warning("이미 제출한 학생입니다.")
        else:
            new_row = {
                "날짜": date_input,
                "학번": student_id,
                "학생 이름": student_name,
                "1지망": first_choice,
                "2지망": second_choice,
                "3지망": third_choice
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"{student_name}님의 지망이 저장되었습니다 ✅")
            st.info(f"데이터는 {DATA_FILE}에 저장됩니다. 다른 학생들은 볼 수 없습니다.")

st.markdown("---")

# ----------------------------
# 3️⃣ 자리 배정 (교사용)
# ----------------------------
st.header("관리자: 자리 배정 실행")

selected_group = st.text_input("배정할 그룹 입력 (날짜+학번 앞2자리, 예: 25112121)")

if st.button("자리 배정 실행"):
    DATA_FILE = f"seat_preferences_{selected_group}.csv"
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        all_students = df["학생 이름"].tolist()
        preferences = {row["학생 이름"]: [row["1지망"], row["2지망"], row["3지망"]] for _, row in df.iterrows()}
        seats_copy = available_seats.copy()
        assigned_seats = {}

        if len(all_students) > len(seats_copy):
            st.warning("학생 수가 좌석 수보다 많습니다! 일부 학생은 배정되지 않을 수 있습니다.")


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

        # 결과 DataFrame 생성
        result_df = df.copy()
        result_df["배정 좌석"] = result_df["학생"].map(assigned_seats)
         st.subheader(f"{selected_group} 그룹 자리 배정 결과")
        st.dataframe(result_df)

         # 제출자 이름 확인
        st.subheader("제출자 명단")
        st.write(all_students)

    else:
        st.warning(f"{selected_group} 그룹 데이터가 존재하지 않습니다. 먼저 학생들의 지망을 제출받으세요.")
