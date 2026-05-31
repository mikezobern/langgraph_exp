"""Editorial (model solution) — Problem 0003: Grade Pipeline (Consolidation).

This is a reference answer. Try to solve `solution.py` on your own first;
peek here only when you're stuck or to compare after passing the tests.

Key idea
--------
No new objects — just two arrangements of familiar ones:

  1. Conditional edges can start from a *node* (here "clamp"), not only from START.
  2. Several branches can converge into one node ("finalize") via plain add_edge.

Each piece has a single responsibility:
  - "clamp"     : normalizes the input
  - router      : decides the route (returns a label, never mutates state)
  - grade_*     : sets the grade
  - "finalize"  : composes the final message

    START → clamp ─(router)─┬── grade_a ────┐
                            ├── grade_pass ──┤→ finalize → END
                            └── grade_fail ──┘
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    score: int
    normalized: int
    grade: str
    message: str


def build_graph():
    def clamp(state: State) -> dict:
        return {"normalized": max(0, min(100, state["score"]))}

    def router(state: State) -> str:
        n = state["normalized"]
        if n >= 90:
            return "a"
        if n >= 60:
            return "pass"
        return "fail"

    def grade_a(state: State) -> dict:
        return {"grade": "A"}

    def grade_pass(state: State) -> dict:
        return {"grade": "Pass"}

    def grade_fail(state: State) -> dict:
        return {"grade": "Fail"}

    def finalize(state: State) -> dict:
        return {"message": f"{state['normalized']}: {state['grade']}"}

    builder = StateGraph(State)
    builder.add_node("clamp", clamp)
    builder.add_node("grade_a", grade_a)
    builder.add_node("grade_pass", grade_pass)
    builder.add_node("grade_fail", grade_fail)
    builder.add_node("finalize", finalize)

    builder.add_edge(START, "clamp")
    builder.add_conditional_edges(
        "clamp",
        router,
        {"a": "grade_a", "pass": "grade_pass", "fail": "grade_fail"},
    )
    builder.add_edge("grade_a", "finalize")
    builder.add_edge("grade_pass", "finalize")
    builder.add_edge("grade_fail", "finalize")
    builder.add_edge("finalize", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    for score in (95, 60, 59, 150, -5):
        print(score, "->", graph.invoke({"score": score})["message"])
