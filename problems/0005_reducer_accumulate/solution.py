"""Problem 0005 — Accumulating State with a Reducer.

Read the task in this folder's README.md, then implement `build_graph()` below.
Run the tests with:  pytest problems/0005_reducer_accumulate -v
"""

from typing import Annotated, TypedDict
from operator import add  # noqa: F401  (you'll likely need this for the reducer)

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    n: int
    log: Annotated[list[str],add]


def build_graph():
    """Build and return a COMPILED graph: 3 steps that transform n and append to log.

    Pipeline:  START -> "double" -> "increment" -> "square" -> END

    Each node updates `n` AND appends one entry to `log` (which must accumulate):
      - "double":    n = n * 2,  append f"doubled to {n}"
      - "increment": n = n + 1,  append f"incremented to {n}"
      - "square":    n = n * n,  append f"squared to {n}"

    Return the object produced by `.compile()`.
    """
    # 2) Write the three nodes; each returns {"n": new_n, "log": [<one entry>]}.
    def double(state:State):
        n = state['n']
        return {'n': 2*n, 'log':[f"doubled to {2*n}"]}
    def increment(state:State):
        n = state['n']
        return {'n': 1+n, 'log':[f"incremented to {n+1}"]}
    def square(state:State):
        n = state['n']
        return {'n': n*n, 'log':[f"squared to {n*n}"]}

    # 3) builder = StateGraph(State); add the three nodes.
    builder = StateGraph(State)
    builder.add_node('double', double)
    builder.add_node('increment', increment)
    builder.add_node('square', square)
    # 4) Wire START -> double -> increment -> square -> END with add_edge.
    builder.add_edge(START, 'double')
    builder.add_edge('double', 'increment')
    builder.add_edge('increment', 'square')
    builder.add_edge('square', END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"n": 3, "log": []})
    print("n   =", result["n"])
    print("log =", result["log"])
