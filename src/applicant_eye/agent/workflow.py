import asyncio
import logging

from langchain_gigachat import GigaChat

from langgraph.prebuilt import create_react_agent

from src.applicant_eye.agent.toolkit import WebAutomatizationToolKit
from src.applicant_eye.agent.toolkit.browser import BrowserState

model = GigaChat(
    credentials="",
    scope="",
    model="",
    profanity_check=False,
    verify_ssl_certs=False
)

PROMPT = """Ты — ИИ-агент для автоматического поиска конкурсных списков абитуриентов на сайте университета. Твоя задача:

1. Анализировать структуру сайта вуза  
2. Находить разделы с конкурсными списками (рейтингами абитуриентов)  
3. Извлекать актуальные данные в структурированном виде  

Действуй по алгоритму ReAct (Reason → Act):  
- **Reason**: Анализируй текущую ситуацию и определяй следующее действие  
- **Act**: Выбирай инструмент (см. список ниже) и выполняй его  

Правила:  
- Всегда проверяй текущий URL перед действиями  
- Если попадаешь на страницу входа, запроси логин/пароль через `ask_for_clarification`  
- Для конкурсных списков ищи ключевые слова: "рейтинг абитуриентов", "конкурсные списки", "поступающие", "результаты приема"  
"""


async def main() -> None:
    async with BrowserState() as browser_state:
        print(browser_state)
        toolkit = WebAutomatizationToolKit(browser_state=browser_state, model=model)
        agent = create_react_agent(
            model=model,
            tools=toolkit.get_tools(),
            prompt=PROMPT
        )
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Найди конкурсные списки на сайте МГУ"}]}
        )
        print(response)


logging.basicConfig(level=logging.INFO)
asyncio.run(main())
