from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from .states import PlanState


def build_graph() -> CompiledStateGraph[PlanState]:
    workflow = ...
