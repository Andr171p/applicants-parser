from typing import TypeVar

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def create_structured_output_llm_chain[T: BaseModel](
    output_schema: type[T], model: BaseChatModel, prompt_template: str
) -> Runnable[dict[str, str], T]:
    parser = PydanticOutputParser(pydantic_object=output_schema)
    prompt = ChatPromptTemplate.from_messages([("system", prompt_template)]).partial(
        format_instructions=parser.get_format_instructions()
    )
    return prompt | model | parser
