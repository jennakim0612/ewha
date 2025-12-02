with tab1:
    st.header("학생: 학년, 반, 이름, 3지망 제출")

    # 학년은 키보드로 입력
    grade = st.text_input("학년 입력 (예: 2)")
    try:
        grade_int = int(grade)
    except:
        st.warning("학년은 숫자로 입력해주세요.")
        st.stop()

    # 반은 +- 조절
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
