"""Problem 0005 — Accumulating State with a Reducer.

Read the task in this folder's README.md, then implement `build_graph()` below.
Run the tests with:  pytest problems/0005_reducer_accumulate -v
"""

from typing import Annotated, TypedDict
from operator import add  # noqa: F401  (you'll likely need this for the reducer)

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    n: int
    # TODO: make `log` ACCUMULATE across nodes instead of being overwritten.
    #       Hint: Annotated[list[str], <reducer>].
    log: list[str]


def build_graph():
    """Build and return a COMPILED graph: 3 steps that transform n and append to log.

    Pipeline:  START -> "double" -> "increment" -> "square" -> END

    Each node updates `n` AND appends one entry to `log` (which must accumulate):
      - "double":    n = n * 2,  append f"doubled to {n}"
      - "increment": n = n + 1,  append f"incremented to {n}"
      - "square":    n = n * n,  append f"squared to {n}"

    Return the object produced by `.compile()`.
    """
    # TODO: implement me.
    #
    # 1) First fix the `State` above so `log` accumulates (add a reducer via Annotated).
    # 2) Write the three nodes; each returns {"n": new_n, "log": [<one entry>]}.
    # 3) builder = StateGraph(State); add the three nodes.
    # 4) Wire START -> double -> increment -> square -> END with add_edge.
    # 5) return builder.compile()
    raise NotImplementedError("Implement build_graph() — see README.md")


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"n": 3, "log": []})
    print("n   =", result["n"])
    print("log =", result["log"])
