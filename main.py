import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Filter, Command
from aiogram.types import Message

from dotenv import load_dotenv
from os import environ


class DiceFilter(Filter):
    async def __call__(self, message: Message):
        return (
            message.dice is not None
            and message.dice.emoji == "🎰"
            and message.forward_origin is None
        )


scores: dict[int, tuple[str, int]] = {}

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"мяу :3 {html.bold(message.from_user.full_name)}!")


@dp.message(DiceFilter())
async def echo_handler(message: Message) -> None:
    id = message.from_user.id
    user = message.from_user.username
    value = (message.dice.value - 33) * 100

    if id in scores:
        scores[id] = (user, scores[id][1] + value)
    else:
        scores[id] = (user, value)

    await message.answer(
        f"поздравляю! @{message.from_user.username or "сили"} выиграл {value}$!!!! 🤑🤑🤑"
    )

    # elif message.text and message.text.lower().find("баланс") != -1:
    #     balance = scores.get(message.from_user.id, ("", 0))
    #     await message.answer(
    #         f"баланс @{message.from_user.username or "сили"}: {balance[1]}$"
    #     )


@dp.message(Command("balance"))
async def balance(message: Message):
    balance = scores.get(message.from_user.id, ("", 0))
    await message.answer(
        f"баланс @{message.from_user.username or "сили"}: {balance[1]}$"
    )


async def main() -> None:
    load_dotenv()
    TOKEN = environ["TOKEN"]
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
