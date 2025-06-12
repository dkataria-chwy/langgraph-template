"""
Core helpers for every LangGraph workflow.
• default_state  – fills missing keys with sensible defaults.
• build_graph    – converts {agents, edges} → compiled LangGraph.
"""

from typing import Annotated, Awaitable, Callable, Dict, List, TypedDict, \
                   get_type_hints, get_origin
from langgraph.graph import StateGraph, END

Agent = Callable[[dict], Awaitable[Dict[str, object]]]  # generic node type

# ────────────────────────────────────────────────────────────────
# Create a blank State with [] / None defaults so users only fill
# the keys they care about.
# ────────────────────────────────────────────────────────────────
def default_state(state_model: type, **overrides) -> dict:
    blank = {"current_step": "start", "errors": []}
    for key, tp in get_type_hints(state_model, include_extras=True).items():
        if key in blank or key in overrides:
            continue                                    # already supplied
        origin = get_origin(tp) or tp
        if origin is Annotated:                         # unwrap Annotated[…]
            origin = get_origin(tp.__args__[0]) or tp.__args__[0]
        blank[key] = [] if origin is list else None
    blank.update(overrides)
    return blank

# ────────────────────────────────────────────────────────────────
# Build the LangGraph once we know:
#   • State model  (TypedDict)
#   • agents       {name: wrapper fn}
#   • edges        {parent: [child, …]}
#   • entry        first node name
# ────────────────────────────────────────────────────────────────
def build_graph(
    state_model: type,
    agents: Dict[str, Agent],
    edges: Dict[str, List[str]],
    entry: str,
    max_concurrency: int = 6,
):
    g = StateGraph(state_model)

    # add nodes
    for name, fn in agents.items():
        g.add_node(name, fn)

    # entry point
    g.set_entry_point(entry)

    # edges
    for parent, children in edges.items():
        for child in children:
            g.add_edge(parent, child)

    # finish at END automatically
    g.add_edge(list(agents)[-1], END)
    return g.compile(max_concurrency=max_concurrency) 