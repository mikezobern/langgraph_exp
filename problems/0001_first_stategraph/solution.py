"""Problem 0001 — Your First StateGraph.

Read the task in this folder's README.md, then implement `build_graph()` below.
Run the tests with:  pytest problems/0001_first_stategraph -v
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel


class State(BaseModel):
    name: str
    greeting: str = ""


def build_graph():
    """Build and return a COMPILED graph.

    Requirements:
      - state schema is `State`
      - one node named "greet" that sets state["greeting"] = f"Hello, {name}!"
      - wiring: START -> "greet" -> END

    Return the object produced by `.compile()`.
    """
    # TODO: implement me.
    #
    # 1) Define the node function: it receives `state` and returns
    #    a partial update dict containing only the "greeting" key.
    def greet(S:State):
        answer = f'Hello, {S.name}!'
        S.greeting = answer
        return S # я не хочу писать руками имена ключей, потому сделал стейт из пидантика и возвращаю весь шкаф целиком

    # 2) Create a StateGraph(State) builder.
    builder = StateGraph(State)
    # 3) add_node("greet", <your function>)
    builder.add_node('greet', greet)
    # 4) add_edge(START, "greet") and add_edge("greet", END)
    builder.add_edge(START, 'greet')
    builder.add_edge('greet', END)

    # 5) return builder.compile()
    return builder.compile()
    raise NotImplementedError("Implement build_graph() — see README.md")


if __name__ == "__main__":
    # Quick manual check (the real grading happens in test_solution.py via pytest).
    graph = build_graph()
    print(graph.invoke({"name": "Ada"}))
