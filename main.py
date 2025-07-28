import asyncio
import logging

from src.app import create_faststream_app, execute_gosuslugi_parser


async def main() -> None:
    await asyncio.gather(
        create_faststream_app(),
        execute_gosuslugi_parser()
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
