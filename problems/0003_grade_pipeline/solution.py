"""Problem 0003 — Grade Pipeline (Consolidation).

Read the task in this folder's README.md, then implement `build_graph()` below.
Run the tests with:  pytest problems/0003_grade_pipeline -v
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    score: int
    normalized: int
    grade: str
    message: str


def build_graph():
    """Build and return a COMPILED graph: score -> grade -> message.

    Pipeline (see README.md for details):
      START -> "clamp" -> (router) -> "grade_a" | "grade_pass" | "grade_fail" -> "finalize" -> END

    Node names must be exactly:
      "clamp", "grade_a", "grade_pass", "grade_fail", "finalize"

    Return the object produced by `.compile()`.
    """
    # TODO: implement me.
    #
    # 1) "clamp" node: normalized = max(0, min(100, score)); return {"normalized": ...}
    # 2) router(state) -> str: decide by state["normalized"] which branch label to return.
    # 3) Three branch nodes setting {"grade": "A" / "Pass" / "Fail"}.
    # 4) "finalize" node: return {"message": f'{normalized}: {grade}'}.
    # 5) Wire it:
    #      add_edge(START, "clamp")
    #      add_conditional_edges("clamp", router, { label -> node ... })
    #      add_edge(<each branch>, "finalize")
    #      add_edge("finalize", END)
    # 6) return builder.compile()
    raise NotImplementedError("Implement build_graph() — see README.md")


if __name__ == "__main__":
    graph = build_graph()
    for score in (95, 60, 59, 150, -5):
        print(score, "->", graph.invoke({"score": score})["message"])
