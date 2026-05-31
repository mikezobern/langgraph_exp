"""Problem 0002 — Conditional Routing (FizzBuzz Graph).

Read the task in this folder's README.md, then implement `build_graph()` below.
Run the tests with:  pytest problems/0002_conditional_routing -v
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    n: int
    output: str


def build_graph():
    """Build and return a COMPILED graph that plays FizzBuzz for state["n"].

    Requirements:
      - a router function decides the branch based on n
      - use add_conditional_edges(START, router, path_map)
      - four branch nodes named exactly: "fizzbuzz", "fizz", "buzz", "number"
      - each node sets state["output"] (see the table in README.md)
      - every node then goes to END

    Return the object produced by `.compile()`.
    """
    # TODO: implement me.
    #
    # 1) Write the router:  def route(state) -> str  returning one of the
    #    labels you'll use in the path_map (e.g. "fizzbuzz"/"fizz"/"buzz"/"number").
    #    Remember: check divisibility by 15 BEFORE 3 and 5.
    # 2) Write the four branch nodes; each returns {"output": ...}.
    # 3) builder = StateGraph(State); add the four nodes.
    # 4) builder.add_conditional_edges(START, route, { ...label -> node... })
    # 5) Connect every branch node to END with add_edge(node, END).
    # 6) return builder.compile()
    raise NotImplementedError("Implement build_graph() — see README.md")


if __name__ == "__main__":
    graph = build_graph()
    for n in (15, 9, 10, 7):
        print(n, "->", graph.invoke({"n": n})["output"])
