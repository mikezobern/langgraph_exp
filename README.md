# LangGraph Dojo — LeetCode for LangGraph

A LeetCode-style training ground for learning [LangGraph](https://langchain-ai.github.io/langgraph/),
one small, focused problem at a time.

Each problem introduces a LangGraph object (just like LeetCode introduces a class such as
`TreeNode`), gives you a small task built around that object (and objects from previous problems),
ships with a boilerplate file to fill in, and a set of test cases that tell you whether you passed.

## How it works

Every problem lives in its own folder under `problems/`, named like `0001_first_stategraph`:

```
problems/
  0001_first_stategraph/
    README.md          # the problem statement + the objects you'll meet
    solution.py        # boilerplate — YOU write your solution here
    test_solution.py   # the test cases (do not edit)
    editorial.py       # model solution + short explanation (peek only when stuck)
```

> **`editorial.py`** is a clean reference answer with a short write-up of the key idea. Try to solve
> on your own first — open it only when you're stuck, or afterwards to compare approaches.

1. Open the problem's `README.md` and read the task.
2. Implement your solution in `solution.py` (replace the `TODO` / `NotImplementedError`).
3. Run the tests. Green = you solved it. Red = a test case failed; the message tells you why.

Every problem's `README.md` contains a **"Run the tests"** section with a ready-to-copy command,
so you never have to assemble the command yourself.

## Running the tests

The runner is **pytest**. Solve **one problem at a time** and run the tests for that problem.

### From the terminal

```bash
source venv/bin/activate
pytest problems/0001_first_stategraph -v
```

### From PyCharm

- Open `test_solution.py` inside the problem folder.
- Click the green ▶ next to a test function (or the class) to run it.
- Make sure the project interpreter is the `venv` in this repo.
- Set the test runner to **pytest**: `Settings → Tools → Python Integrated Tools → Testing → pytest`.

When everything is green you've passed the problem. Move on to the next folder.

## LLM policy

Most problems are **deterministic and need no network or API keys** — the focus is the graph
mechanics. A problem will use a real LLM **only when the concept itself is about LLMs/agents**, and
that problem's README will say so explicitly and tell you which env var (e.g. `OPENAI_API_KEY`) to set.

## Setup

```bash
python3 -m venv venv          # already created in this repo
source venv/bin/activate
pip install -r requirements.txt
```

Installed stack: `langgraph`, `langchain-core`, `langchain-openai`, `pytest`.
