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


def show_by_category():
    """카테고리를 고르면 그 카테고리의 프롬프트만 출력한다."""
    print("\n=== 카테고리별 조회 ===")
    # 기본 카테고리 + 직접 입력으로 추가된 카테고리를 함께 보여준다
    names = list(CATEGORIES) + sorted({p["category"] for p in prompts} - set(CATEGORIES))
    for index, name in enumerate(names, start=1):
        print(f"{index}) {name}")
    choice = input("선택: ").strip()
    if not (choice.isdigit() and 1 <= int(choice) <= len(names)):
        print("목록에 있는 번호를 입력해주세요.")
        return
    category = names[int(choice) - 1]
    items = [(i, p) for i, p in enumerate(prompts, start=1) if p["category"] == category]
    print(f"\n[{category}] 카테고리 프롬프트:")
    print_list(items, f"[{category}] 카테고리에 등록된 프롬프트가 없습니다.")


def search_prompt():
    """키워드가 제목 또는 내용에 포함된 프롬프트를 검색한다."""
    print("\n=== 프롬프트 검색 ===")
    keyword = input_nonempty("검색어")
    lowered = keyword.lower()
    items = [
        (i, p) for i, p in enumerate(prompts, start=1)
        if lowered in p["title"].lower() or lowered in p["content"].lower()
    ]
    print("\n검색 결과:")
    if not items:
        print(f"'{keyword}'을(를) 포함한 프롬프트가 없습니다.")
        return
    for index, prompt in items:
        print(format_line(index, prompt))
    print(f"\n{len(items)}개의 프롬프트를 찾았습니다.")


def select_prompt(label="번호 입력"):
    """번호를 입력받아 해당 프롬프트를 돌려준다. 잘못된 번호면 None."""
    choice = input(f"{label}: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(prompts):
        return prompts[int(choice) - 1]
    print(f"잘못된 번호입니다. 1~{len(prompts)} 사이의 번호를 입력해주세요.")
    return None


def show_detail():
    """프롬프트 번호를 입력하면 전체 내용을 출력한다."""
    print("\n=== 프롬프트 상세 보기 ===")
    prompt = select_prompt()
    if prompt is None:
        return
    line = "─" * 28
    print(f"\n{line}")
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '없음'}")
    print(line)
    print("내용:")
    print(prompt["content"])
    print(line)


def toggle_favorite():
    """프롬프트 번호를 입력해 즐겨찾기를 추가하거나 해제한다."""
    print("\n=== 즐겨찾기 관리 ===")
    prompt = select_prompt("프롬프트 번호 입력")
    if prompt is None:
        return
    prompt["favorite"] = not prompt["favorite"]
    state = "추가했습니다" if prompt["favorite"] else "해제했습니다"
    print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 {state}!" if not prompt["favorite"]
          else f"'{prompt['title']}' 프롬프트를 즐겨찾기에 {state}!")


def show_favorites():
    """즐겨찾기된 프롬프트만 모아서 출력한다."""
    print("\n=== 즐겨찾기 목록 ===")
    items = [(i, p) for i, p in enumerate(prompts, start=1) if p["favorite"]]
    if not items:
        print("즐겨찾기한 프롬프트가 없습니다.")
        return
    for index, prompt in items:
        print(format_line(index, prompt))
    print(f"\n총 {len(items)}개의 즐겨찾기")


def main():
    actions = {"1": add_prompt, "2": show_list, "3": show_by_category, "4": search_prompt, "5": show_detail, "6": toggle_favorite, "7": show_favorites}
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
