from typing import Union

import logging

from pydantic import BaseModel, Field

from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel

from langgraph.graph.state import END
from langgraph.prebuilt import create_react_agent

from .states import PlanState
from .utils import create_structured_output_llm_chain

logger = logging.getLogger(__name__)


class Plan(BaseModel):
    """План для достижения поставленной задачи"""
    steps: list[str] = Field(
        description="Различные шаги, которые необходимо выполнить, должны быть отсортированы"
    )


class PlanStepsNode:
    """Узел графа для планирования задач"""
    def __init__(self, model: BaseChatModel) -> None:
        self.planner = create_structured_output_llm_chain(
            output_schema=Plan,
            model=model,
            prompt_template=""
        )

    async def __call__(self, state: PlanState) -> dict[str, list[str]]:
        logger.info("---PLAN STEPS---")
        plan = await self.planner.ainvoke({"task": state["task"]})
        return plan.steps


class ExecuteStepNode:
    def __init__(self, model: BaseChatModel, tools: list[BaseTool], prompt: str) -> None:
        self.agent = create_react_agent(model=model, tools=tools, prompt=prompt)

    async def __call__(self, state: PlanState) -> PlanState:
        logger.info("---EXECUTE STEP---")
        plan, past_steps = state["plan"], state.get("past_steps", [])
        formatted_plan = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(plan))
        task = plan[len(past_steps) + 1] if not past_steps else plan[len(past_steps)]
        formatted_task = f"""Для этого плана: {formatted_plan}
        
        Тебе нужно выполнить: {task}.
        """
        response = await self.agent.ainvoke({"messages": [("user", formatted_task)]})
        return {"past_steps": [(task, response["messages"][-1].content)]}


class Response(BaseModel):
    """Ответ пользователю"""
    response: str


class Action(BaseModel):
    """Действие которое необходимо выполнить"""
    action: Union[Response, Plan] = Field(
        description="""Действие, которое необходимо выполнить. Если ты хочешь ответить пользователю, используй Response. "
        «Если тебе нужно дополнительно использовать инструменты для получения ответа, используй Plan"""
    )


class ReplanStepsNode:
    """Узел графа для перепланирования задач и формирования ответа для пользователя"""
    def __init__(self, model: BaseChatModel) -> None:
        self.replanner = create_structured_output_llm_chain(
            output_schema=Action,
            model=model,
            prompt_template=""
        )

    async def __call__(self, state: PlanState) -> dict[str, Union[list[str], str]]:
        logger.info("---REPLAN STEPS---")
        output = await self.replanner.ainvoke(state)
        if isinstance(output.action, Response):
            return {"response": output.action.response}
        else:
            return {"plan": output.action.steps}


def should_end(state: PlanState) -> str | END:
    """Узел графа для принятия решения о выборе следующего узла"""
    if "response" in state and state["response"]:
        return END
    else:
        return "agent"
