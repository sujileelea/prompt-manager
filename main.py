"""나만의 프롬프트 관리 — 콘솔 프로그램.

메뉴 번호를 입력해 기능을 선택한다. 데이터는 프로그램 실행 중에만 유지된다.
"""

from data import CATEGORIES, DEFAULT_PROMPTS

# 실행 중 사용하는 프롬프트 목록 (기본 데이터 복사본)
prompts = [dict(p) for p in DEFAULT_PROMPTS]

MENU = [
    ("1", "프롬프트 추가"),
    ("2", "프롬프트 목록"),
    ("3", "카테고리별 조회"),
    ("4", "프롬프트 검색"),
    ("5", "프롬프트 상세 보기"),
    ("6", "즐겨찾기 관리"),
    ("7", "즐겨찾기 목록"),
    ("0", "종료"),
]


def show_menu():
    """메뉴를 출력하고 사용자의 선택을 돌려준다."""
    print("\n=== 나만의 프롬프트 관리 ===")
    for number, name in MENU:
        print(f"{number}. {name}")
    return input("선택: ").strip()


def not_ready():
    print("아직 준비 중인 기능입니다.")


def main():
    actions = {}
    while True:
        choice = show_menu()
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        action = actions.get(choice)
        if action is None:
            print("잘못된 번호입니다. 메뉴에 있는 번호를 입력해주세요.")
            continue
        action()


if __name__ == "__main__":
    main()
