from datetime import datetime

# --- 좌석 타입 맵 (D: 장애인, E: 전기차, N: 일반) ---
seat_types = [
    # A행: 0~2는 장애인, 5~7은 전기차
    ['D','D','D','N','N','E','E','E','N','N'],
    # B행
    ['N','N','N','N','N','N','N','N','N','N'],
    # C행
    ['N','N','N','N','N','N','N','N','N','N'],
    # D행
    ['N','N','N','N','N','N','N','N','N','N']
]

# --- 아이콘 매핑 (빈자리일 때 표시) ---
EMPTY_ICON = {'D': '♿', 'E': '🔋', 'N': '⬜'}
OCC_ICON = '⬛'

# --- 현재 좌석 표시 상태(아이콘) 초기화 ---
seats = [[EMPTY_ICON[t] for t in row] for row in seat_types]

# --- 점유 테이블 (번호판 → 위치/입차시간) ---
occupied = {}


# --- 정기 회원 (번호판 → 이름/할인율 %) ---
members = {
    '11가1234': {'name': '정지아1',  'discount': 80},
    '22나2345': {'name': '정지아2', 'discount': 50},
    '33나3456': {'name': '정지아3',  'discount': 0},
}

    
# ===== 유틸 함수 =====

def row_char_to_index(ch: str) -> int:
    """A/B/C/D → 0/1/2/3"""
    return ord(ch.upper()) - ord('A')


def parse_position(text: str):
    """'A10' → (row_idx, col_idx). 실패 시 (None, None)"""
    text = text.strip()
    if len(text) < 2:
        return None, None
    row_ch = text[0]
    if not row_ch.isalpha():
        return None, None
    row = row_char_to_index(row_ch)
    try:
        col = int(text[1:]) - 1  # 1-based → 0-based
    except ValueError:
        return None, None
    if not (0 <= row < len(seats) and 0 <= col < len(seats[0])):
        return None, None
    return row, col


def pos_to_label(r: int, c: int) -> str:
    return f"{chr(r + 65)}{c + 1}"


def show_seats():
    print("[좌석 현황] (A~D 행, 1~10 열)")
    print("설명: ⬜ 일반 빈자리  ⬛ 점유중  ♿ 장애인 전용  🔋 전기차 전용")
    header = "    " + " ".join(f"{i:>2}" for i in range(1, 11))
    print(header)
    for r, row in enumerate(seats):
        line = f"{chr(65+r)} | " + " ".join(f"{cell:>2}" for cell in row)
        print(line)
    print()


def is_eligible(row: int, col: int, kind: str) -> bool:
    """
    좌석 타입 대비 자격 확인.
    kind: 'd'(장애인), 'e'(전기차), 'n'(일반)
    """
    t = seat_types[row][col]
    if t == 'D':
        return kind == 'd'
    if t == 'E':
        return kind == 'e'
    return True  # 일반석은 누구나 가능


def recommend_positions(kind: str, limit: int = 3):
    """왼쪽 상단부터 훑으며 빈자리 + 자격 충족 좌석 최대 3개 추천"""
    rec = []
    for r in range(len(seats)):
        for c in range(len(seats[r])):
            if seats[r][c] != OCC_ICON and is_eligible(r, c, kind):
                rec.append(pos_to_label(r, c))
                if len(rec) >= limit:
                    return rec
    return rec


def occupy(row: int, col: int, car_num: str, entrance_str: str):
    seats[row][col] = OCC_ICON
    occupied[car_num] = {'position': pos_to_label(row, col), 'entrance': entrance_str}


def free_seat(row: int, col: int):
    t = seat_types[row][col]
    seats[row][col] = EMPTY_ICON[t]


def calc_fee(in_str: str, out_str: str, discount_pct: int) -> int:
    """30분당 3,000원, 0~29분 무료. 할인 % 적용."""
    in_dt = datetime.strptime(in_str, "%Y-%m-%d %H:%M")
    out_dt = datetime.strptime(out_str, "%Y-%m-%d %H:%M")
    diff = out_dt - in_dt
    total_30mins = int(diff.total_seconds() // 1800)
    base = total_30mins * 3000
    final = int(base * (1 - discount_pct / 100))
    return final


# ===== 기능: 입차 =====

def do_checkin():
    show_seats()
    desire_pos = input("원하는 자리 입력 (예: A5): ").strip()
    r, c = parse_position(desire_pos)
    if r is None:
        print("자리 입력 형식이 올바르지 않습니다.")
        return

    kind = input("차량 유형 선택 (d: 장애인, e: 전기차, n: 일반): ").strip().lower()
    if kind not in ('d', 'e', 'n'):
        print("잘못된 입력입니다. d/e/n 중에서 선택하세요.")
        return

    if not is_eligible(r, c, kind):
        print("해당 전용 좌석을 사용할 자격이 없습니다.")
        rec = recommend_positions(kind)
        print(f"추천 좌석: {rec if rec else '없음'}")
        return

    if seats[r][c] == OCC_ICON:
        print("선택한 자리는 이미 사용 중입니다.")
        rec = recommend_positions(kind)
        print(f"추천 좌석: {rec if rec else '없음'}")
        return

    car_num = input("차량 번호 입력 (예: 12다1234): ").strip()
    in_time = input("입차 시간 입력 (YYYY-MM-DD HH:MM): ").strip()
    try:
        datetime.strptime(in_time, "%Y-%m-%d %H:%M")
    except ValueError:
        print("입차 시간 형식이 올바르지 않습니다.")
        return

    occupy(r, c, car_num, in_time)
    print("자리 선택이 완료되었습니다.")
    show_seats()


# ===== 기능: 출차 =====

def do_checkout():
    car_num = input("차량 번호 입력 (예: 12다1234): ").strip()
    if car_num not in occupied:
        print("등록된 주차 기록이 없습니다.")
        return

    print("주차 기록:", occupied[car_num])

    out_time = input("출차 시간 입력 (YYYY-MM-DD HH:MM): ").strip()
    try:
        datetime.strptime(out_time, "%Y-%m-%d %H:%M")
    except ValueError:
        print("출차 시간 형식이 올바르지 않습니다.")
        return

    discount = members.get(car_num, {}).get('discount', 0)
    in_time = occupied[car_num]['entrance']
    price = calc_fee(in_time, out_time, discount)
    print(f"총 요금: {int(price):,}원")

    out_position = occupied[car_num]['position']
    r, c = parse_position(out_position)
    if r is not None:
        free_seat(r, c)
    del occupied[car_num]

    show_seats()


# ===== 메인 루프 =====

def main():
    while True:
        print("===== 주차 시스템 =====")
        print("1: 입차")
        print("2: 출차")
        print("0: 종료")
        print("======================")
        choice = input("메뉴를 선택하세요: ").strip()

        if choice == '0':
            print("이용해 주셔서 감사합니다!")
            break
        elif choice == '1':
            do_checkin()
        elif choice == '2':
            do_checkout()
        else:
            print("잘못된 메뉴입니다. 다시 시도하세요.")


if __name__ == '__main__':
    main()
