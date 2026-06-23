import streamlit as st
import uuid
from typing import List, Dict

TODO_SESSION_KEY = "todo_items"


def initialize_state() -> None:
    if TODO_SESSION_KEY not in st.session_state:
        st.session_state[TODO_SESSION_KEY] = []


def add_todo_item(text: str) -> None:
    if not text:
        return
    st.session_state[TODO_SESSION_KEY].append(
        {"id": uuid.uuid4().hex, "text": text, "done": False}
    )


def delete_todo_item(index: int) -> None:
    st.session_state[TODO_SESSION_KEY].pop(index)


def update_done_state(index: int, checked: bool) -> None:
    st.session_state[TODO_SESSION_KEY][index]["done"] = checked


def get_summary(items: List[Dict[str, object]]) -> Dict[str, int]:
    completed = sum(1 for item in items if item["done"])
    total = len(items)
    return {"total": total, "completed": completed, "remaining": total - completed}


def main() -> None:
    st.set_page_config(page_title="할 일 관리", page_icon="📝")
    initialize_state()

    st.title("할 일(To-Do) 관리")
    st.write("간단한 할 일 추가, 완료, 삭제 기능을 제공합니다.")

    with st.form(key="todo_form"):
        todo_text = st.text_input("새 할 일", placeholder="할 일을 입력하세요")
        submitted = st.form_submit_button("추가")

        if submitted and todo_text:
            add_todo_item(todo_text)

    items = st.session_state[TODO_SESSION_KEY]
    summary = get_summary(items)

    st.markdown(
        f"**전체:** {summary['total']}개  |  **완료:** {summary['completed']}개  |  **미완료:** {summary['remaining']}개"
    )

    if not items:
        st.info("등록된 할 일이 없습니다. 먼저 할 일을 추가해보세요.")
        return

    for index, item in enumerate(items):
        item_id = item["id"]
        done_key = f"done_{item_id}"

        if done_key not in st.session_state:
            st.session_state[done_key] = item["done"]
        elif st.session_state[done_key] != item["done"]:
            st.session_state[done_key] = item["done"]

        cols = st.columns([0.1, 0.7, 0.1, 0.1])
        checked = cols[0].checkbox("", key=done_key)
        if checked != item["done"]:
            update_done_state(index, checked)

        cols[1].markdown(
            f"{'~~' if item['done'] else ''}{item['text']}{'~~' if item['done'] else ''}"
        )

        if cols[2].button("완료", key=f"complete_{item_id}"):
            if not item["done"]:
                update_done_state(index, True)

        if cols[3].button("삭제", key=f"delete_{item_id}"):
            delete_todo_item(index)


if __name__ == "__main__":
    main()
