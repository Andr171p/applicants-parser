import logging

from pydantic import BaseModel, Field

from langchain_core.language_models import BaseChatModel

from .utils import create_structured_output_llm_chain
from .states import AgentState

logger = logging.getLogger(__name__)


class Plan(BaseModel):
    steps: list[str] = Field(description="")


class PlanStepsNode:
    def __init__(self, model: BaseChatModel) -> None:
        self.llm_chain = create_structured_output_llm_chain(
            output_schema=Plan,
            prompt_template="",
            model=model
        )

    async def __call__(self, state: AgentState) -> dict[str, list[str]]:
        logger.info("---PLANNING---")
        plan = await self.llm_chain.ainvoke(...)
        return {"plan": plan.steps}


class ReplanStepsNode:
    def __init__(self) -> None:
        ...

    async def __call__(self, state: AgentState) -> dict[str, list[str]]:
        logger.info("---REPLANNING---")
        ...


def should_continue(state: AgentState) -> ...:
    ...
