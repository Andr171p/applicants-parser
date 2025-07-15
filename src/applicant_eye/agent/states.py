import operator
from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage

from langgraph.graph.message import add_messages


class PlanState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    page_source: str
    plan: list[str]
    past_steps: Annotated[list[tuple[str, str]], operator.add]
    ...


class ReACTState(TypedDict):
    ...
