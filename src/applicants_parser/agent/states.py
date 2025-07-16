import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage

from langgraph.graph.message import add_messages


class PlanState(TypedDict):
    ...


class ReActState(TypedDict):
    """Состояние ReAct агента"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    tools: list[BaseTool]
