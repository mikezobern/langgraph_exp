"""Problem 0004 — Calculator (Nested Routing).

Read the task in this folder's README.md, then implement `build_graph()` below.
Run the tests with:  pytest problems/0004_calculator_nested_routing -v
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
    """Build and return a COMPILED integer calculator graph.

    Two routing stages (see README.md):
      - from START, route on state["op"] -> "add" | "sub" | "mul" | "check_div"
      - from "check_div" (a pass-through hub), route on (b == 0) -> "div_error" | "div_ok"

    Node names must be exactly:
      "add", "sub", "mul", "check_div", "div_ok", "div_error"

    Return the object produced by `.compile()`.
    """
    # TODO: implement me.
    #
    # 1) Nodes "add"/"sub"/"mul": compute result and set message, e.g.
    #       return {"result": a + b, "message": f"{a} + {b} = {a + b}"}
    # 2) "check_div": a hub that changes nothing -> return {}
    # 3) "div_ok": result = a // b, message f"{a} / {b} = {result}"
    #    "div_error": result = 0, message "division by zero"
    # 4) op_router(state) -> str  (label for "+"/"-"/"*"/"/")
    #    zero_router(state) -> str (label for b == 0 vs not)
    # 5) Wire it:
    #       add_conditional_edges(START, op_router, { ... })
    #       add_conditional_edges("check_div", zero_router, { ... })
    #       add_edge(<each terminal node>, END)
    # 6) return builder.compile()
    raise NotImplementedError("Implement build_graph() — see README.md")


if __name__ == "__main__":
    graph = build_graph()
    cases = [
        {"a": 4, "b": 5, "op": "+"},
        {"a": 9, "b": 4, "op": "-"},
        {"a": 6, "b": 7, "op": "*"},
        {"a": 10, "b": 3, "op": "/"},
        {"a": 10, "b": 0, "op": "/"},
    ]
    for c in cases:
        print(c, "->", graph.invoke(c)["message"])
