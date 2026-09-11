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


def input_nonempty(label):
    """빈 값이면 다시 입력을 요청한다."""
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"{label}은(는) 비워둘 수 없습니다. 다시 입력해주세요.")


def choose_category():
    """카테고리 목록에서 번호로 고르거나, 직접 입력한다."""
    print("\n카테고리 선택:")
    for index, name in enumerate(CATEGORIES, start=1):
        print(f"{index}) {name}")
    print(f"{len(CATEGORIES) + 1}) 직접 입력")
    while True:
        choice = input("선택: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        if choice == str(len(CATEGORIES) + 1):
            return input_nonempty("카테고리 이름")
        print("목록에 있는 번호를 입력해주세요.")


def add_prompt():
    """새 프롬프트를 입력받아 목록에 추가한다. 즐겨찾기 기본값은 False."""
    print("\n=== 프롬프트 추가 ===")
    title = input_nonempty("제목")
    content = input_nonempty("내용")
    category = choose_category()
    prompts.append({"title": title, "content": content, "category": category, "favorite": False})
    print(f"\n'{title}' 프롬프트가 추가되었습니다! (총 {len(prompts)}개)")


def format_line(index, prompt):
    """목록 한 줄: 번호. [카테고리] 제목 ⭐"""
    star = " ⭐" if prompt["favorite"] else ""
    return f"{index}. [{prompt['category']}] {prompt['title']}{star}"


def print_list(items, empty_message="등록된 프롬프트가 없습니다."):
    """(원본 번호, 프롬프트) 목록을 출력하고 총 개수를 보여준다."""
    if not items:
        print(empty_message)
        return
    for index, prompt in items:
        print(format_line(index, prompt))
    print(f"\n총 {len(items)}개의 프롬프트")


def show_list():
    """저장된 모든 프롬프트를 번호와 함께 출력한다."""
    print("\n=== 프롬프트 목록 ===")
    print_list(list(enumerate(prompts, start=1)))


def main():
    actions = {"1": add_prompt, "2": show_list}
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
