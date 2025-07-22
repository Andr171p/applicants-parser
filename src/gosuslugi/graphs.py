from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from .states import UniversityState
from .nodes import (
    ParseUniversity,
    FilterDirections,
    ParseDirection,
    DownloadApplicants,
    ParseApplicants
)


def build_university_graph(browser: AsyncBrowser) -> CompiledStateGraph[UniversityState]:
    graph = StateGraph(UniversityState)
    # Добавления узлов (вершин) графа
    graph.add_node("parse_university", ParseUniversity(browser))
    graph.add_node("filter_directions", FilterDirections(browser))
    graph.add_node("parse_direction", ParseDirection(browser))
    # Добавление ребёр графа
    ...
