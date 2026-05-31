# 0002 — Conditional Routing (FizzBuzz Graph)

**Difficulty:** Easy–Medium
**New concepts:** conditional edges (`add_conditional_edges`), a **router** function, `path_map`
**Recap from 0001:** `StateGraph`, `TypedDict` state, `add_node`, `add_edge`, `START`, `END`, `.compile()`, `.invoke()`

## Run the tests

```bash
source venv/bin/activate && pytest problems/0002_conditional_routing -v
```

(In PyCharm you can also open `test_solution.py` and click the green ▶.)

---

## The objects you'll meet

In 0001 every edge was **unconditional**: A always goes to B (`add_edge(A, B)`). Real graphs need to
**branch** — pick the next node based on the current state. That's what **conditional edges** do.

### A router function

A router is a plain function that looks at the state and **returns a string** — a label telling the
graph which way to go. It does **not** change the state; it only decides the route.

```python
def route(state: State) -> str:
    if state["n"] % 2 == 0:
        return "even"
    return "odd"
```

### `add_conditional_edges`

You attach the router to a source (a node, or `START`). LangGraph calls the router, takes the
returned label, looks it up in the **`path_map`**, and jumps to the mapped node.

```python
builder.add_conditional_edges(
    START,            # the source: routing happens right at the start
    route,            # the router function
    {                 # path_map: router's return value -> node name
        "even": "even_node",
        "odd": "odd_node",
    },
)
```

- The router's **return value** is just a label/key. It does **not** have to equal a node name —
  the `path_map` is what maps label → actual node.
- Every label the router can return **must** appear in the `path_map`.

### The shape of this graph

```
            ┌── "fizzbuzz" ──┐
            ├── "fizz" ──────┤
START ─(router)              ├──> END
            ├── "buzz" ──────┤
            └── "number" ────┘
```

---

## Task

Implement `build_graph()` in `solution.py`. The graph plays **FizzBuzz** for a single number.

State (`TypedDict`):

```python
class State(TypedDict):
    n: int        # input
    output: str   # what your graph writes
```

Routing rules, based on `n`:

| Condition                | `output` |
|--------------------------|----------|
| divisible by **15**      | `"FizzBuzz"` |
| divisible by **3** only  | `"Fizz"` |
| divisible by **5** only  | `"Buzz"` |
| otherwise                | `str(n)` (the number as text, e.g. `"7"`) |

Requirements:

- Use a **router** + `add_conditional_edges(START, ...)` to choose the branch.
- Each branch is its **own node** that sets `output`. Use exactly these node names:
  **`"fizzbuzz"`**, **`"fizz"`**, **`"buzz"`**, **`"number"`** (tests check for them).
- Every branch then goes to `END`.

### Example

```python
graph = build_graph()
graph.invoke({"n": 15})["output"]  # -> "FizzBuzz"
graph.invoke({"n": 9})["output"]   # -> "Fizz"
graph.invoke({"n": 10})["output"]  # -> "Buzz"
graph.invoke({"n": 7})["output"]   # -> "7"
```

### Constraints / hints

- Order matters in the router: check **15 first**, otherwise 15 would be caught by the "3" rule.
- The router only **decides**; the **node** sets `output`. Keep that separation.
- No LLM, no network.
