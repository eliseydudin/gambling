import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = "7964551134:AAHhHsEE0nE9p8Qg-s706X36jfbpHrzB03U"

scores: dict[int, tuple[str, int]] = {}

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"мяу :3 {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    if message.dice and message.forward_origin is None:
        dice = message.dice
        if dice.emoji != "🎰":
            await message.answer("ты ебанашка? в боте нужно отправлять только 🎰")
            return

        id = message.from_user.id
        user = message.from_user.username
        value = (dice.value - 33) * 100

        if id in scores:
            scores[id] = (user, scores[id][1] + value)
        else:
            scores[id] = (user, value)

        await message.answer(
            f"поздравляю! @{message.from_user.username or "сили"} выиграл {value}$!!!! 🤑🤑🤑"
        )
    elif message.text and message.text.lower().find("баланс") != -1:
        balance = scores.get(message.from_user.id, ("", 0))
        await message.answer(
            f"баланс @{message.from_user.username or "сили"}: {balance[1]}$"
        )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
