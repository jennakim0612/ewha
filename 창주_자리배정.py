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

rows = st.number_input("좌석 행 수", min_value=1, value=4)
cols = st.number_input("좌석 열 수", min_value=1, value=8)

# 좌석 번호 자동 생성
seat_numbers = [[row*cols + col + 1 for col in range(cols)] for row in range(rows)]
flat_seats = [seat for row in seat_numbers for seat in row]

st.subheader("좌석 번호 예시")
st.table(seat_numbers)

st.markdown("---")

# ----------------------------
# 2️⃣ 학생 지망 입력
# ----------------------------
st.header("학생: PIN과 지망 입력")

pin = st.text_input("PIN 입력 (예: yymmdd학년반 → 2511101A)")
student_name = st.text_input("학생 이름 입력")

if pin and student_name:
    try:
        grade = pin[6]
        class_name = pin[7].upper()
        DATA_FILE = f"seat_preferences_{class_name}.csv"
    except:
        st.warning("PIN 형식이 잘못되었습니다. 예: 2511101A")
        st.stop()
    
    st.subheader("1지망, 2지망, 3지망 선택")
    col1, col2, col3 = st.columns(3)
    with col1:
        first_choice = st.selectbox("1지망", options=flat_seats, key="first")
    with col2:
        second_choice = st.selectbox("2지망", options=flat_seats, key="second")
    with col3:
        third_choice = st.selectbox("3지망", options=flat_seats, key="third")

    if st.button("지망 제출"):
        # CSV 불러오기 또는 새로 생성
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
        else:
            df = pd.DataFrame(columns=["PIN", "학생", "1지망", "2지망", "3지망"])

        # 중복 제출 방지
        if student_name in df["학생"].values:
            st.warning("이미 제출한 학생입니다.")
        else:
            new_row = {
                "PIN": pin,
                "학생": student_name,
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

selected_class = st.text_input("배정할 반 입력 (예: A)")

if st.button("자리 배정 실행"):
    DATA_FILE = f"seat_preferences_{selected_class.upper()}.csv"
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        all_students = df["학생"].tolist()
        preferences = {row["학생"]: [row["1지망"], row["2지망"], row["3지망"]] for _, row in df.iterrows()}
        available_seats = flat_seats.copy()
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

        # 결과 DataFrame 생성
        result_df = df.copy()
        result_df["배정 좌석"] = result_df["학생"].map(assigned_seats)
        st.subheader(f"{selected_class.upper()}반 자리 배정 결과")
        st.dataframe(result_df)

        # 엑셀 다운로드
        result_df.to_excel(f"assigned_seats_{selected_class.upper()}.xlsx", index=False)
        st.download_button(
            label="📥 배정 결과 엑셀 다운로드",
            data=open(f"assigned_seats_{selected_class.upper()}.xlsx", "rb").read(),
            file_name=f"assigned_seats_{selected_class.upper()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning(f"{selected_class.upper()}반 데이터가 존재하지 않습니다. 먼저 학생들의 지망을 제출받으세요.")
