# 0004 — Calculator (Nested Routing)

**Difficulty:** Medium (consolidation)
**New concepts:** none.
**You'll reuse:** `StateGraph`, `TypedDict` state, `add_node`, `add_edge`, `START`, `END`,
`.compile()`, `.invoke()`, `add_conditional_edges` + router + `path_map` (from 0001–0003).

## Run the tests

```bash
source venv/bin/activate && pytest problems/0004_calculator_nested_routing -v
```

(In PyCharm you can also open `test_solution.py` and click the green ▶.)

---

## What's new here (same objects, new shapes)

1. **Two routing stages in one graph.** You'll branch once on the operator, and — only inside the
   division branch — branch again on whether the divisor is zero. That's just
   `add_conditional_edges` used twice, at two different sources.
2. **A pass-through "hub" node.** A node doesn't have to change the state. `"check_div"` returns an
   empty update (`{}`) and exists only to be a *source* for the second routing decision. Useful when
   you want a named place in the graph to branch from.

```
                ┌── add ───────────────┐
                ├── sub ───────────────┤
START ─(op?)────┤                       ├──> END
                ├── mul ───────────────┤
                └── check_div ─(b==0?)──┤
                        │  zero → div_error
                        └─ ok   → div_ok
```

---

## Task

Implement `build_graph()` in `solution.py`: a tiny integer calculator.

State (`TypedDict`):

```python
class State(TypedDict):
    a: int        # left operand
    b: int        # right operand
    op: str       # one of "+", "-", "*", "/"
    result: int   # numeric result
    message: str  # human-readable text
```

Flow:

1. From `START`, **route on `op`** into one of four nodes:
   - `"+"` → node **`"add"`**
   - `"-"` → node **`"sub"`**
   - `"*"` → node **`"mul"`**
   - `"/"` → node **`"check_div"`**
2. `"add"`, `"sub"`, `"mul"` each compute `result` and set `message`, then go to `END`:
   - add → `result = a + b`, `message = f"{a} + {b} = {result}"`
   - sub → `result = a - b`, `message = f"{a} - {b} = {result}"`
   - mul → `result = a * b`, `message = f"{a} * {b} = {result}"`
3. `"check_div"` is a **pass-through hub** (returns `{}`). From it, **route on whether `b == 0`**:
   - `b == 0` → node **`"div_error"`** → `result = 0`, `message = "division by zero"`
   - otherwise → node **`"div_ok"`** → `result = a // b` (**integer** division),
     `message = f"{a} / {b} = {result}"`
4. `"div_ok"` and `"div_error"` go to `END`.

Use exactly these node names (tests check for them):
**`"add"`, `"sub"`, `"mul"`, `"check_div"`, `"div_ok"`, `"div_error"`**.

### Example

```python
graph = build_graph()
graph.invoke({"a": 4,  "b": 5, "op": "+"})["message"]  # -> "4 + 5 = 9"
graph.invoke({"a": 9,  "b": 4, "op": "-"})["message"]  # -> "9 - 4 = 5"
graph.invoke({"a": 6,  "b": 7, "op": "*"})["message"]  # -> "6 * 7 = 42"
graph.invoke({"a": 10, "b": 3, "op": "/"})["message"]  # -> "10 / 3 = 3"   (integer division)
graph.invoke({"a": 10, "b": 0, "op": "/"})             # -> result 0, message "division by zero"
```

### Constraints / hints

- Use **integer** division (`//`) for `"/"`.
- A node may return `{}` to change nothing — that's how `"check_div"` works as a routing hub.
- Two `add_conditional_edges` calls: one from `START` (op), one from `"check_div"` (zero check).
- No LLM, no network.
