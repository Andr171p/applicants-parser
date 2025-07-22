# from langgraph.graph import StateGraph  # noqa: ERA001
from langgraph.graph.state import CompiledStateGraph

from .states import PlanState


def build_graph() -> CompiledStateGraph[PlanState]:
    ...
