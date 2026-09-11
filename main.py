"""나만의 프롬프트 관리 — 콘솔 프로그램.

메뉴 번호를 입력해 기능을 선택한다. 데이터는 프로그램 실행 중에만 유지된다.
"""

import json
import os

from data import CATEGORIES, DEFAULT_PROMPTS

DATA_FILE = "prompts.json"
EXPORT_DIR = "exports"

# 실행 중 사용하는 프롬프트 목록 (기본 데이터 복사본)
prompts = [dict(p, views=0) for p in DEFAULT_PROMPTS]

MENU = [
    ("1", "프롬프트 추가"),
    ("2", "프롬프트 목록"),
    ("3", "카테고리별 조회"),
    ("4", "프롬프트 검색"),
    ("5", "프롬프트 상세 보기"),
    ("6", "즐겨찾기 관리"),
    ("7", "즐겨찾기 목록"),
    ("8", "JSON 저장 / 불러오기"),
    ("9", "카테고리별 Markdown 내보내기"),
    ("10", "프롬프트 수정"),
    ("11", "프롬프트 삭제"),
    ("12", "조회수 TOP 목록"),
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
    prompts.append({"title": title, "content": content, "category": category, "favorite": False, "views": 0})
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
    prompt["views"] = prompt.get("views", 0) + 1
    line = "─" * 28
    print(f"\n{line}")
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '없음'}")
    print(f"조회수: {prompt['views']}")
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
    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다!")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다!")


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


def save_to_json():
    """전체 프롬프트를 JSON 파일로 저장한다. (보너스 1)"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    print(f"{len(prompts)}개의 프롬프트를 '{DATA_FILE}'에 저장했습니다.")


def load_from_json():
    """JSON 파일에서 프롬프트를 불러와 현재 목록을 교체한다. (보너스 1)"""
    if not os.path.exists(DATA_FILE):
        print(f"'{DATA_FILE}' 파일이 없습니다. 먼저 저장해주세요.")
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    prompts.clear()
    prompts.extend(loaded)
    print(f"'{DATA_FILE}'에서 {len(prompts)}개의 프롬프트를 불러왔습니다.")


def json_menu():
    """저장/불러오기 중 하나를 고른다."""
    print("\n=== JSON 저장 / 불러오기 ===")
    print("1) 저장")
    print("2) 불러오기")
    choice = input("선택: ").strip()
    if choice == "1":
        save_to_json()
    elif choice == "2":
        load_from_json()
    else:
        print("1 또는 2를 입력해주세요.")


def export_markdown():
    """카테고리별로 Markdown 파일을 만든다. (보너스 1)"""
    print("\n=== 카테고리별 Markdown 내보내기 ===")
    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return
    os.makedirs(EXPORT_DIR, exist_ok=True)
    categories = sorted({p["category"] for p in prompts})
    for category in categories:
        path = os.path.join(EXPORT_DIR, f"{category.replace('/', '_')}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {category}\n\n")
            for prompt in prompts:
                if prompt["category"] != category:
                    continue
                star = " ⭐" if prompt["favorite"] else ""
                f.write(f"## {prompt['title']}{star}\n\n```\n{prompt['content']}\n```\n\n")
        print(f"- {path}")
    print(f"\n{len(categories)}개 카테고리를 '{EXPORT_DIR}/' 폴더에 내보냈습니다.")


def edit_prompt():
    """프롬프트의 제목·내용·카테고리를 수정한다. 빈 입력은 기존 값 유지. (보너스 2)"""
    print("\n=== 프롬프트 수정 ===")
    prompt = select_prompt("수정할 프롬프트 번호")
    if prompt is None:
        return
    print("(그대로 두려면 Enter)")
    title = input(f"제목 [{prompt['title']}]: ").strip()
    content = input("내용 [기존 내용 유지]: ").strip()
    change_category = input(f"카테고리 변경? (현재 {prompt['category']}) y/N: ").strip().lower()
    if title:
        prompt["title"] = title
    if content:
        prompt["content"] = content
    if change_category == "y":
        prompt["category"] = choose_category()
    print(f"'{prompt['title']}' 프롬프트를 수정했습니다.")


def delete_prompt():
    """프롬프트를 삭제한다. 확인 후 진행. (보너스 2)"""
    print("\n=== 프롬프트 삭제 ===")
    prompt = select_prompt("삭제할 프롬프트 번호")
    if prompt is None:
        return
    confirm = input(f"'{prompt['title']}'을(를) 정말 삭제할까요? y/N: ").strip().lower()
    if confirm != "y":
        print("삭제를 취소했습니다.")
        return
    prompts.remove(prompt)
    print(f"'{prompt['title']}' 프롬프트를 삭제했습니다. (남은 {len(prompts)}개)")


def show_top():
    """조회수가 많은 순으로 상위 프롬프트를 보여준다. (보너스 2)"""
    print("\n=== 조회수 TOP 목록 ===")
    ranked = sorted(enumerate(prompts, start=1), key=lambda item: item[1].get("views", 0), reverse=True)
    ranked = [(i, p) for i, p in ranked if p.get("views", 0) > 0][:5]
    if not ranked:
        print("아직 조회한 프롬프트가 없습니다. 상세 보기를 하면 조회수가 쌓입니다.")
        return
    for rank, (index, prompt) in enumerate(ranked, start=1):
        print(f"{rank}위 (조회 {prompt['views']}회) — {format_line(index, prompt)}")


def main():
    actions = {"1": add_prompt, "2": show_list, "3": show_by_category, "4": search_prompt, "5": show_detail, "6": toggle_favorite, "7": show_favorites,
               "8": json_menu, "9": export_markdown,
               "10": edit_prompt, "11": delete_prompt, "12": show_top}
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
