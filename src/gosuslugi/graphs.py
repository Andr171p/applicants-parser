from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from ..core.base import Broker
from .states import UniversityState, AdmissionListState
from .nodes import (
    ParseUniversity,
    FilterDirectionURLs,
    ParseDirection,
    DownloadApplicants,
    ParseApplicants,
    ParseAdmissionLists
)


def build_university_graph(
        broker: Broker,
        browser: AsyncBrowser
) -> CompiledStateGraph[UniversityState]:
    graph = StateGraph(UniversityState)
    # Добавления узлов (вершин) графа
    graph.add_node("parse_university", ParseUniversity(browser))
    graph.add_node("filter_direction_urls", FilterDirectionURLs(browser))
    graph.add_node("parse_admission_lists", ParseAdmissionLists(broker, browser))
    # Добавление ребёр графа
    graph.add_edge(START, "parse_university")
    graph.add_edge("parse_university", "filter_direction_urls")
    graph.add_edge("filter_direction_urls", "parse_admission_lists")
    graph.add_edge("parse_admission_lists", END)
    # Компиляция графа
    return graph.compile()


def build_admission_list_graph(browser: AsyncBrowser) -> CompiledStateGraph[AdmissionListState]:
    graph = StateGraph(AdmissionListState)
    # Добавление узлов (вершин) графа
    graph.add_node("parse_direction", ParseDirection(browser))
    graph.add_node("download_applicants", DownloadApplicants(browser))
    graph.add_node("parse_applicants", ParseApplicants(browser))
    # Добавление рёбер графа
    graph.add_edge(START, "parse_direction")
    graph.add_edge("parse_direction", "download_applicants")
    graph.add_edge("download_applicants", "parse_applicants")
    graph.add_edge("parse_applicants", END)
    # Компиляция графа
    return graph.compile()
