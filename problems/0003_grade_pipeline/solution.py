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
    builder = StateGraph(State)
    # 1) "clamp" node: normalized = max(0, min(100, score)); return {"normalized": ...}
    def clamp_node(state:State):
        v = state['score']
        v = int(v)
        print(v)
        norm = max(0, min(100,v))
        return {'normalized':norm}

    builder.add_node('clamp',clamp_node)
    # 2) router(state) -> str: decide by state["normalized"] which branch label to return.
    def router(state:State):
        norm = state['normalized']
        if norm>=90:
            return "A"
        elif norm>=60:
            return 'PASS'
        return 'FAIL'
    # 3) Three branch nodes setting {"grade": "A" / "Pass" / "Fail"}.
    def grade_a(state:State):
        return {'grade':'A'}
    def grade_pass(state:State):
        return {'grade':'Pass'}
    def grade_fail(state:State):
        return {'grade':'Fail'}
    for f in (grade_a, grade_pass,grade_fail):
        builder.add_node(f.__name__, f)

    # 4) "finalize" node: return {"message": f'{normalized}: {grade}'}.
    def finalize(state:State):
        normalized = state['normalized']
        grade = state['grade']
        return {"message": f'{normalized}: {grade}'}
    builder.add_node('finalize', finalize)

    # 5) Wire it:
    #      add_edge(START, "clamp")
    builder.add_edge(START, 'clamp')
    #      add_conditional_edges("clamp", router, { label -> node ... })
    builder.add_conditional_edges('clamp', router, {'A':'grade_a','PASS':'grade_pass','FAIL':'grade_fail'})
    #      add_edge(<each branch>, "finalize")
    builder.add_edge('grade_a', 'finalize')
    builder.add_edge('grade_pass', 'finalize')
    builder.add_edge('grade_fail', 'finalize')

    #      add_edge("finalize", END)
    builder.add_edge('finalize', END)
    # 6) return builder.compile()
    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    for score in (95, 60, 59, 150, -5):
        print(score, "->", graph.invoke({"score": score})["message"])
