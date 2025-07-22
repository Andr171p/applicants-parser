from typing import Protocol

from pydantic import BaseModel


class Broker(Protocol):
    """Абстрактный класс брокера сообщений"""
    async def publish(
            self,
            messages: str | dict | list[dict] | BaseModel | list[BaseModel],
            **kwargs
    ) -> None:
        pass
