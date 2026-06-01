# 0005 — Accumulating State with a Reducer

**Difficulty:** Medium
**New concept:** **reducers** via `typing.Annotated` (how a state channel is *updated*).
**You'll reuse:** `StateGraph`, `TypedDict` state, nodes, `add_edge`, `START`, `END`,
`.compile()`, `.invoke()` (from 0001–0004).

## Run the tests

```bash
source venv/bin/activate && pytest problems/0005_reducer_accumulate -v
```

(In PyCharm you can also open `test_solution.py` and click the green ▶.)

---

## The new object: a reducer

So far, when a node returned `{"key": value}`, it **overwrote** that key. That's the default channel
behavior: **last write wins**.

But sometimes you want updates to **combine** instead of overwrite — e.g. an append-only log, a
growing list of messages, a running total. You control this per-key with a **reducer**.

A reducer is a function `(current_value, update) -> new_value`. You attach it to a state key using
`typing.Annotated`:

```python
from typing import Annotated, TypedDict
from operator import add   # add(list_a, list_b) -> list_a + list_b

class State(TypedDict):
    total: int                       # no reducer -> OVERWRITE (last write wins)
    log: Annotated[list[str], add]   # reducer = add -> CONCATENATE updates
```

Now compare two nodes both touching `log`:

```python
def step_one(state): return {"log": ["one"]}
def step_two(state): return {"log": ["two"]}
# After both run, with the `add` reducer:  log == ["one", "two"]   (not ["two"])
```

This is exactly why nodes should return **small partial updates** (e.g. `{"log": [entry]}`): the
reducer merges each update into the channel. Returning the whole state object would fight the reducer.

> `operator.add` works because `["a"] + ["b"] == ["a", "b"]`. Any 2-arg function can be a reducer.

---

## Task

Implement `build_graph()` in `solution.py`: a 3-step number pipeline that **also records a log of
what it did**, where the log **accumulates** across nodes.

State (`TypedDict`):

```python
class State(TypedDict):
    n: int               # overwritten each step (we want the latest value)
    log: list[str]       # <-- YOU must make this ACCUMULATE (add a reducer)
```

Nodes (run in this order), each updates `n` **and** appends one line to `log`:

1. node **`"double"`**:    `n = n * 2`, append `f"doubled to {n}"`
2. node **`"increment"`**: `n = n + 1`, append `f"incremented to {n}"`
3. node **`"square"`**:    `n = n * n`, append `f"squared to {n}"`

Wiring: `START → double → increment → square → END`.

### Example

```python
graph = build_graph()
result = graph.invoke({"n": 3, "log": []})
result["n"]    # -> 49     (3 -> 6 -> 7 -> 49)
result["log"]  # -> ["doubled to 6", "incremented to 7", "squared to 49"]
```

### Constraints / hints

- The whole point: make `log` accumulate. Use `Annotated[list[str], add]` (with `from operator
  import add`). Without the reducer, `log` would only contain the **last** entry — a test checks this.
- `n` has **no** reducer on purpose: each step should overwrite it with the new value.
- Each node returns a small partial update, e.g. `return {"n": new_n, "log": [f"doubled to {new_n}"]}`.
  Note `log`'s update is a **list with one element** — the reducer concatenates it onto the rest.
- No LLM, no network.
