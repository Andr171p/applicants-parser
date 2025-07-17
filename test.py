import asyncio
<<<<<<< HEAD
import os
=======
import logging
>>>>>>> c03a143c969567c7d1f29d907bcdf276459247fd

from dotenv import load_dotenv
from langchain_gigachat import GigaChat
<<<<<<< HEAD
from langgraph.checkpoint.memory import MemorySaver
=======

>>>>>>> c03a143c969567c7d1f29d907bcdf276459247fd
from langgraph.prebuilt import create_react_agent

from src.applicants_parser.agent.toolkit import BrowserAutomatizationToolKit
from src.applicants_parser.browser import BrowserState

model = GigaChat(
<<<<<<< HEAD
    credentials=os.getenv("GIGACHAT_API_KEY"),
    scope=os.getenv("GIGACHAT_SCOPE"),
    model=os.getenv("GIGACHAT_MODEL"),
    verify_ssl_certs=False,
    profanity_check=False,
=======
    credentials="",
    scope="",
    model="",
    profanity_check=False,
    verify_ssl_certs=False
>>>>>>> c03a143c969567c7d1f29d907bcdf276459247fd
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
<<<<<<< HEAD
    agent = create_react_agent(
        model=model,
        tools=[open_site],
        prompt="Ты полезный ассистент для автоматизации задач в браузере",
        checkpointer=checkpointer,
    )
    config: dict[str, dict[str, str]] = {"configurable": {"thread_id": "123456789"}}
    while True:
        text = input("[User]: ")
        inputs = {"messages": [{"role": "human", "content": text}]}
        response = await agent.ainvoke(inputs, config=config)
=======
    async with BrowserState() as browser_state:
        print(browser_state)
        toolkit = BrowserAutomatizationToolKit(browser_state=browser_state, model=model)
        agent = create_react_agent(
            model=model,
            tools=toolkit.get_tools(),
            prompt=PROMPT
        )
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Найди конкурсные списки на сайте МГУ"}]}
        )
>>>>>>> c03a143c969567c7d1f29d907bcdf276459247fd
        print(response)


logging.basicConfig(level=logging.INFO)
asyncio.run(main())
