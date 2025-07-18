from typing import Annotated, TypedDict

import operator
from collections.abc import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class PlanState(TypedDict):
    """
    Состояние агента планировщика для декомпозиции большой задачи

    :param task: Задача которую надо разбить
    :param plan: Последовательный план выполнения задачи
    :param past_steps: Проделанные шаги
    :param response: Сформированный ответ пользователю
    """
    task: str
    plan: list[str]
    past_steps: Annotated[list[tuple[str, str]], operator.add]
    response: str


class ReActState(TypedDict):
    """
    Состояние ReAct агента для выполнения задач в браузере

    :param messages: История сообщений
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
