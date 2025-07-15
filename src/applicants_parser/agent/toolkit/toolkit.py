from pydantic import Field, ConfigDict

from langchain_core.tools import BaseToolkit
from langchain_core.language_models import BaseChatModel

from .tools import *
from .browser import BrowserState


class WebAutomatizationToolKit(BaseToolkit):
    browser_state: BrowserState = Field(exclude=True)
    model: BaseChatModel = Field(exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_tools(self) -> list[BaseTool]:
        return [
            OpenURLTool(self.browser_state),
            NavigationTool(self.browser_state),
            ClickButtonTool(self.browser_state),
            ExtractTextTool(self.browser_state),
            SearchElementTool(self.browser_state, self.model)
        ]
