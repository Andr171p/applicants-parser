from typing import TypeVar

from pydantic import BaseModel

from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser

T = TypeVar("T", bound=BaseModel)


def create_structured_output_llm_chain(
        output_schema: type[T],
        model: BaseChatModel,
        prompt_template: str
) -> Runnable[dict[str, str], T]:
    parser = PydanticOutputParser(pydantic_object=output_schema)
    prompt = (
        ChatPromptTemplate.from_messages([("system", prompt_template)])
        .partial(format_instructions=parser.get_format_instructions())
    )
    return prompt | model | parser
