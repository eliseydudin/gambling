from aiogram import Dispatcher, html

from aiogram.filters import CommandStart, Filter, Command
from aiogram.types import Message

from gambling.db import DATABASE

DISPATCHER = Dispatcher()


class DiceFilter(Filter):
    async def __call__(self, message: Message):
        return (
            message.dice is not None
            and message.dice.emoji == "🎰"
            and message.forward_origin is None
        )


@DISPATCHER.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"мяу :3 {html.bold(message.from_user.full_name)}!")


@DISPATCHER.message(DiceFilter())
async def echo_handler(message: Message) -> None:
    id = message.from_user.id
    user = message.from_user.username
    value = (message.dice.value - 33) * 100

    if id in DATABASE:
        DATABASE.set_score(id, value)
    else:
        DATABASE.create_user(id, user)
        DATABASE.set_score(id, value)

    await message.answer(
        f"поздравляю! @{message.from_user.username or "сили"} выиграл {value}$!!!! 🤑🤑🤑"
    )

    # elif message.text and message.text.lower().find("баланс") != -1:
    #     balance = scores.get(message.from_user.id, ("", 0))
    #     await message.answer(
    #         f"баланс @{message.from_user.username or "сили"}: {balance[1]}$"
    #     )


@DISPATCHER.message(Command("balance"))
async def balance(message: Message):
    balance = DATABASE.get_score(message.from_user.id)
    await message.answer(
        f"баланс @{message.from_user.username or "сили"}: {balance[1]}$"
    )
