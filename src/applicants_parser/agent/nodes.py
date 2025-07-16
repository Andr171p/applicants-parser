from typing import Optional

import json
import logging

from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableConfig
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolMessage, SystemMessage, BaseMessage

# from langgraph.prebuilt import ToolNode

from .states import ReActState

logger = logging.getLogger(__name__)


async def tool_node(state: ReActState) -> dict[str, list[ToolMessage]]:
    logger.info("---CALL TOOL---")
    messages: list[ToolMessage] = []
    tools_by_name: dict[str, BaseTool] = {tool.name: tool for tool in state["tools"]}
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].ainvoke(tool_call["args"])
        messages.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"]
            )
        )
    return {"messages": messages}


class ModelCallingNode:
    def __init__(self, model: BaseChatModel, prompt: str) -> None:
        self.model = model
        self.prompt = prompt

    async def __call__(
            self,
            state: ReActState,
            config: Optional[RunnableConfig] = None
    ) -> dict[str, list[BaseMessage]]:
        logger.info("---MODEL CALLING---")
        message = await self.model.ainvoke(
            [SystemMessage(self.prompt)] + state["messages"], config=config
        )
        return {"messages": [message]}
