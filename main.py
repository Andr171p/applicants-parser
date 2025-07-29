import asyncio
import logging

from src.app import start_broker, execute_gosuslugi_parser
from src.constants import TIMEOUT


async def main() -> None:
    async with start_broker():
        await execute_gosuslugi_parser()
        await asyncio.sleep(TIMEOUT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
