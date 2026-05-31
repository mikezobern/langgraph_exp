"""Editorial (model solution) — Problem 0004: Calculator (Nested Routing).

This is a reference answer. Try to solve `solution.py` on your own first;
peek here only when you're stuck or to compare after passing the tests.

Key idea
--------
No new objects — two ideas about arranging the familiar ones:

  1. You can call add_conditional_edges more than once, at different sources, to get
     multi-stage routing (here: route on the operator, then route on b == 0).
  2. A node may return {} (change nothing). "check_div" is a pure routing hub: its only
     job is to be the source of the second branch.

                ┌── add ───────────────┐
                ├── sub ───────────────┤
    START ─(op?)┤                       ├──> END
                ├── mul ───────────────┤
                └── check_div ─(b==0?)──┤
                        zero → div_error
                        ok   → div_ok
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    a: int
    b: int
    op: str
    result: int
    message: str


def build_graph():
    def add(state: State) -> dict:
        r = state["a"] + state["b"]
        return {"result": r, "message": f"{state['a']} + {state['b']} = {r}"}

    def sub(state: State) -> dict:
        r = state["a"] - state["b"]
        return {"result": r, "message": f"{state['a']} - {state['b']} = {r}"}

    def mul(state: State) -> dict:
        r = state["a"] * state["b"]
        return {"result": r, "message": f"{state['a']} * {state['b']} = {r}"}

    def check_div(state: State) -> dict:
        # Pure routing hub: change nothing, just exist as a branch source.
        return {}

    def div_ok(state: State) -> dict:
        r = state["a"] // state["b"]
        return {"result": r, "message": f"{state['a']} / {state['b']} = {r}"}

    def div_error(state: State) -> dict:
        return {"result": 0, "message": "division by zero"}

    def op_router(state: State) -> str:
        return {"+": "add", "-": "sub", "*": "mul", "/": "check_div"}[state["op"]]

    def zero_router(state: State) -> str:
        return "zero" if state["b"] == 0 else "ok"

    builder = StateGraph(State)
    for name, fn in [
        ("add", add), ("sub", sub), ("mul", mul),
        ("check_div", check_div), ("div_ok", div_ok), ("div_error", div_error),
    ]:
        builder.add_node(name, fn)

    builder.add_conditional_edges(
        START,
        op_router,
        {"add": "add", "sub": "sub", "mul": "mul", "check_div": "check_div"},
    )
    builder.add_conditional_edges(
        "check_div",
        zero_router,
        {"zero": "div_error", "ok": "div_ok"},
    )
    for name in ("add", "sub", "mul", "div_ok", "div_error"):
        builder.add_edge(name, END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    for c in (
        {"a": 4, "b": 5, "op": "+"},
        {"a": 9, "b": 4, "op": "-"},
        {"a": 6, "b": 7, "op": "*"},
        {"a": 10, "b": 3, "op": "/"},
        {"a": 10, "b": 0, "op": "/"},
    ):
        print(c, "->", graph.invoke(c)["message"])
