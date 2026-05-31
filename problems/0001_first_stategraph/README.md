# 0001 — Your First StateGraph

**Difficulty:** Easy
**New concepts:** `StateGraph`, state schema (`TypedDict`), nodes, edges, `START`, `END`, `.compile()`, `.invoke()`

## Run the tests

```bash
source venv/bin/activate && pytest problems/0001_first_stategraph -v
```

(In PyCharm you can also open `test_solution.py` and click the green ▶.)

---

## The objects you'll meet

In LangGraph you describe a computation as a **graph**: a set of **nodes** (functions) connected by
**edges** (who runs after whom). The data flowing through the graph is called the **state**.

### State schema (a `TypedDict`)

The state is a plain dictionary, but you declare its *shape* with a `TypedDict` so LangGraph knows
which keys exist:

```python
from typing import TypedDict

class State(TypedDict):
    name: str
    greeting: str
```

### `StateGraph`

The builder you use to assemble the graph. You give it the state schema:

```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
```

### Nodes

A **node** is just a function. It receives the current `state` (a dict) and returns a **partial
update** — a dict with only the keys it wants to change. LangGraph merges that update into the state.

```python
def my_node(state: State) -> dict:
    return {"greeting": "..."}   # only the keys you changed

builder.add_node("my_node", my_node)   # name, function
```

### Edges, `START` and `END`

Edges define execution order. `START` is the virtual entry point, `END` is the virtual exit point.

```python
builder.add_edge(START, "my_node")   # graph begins -> my_node
builder.add_edge("my_node", END)     # my_node -> graph ends
```

### Compile & invoke

`.compile()` turns the builder into a runnable graph. `.invoke(input)` runs it and returns the
**final state**.

```python
graph = builder.compile()
result = graph.invoke({"name": "Ada"})
# result == {"name": "Ada", "greeting": "Hello, Ada!"}
```

---

## Task

Implement `build_graph()` in `solution.py`. It must **return a compiled graph** with:

- state schema **`State`** (keys: `name: str`, `greeting: str`),
- exactly **one node named `"greet"`**,
- the `"greet"` node sets `greeting` to **`f"Hello, {name}!"`** (using the incoming `name`),
- wiring: `START → "greet" → END`.

### Example

```python
graph = build_graph()
graph.invoke({"name": "Ada"})
# -> {"name": "Ada", "greeting": "Hello, Ada!"}

graph.invoke({"name": "Linus"})
# -> {"name": "Linus", "greeting": "Hello, Linus!"}
```

### Constraints / hints

- A node returns **only the keys it changes** (here: just `greeting`). Don't return `name` again.
- The node name string must be exactly `"greet"` — a test checks for it.
- No LLM, no network: this is pure graph wiring.

When `pytest problems/0001_first_stategraph -v` is all green, you've passed. 🎉
