# 0003 — Grade Pipeline (Consolidation)

**Difficulty:** Easy–Medium
**New concepts:** none — this is a consolidation problem.
**You'll reuse:** `StateGraph`, `TypedDict` state, `add_node`, `add_edge`, `START`, `END`,
`.compile()`, `.invoke()`, `add_conditional_edges` + router + `path_map` (from 0001–0002).

## Run the tests

```bash
source venv/bin/activate && pytest problems/0003_grade_pipeline -v
```

(In PyCharm you can also open `test_solution.py` and click the green ▶.)

---

## What's new here (same objects, new shapes)

Everything is built from objects you already know, but two arrangements are worth noticing:

1. **Conditional edges can start from a regular node**, not just `START`. In 0002 you routed from
   `START`; here you'll first run a node, *then* branch:
   `add_conditional_edges("clamp", router, path_map)`.
2. **Branches can converge.** Several different nodes can all point to the *same* next node with
   plain `add_edge(branch, "finalize")`. The graph fans out, then fans back in.

```
START → clamp ─(router)─┬── grade_a ────┐
                        ├── grade_pass ──┤→ finalize → END
                        └── grade_fail ──┘
```

---

## Task

Implement `build_graph()` in `solution.py`: a graph that turns a raw `score` into a final message.

State (`TypedDict`):

```python
class State(TypedDict):
    score: int        # raw input (may be out of range)
    normalized: int   # score clamped into [0, 100]
    grade: str        # "A" | "Pass" | "Fail"
    message: str      # final text
```

Pipeline:

1. Node **`"clamp"`** (runs first): set `normalized = max(0, min(100, score))`.
2. From `"clamp"`, **route by `normalized`** into one of three branch nodes:
   - `normalized >= 90`        → node **`"grade_a"`**    → sets `grade = "A"`
   - `60 <= normalized < 90`   → node **`"grade_pass"`** → sets `grade = "Pass"`
   - `normalized < 60`         → node **`"grade_fail"`** → sets `grade = "Fail"`
3. All three branches go to node **`"finalize"`**, which sets
   `message = f"{normalized}: {grade}"`.
4. `"finalize"` → `END`.

Use exactly these node names (tests check for them):
**`"clamp"`, `"grade_a"`, `"grade_pass"`, `"grade_fail"`, `"finalize"`**.

### Example

```python
graph = build_graph()
graph.invoke({"score": 95})["message"]   # -> "95: A"
graph.invoke({"score": 60})["message"]   # -> "60: Pass"
graph.invoke({"score": 59})["message"]   # -> "59: Fail"
graph.invoke({"score": 150})["message"]  # -> "100: A"   (clamped)
graph.invoke({"score": -5})["message"]   # -> "0: Fail"  (clamped)
```

### Constraints / hints

- The router only **decides**; the branch node sets `grade`; `finalize` builds `message`. Keep that
  separation of responsibilities — it mirrors how real pipelines stay readable.
- Boundaries matter: `90` is `"A"`, `89` is `"Pass"`, `60` is `"Pass"`, `59` is `"Fail"`.
- No LLM, no network.
