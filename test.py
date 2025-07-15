import os
import asyncio
from dotenv import load_dotenv

from langchain_gigachat import GigaChat
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from src.applicant_eye.agent.toolkit.tools import open_site

load_dotenv()

model = GigaChat(
        credentials=os.getenv("GIGACHAT_API_KEY"),
        scope=os.getenv("GIGACHAT_SCOPE"),
        model=os.getenv("GIGACHAT_MODEL"),
        verify_ssl_certs=False,
        profanity_check=False
    )

checkpointer = MemorySaver()


async def main() -> None:
    agent = create_react_agent(
        model=model,
        tools=[open_site],
        prompt="Ты полезный ассистент для автоматизации задач в браузере",
        checkpointer=checkpointer
    )
    config = {"configurable": {"thread_id": "123456789"}}
    while True:
        text = input("[User]: ")
        inputs = {"messages": [{"role": "human", "content": text}]}
        response = await agent.ainvoke(inputs, config=config)
        print(response)


asyncio.run(main())
