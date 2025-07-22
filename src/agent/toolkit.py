from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import ConfigDict, Field


class BrowserAutomatizationToolKit(BaseToolkit):
    # browser_state: BrowserState = Field(exclude=True)
    llm: BaseChatModel = Field(exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_tools(self) -> list[BaseTool]:
        return []
