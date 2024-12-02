import asyncio
import logging
import sys


from dotenv import load_dotenv
from os import environ

from aiogram.enums import ParseMode
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from router import DISPATCHER


scores: dict[int, tuple[str, int]] = {}


async def main() -> None:
    load_dotenv()
    TOKEN = environ["TOKEN"]
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await DISPATCHER.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
