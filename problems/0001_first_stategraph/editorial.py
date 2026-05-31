"""Editorial (model solution) — Problem 0001: Your First StateGraph.

This is a reference answer. Try to solve `solution.py` on your own first;
peek here only when you're stuck or to compare after passing the tests.

Key idea
--------
A LangGraph computation = nodes (functions) wired by edges, operating on a shared `state`.
The canonical node contract is: receive `state`, return a *partial update* (only the keys you
changed). LangGraph merges that update into the state for you.

    START --> greet --> END
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    greeting: str


def build_graph():
    def greet(state: State) -> dict:
        # Return ONLY the key we change; LangGraph merges it into the state.
        return {"greeting": f"Hello, {state['name']}!"}

    builder = StateGraph(State)
    builder.add_node("greet", greet)
    builder.add_edge(START, "greet")
    builder.add_edge("greet", END)
    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    print(graph.invoke({"name": "Ada"}))     # {'name': 'Ada', 'greeting': 'Hello, Ada!'}
    print(graph.invoke({"name": "Linus"}))   # {'name': 'Linus', 'greeting': 'Hello, Linus!'}
