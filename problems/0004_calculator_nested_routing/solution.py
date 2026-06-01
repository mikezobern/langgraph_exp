"""Problem 0004 — Calculator (Nested Routing).

Read the task in this folder's README.md, then implement `build_graph()` below.
Run the tests with:  pytest problems/0004_calculator_nested_routing -v
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    a: int
    b: int
    op: str
    result: int
    message: str


def build_graph():
    """Build and return a COMPILED integer calculator graph.

    Two routing stages (see README.md):
      - from START, route on state["op"] -> "add" | "sub" | "mul" | "check_div"
      - from "check_div" (a pass-through hub), route on (b == 0) -> "div_error" | "div_ok"

    Node names must be exactly:
      "add", "sub", "mul", "check_div", "div_ok", "div_error"

    Return the object produced by `.compile()`.
    """
    G = StateGraph(State)
    # 1) Nodes "add"/"sub"/"mul": compute result and set message, e.g.
    #       return {"result": a + b, "message": f"{a} + {b} = {a + b}"}
    def add(state:State):
        return {'result':state['a']+state['b'], 'message':f"{state['a']} + {state['b']} = {state['a'] + state['b']}"}
    def sub(state:State):
        return {'result':state['a']-state['b'], 'message':f"{state['a']} - {state['b']} = {state['a'] - state['b']}"}
    def mul(state:State):
        return {'result':state['a']*state['b'], 'message':f"{state['a']} * {state['b']} = {state['a']*state['b']}"}
    G.add_node('add',add)
    G.add_node('sub', sub)
    G.add_node('mul', mul)

    # 2) "check_div": a hub that changes nothing -> return {}
    def check_div(state:State):
        return {}

    # 3) "div_ok": result = a // b, message f"{a} / {b} = {result}"
    #    "div_error": result = 0, message "division by zero"
    def div_ok(state:State):
        a,b=state['a'],state['b']
        result=a//b

        return {'message' : f"{a} / {b} = {result}", 'result':result}

    def div_error(state:State):
        return {'result':0, 'message':"division by zero"}

    G.add_node('check_div',check_div)
    G.add_node('div_ok',div_ok)
    G.add_node('div_error', div_error)

    # 4) op_router(state) -> str  (label for "+"/"-"/"*"/"/")
    def op_router(state:State):
        oper = state['op']
        if oper=="+":
            return 'PLUS'
        elif oper=="-":
            return "MINUS"
        elif oper=="*":
            return "MULT"
        elif oper=="/":
            return "DIV"

    #    zero_router(state) -> str (label for b == 0 vs not)
    def zero_router(state):
        if state['b']==0:
            return 'ERROR'
        else:
            return 'OK'
    # 5) Wire it:
    #       add_conditional_edges(START, op_router, { ... })
    #       add_conditional_edges("check_div", zero_router, { ... })
    #       add_edge(<each terminal node>, END)
    G.add_conditional_edges(START, op_router, {'PLUS':'add', 'MINUS':'sub', 'MULT':'mul', 'DIV':'check_div'})
    G.add_conditional_edges('check_div', zero_router, {'ERROR': 'div_error', 'OK': 'div_ok'})
    G.add_edge('add', END)
    G.add_edge('sub', END)
    G.add_edge('mul', END)
    G.add_edge('div_ok', END)
    G.add_edge('div_error', END)

    return G.compile()



if __name__ == "__main__":
    graph = build_graph()
    cases = [
        {"a": 4, "b": 5, "op": "+"},
        {"a": 9, "b": 4, "op": "-"},
        {"a": 6, "b": 7, "op": "*"},
        {"a": 10, "b": 3, "op": "/"},
        {"a": 10, "b": 0, "op": "/"},
    ]
    for c in cases:
        print(c, "->", graph.invoke(c)["message"])
