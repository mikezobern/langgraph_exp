"""Editorial (model solution) — Problem 0005: Accumulating State with a Reducer.

This is a reference answer. Try to solve `solution.py` on your own first;
peek here only when you're stuck or to compare after passing the tests.

Key idea
--------
A state key's UPDATE behavior is controlled by its reducer:

  - no reducer        -> overwrite (last write wins)        e.g. `n: int`
  - Annotated[T, fn]  -> combine with reducer `fn`          e.g. `log: Annotated[list[str], add]`

`operator.add` on lists means `["a"] + ["b"] == ["a", "b"]`, so each node returning
`{"log": [entry]}` *appends* one line; the reducer concatenates them in execution order
(and also onto whatever `log` was passed in initially).

This is why nodes return small partial updates instead of the whole state object: the reducer
merges each update into the channel.

    START -> double -> increment -> square -> END
"""

from typing import Annotated, TypedDict
from operator import add

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    n: int                          # overwrite (we want the latest value)
    log: Annotated[list[str], add]  # reducer -> accumulate


def build_graph():
    def double(state: State) -> dict:
        n = state["n"] * 2
        return {"n": n, "log": [f"doubled to {n}"]}

    def increment(state: State) -> dict:
        n = state["n"] + 1
        return {"n": n, "log": [f"incremented to {n}"]}

    def square(state: State) -> dict:
        n = state["n"] * state["n"]
        return {"n": n, "log": [f"squared to {n}"]}

    builder = StateGraph(State)
    builder.add_node("double", double)
    builder.add_node("increment", increment)
    builder.add_node("square", square)

    builder.add_edge(START, "double")
    builder.add_edge("double", "increment")
    builder.add_edge("increment", "square")
    builder.add_edge("square", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"n": 3, "log": []})
    print("n   =", result["n"])     # 49
    print("log =", result["log"])   # ['doubled to 6', 'incremented to 7', 'squared to 49']
