"""Editorial (model solution) — Problem 0002: Conditional Routing (FizzBuzz Graph).

This is a reference answer. Try to solve `solution.py` on your own first;
peek here only when you're stuck or to compare after passing the tests.

Key idea
--------
Branching is done with `add_conditional_edges(source, router, path_map)`:

  - the ROUTER reads the state and returns a *label* (a string) — it does NOT mutate state;
  - the PATH_MAP maps each label to the node to jump to;
  - here we route straight from START, so the very first step is chosen dynamically.

The classic trap: check divisibility by 15 BEFORE 3 and 5, otherwise 15 is swallowed by "Fizz".

              ┌── fizzbuzz ──┐
              ├── fizz ──────┤
    START ─(route)           ├──> END
              ├── buzz ──────┤
              └── number ────┘
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    n: int
    output: str


def build_graph():
    def route(state: State) -> str:
        n = state["n"]
        if n % 15 == 0:        # must come first
            return "fizzbuzz"
        if n % 3 == 0:
            return "fizz"
        if n % 5 == 0:
            return "buzz"
        return "number"

    def fizzbuzz(state: State) -> dict:
        return {"output": "FizzBuzz"}

    def fizz(state: State) -> dict:
        return {"output": "Fizz"}

    def buzz(state: State) -> dict:
        return {"output": "Buzz"}

    def number(state: State) -> dict:
        return {"output": str(state["n"])}

    builder = StateGraph(State)
    builder.add_node("fizzbuzz", fizzbuzz)
    builder.add_node("fizz", fizz)
    builder.add_node("buzz", buzz)
    builder.add_node("number", number)

    # Router label -> node name. (Here labels equal node names, but they need not.)
    builder.add_conditional_edges(
        START,
        route,
        {
            "fizzbuzz": "fizzbuzz",
            "fizz": "fizz",
            "buzz": "buzz",
            "number": "number",
        },
    )
    for name in ("fizzbuzz", "fizz", "buzz", "number"):
        builder.add_edge(name, END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    for n in (15, 9, 10, 7):
        print(n, "->", graph.invoke({"n": n})["output"])
