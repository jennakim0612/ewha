import random
from typing import Dict, List
import openpyxl

# 학생들 이름 리스트!
all_students: List[str] = [
    "강보경", "강윤지", "강지은", "구서은", "구주은", "권태영", "김가현", "김나원", "김나현", "김아인",
    "김은우", "김제나", "김주하", "김하경", "노수진", "박솔빈", "박수연", "심수민", "안효빈", "양수아",
    "원서현", "유다민", "이기쁨", "이한별", "임서연", "장현주", "정다은", "조수아", "주서하", "한지민", "홍유안"
]

def assign_seats(students: List[str]) -> Dict[str, int]: #students매개변수 받을건데, 그거 문자열리스트야. 그리고 그거 문자열, 숫자로 딕셔너리 저장.
    available_seats: List[int] = list(range(1, 32))
    student_prefs: Dict[str, List[int]] = {}

    # 학생들의 자리 지망 입력 받기
    for student in students:
        mylist = input(f"{student}의 자리 지망 (예: 13 2 33): ").strip().split() #strip은 공백제거, split은 공백 기준으로 나눠 리스트 변환
        if not mylist:
            mylist = []
        mylist = list(map(int, mylist)) #split->문자열 이므로 정수로 변환.
        student_prefs[student] = mylist

    assigned_seats: Dict[str, int] = {}

    # 3지망 순위대로 자리 배정
    for priority in range(3): #0 → 1지망, 1 → 2지망, 2 → 3지망
        hubo: Dict[int, List[str]] = {} #자리경쟁 딕셔너리

        for student in students:
            if student in assigned_seats:
                continue

            if len(student_prefs[student]) > priority: #이거 발상 쩐다....
                target_seat = student_prefs[student][priority]
                if target_seat in available_seats:
                    if target_seat not in hubo:
                        hubo[target_seat] = [] #독차지한 애들 빈 리스트 추가
                    hubo[target_seat].append(student)

        # 같은 자리 중에 무작위로 학생 선택
        for seat, hubo_stu in hubo.items():
            chosen_student = random.choice(hubo_stu)
            assigned_seats[chosen_student] = seat
            available_seats.remove(seat)

    # 남은 학생들에게 무작위로 자리 배정
    for student in students:
        if student not in assigned_seats:
            assigned_seats[student] = random.choice(available_seats)
            available_seats.remove(assigned_seats[student])

    return assigned_seats

def update_excel_with_seating_chart(assigned_seats: Dict[str, int], input_filename: str, output_filename: str):
    wb = openpyxl.load_workbook(input_filename)
    ws = wb.active

    # 각 셀을 순회하며 자리 번호에 해당하는 셀에 학생 이름 입력
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, int):  # 셀에 번호가 있을 때
                seat_num = cell.value
                if seat_num in assigned_seats.values():
                    student_name = next(name for name, seat in assigned_seats.items() if seat == seat_num)
                    cell.value = student_name

    # 엑셀 파일을 새 파일로 저장
    wb.save(output_filename)
    print(f"Seating chart updated in {output_filename}")

# 자리 배정 함수 호출
assigned_seats = assign_seats(all_students)

# 자리 배정 결과를 새 엑셀 파일에 업데이트
update_excel_with_seating_chart(assigned_seats, "seating_chart.xlsx", "updated_seating_chart.xlsx")

# 결과 출력
for student in all_students:
    print(f"{student}의 배정석: {assigned_seats[student]}번")