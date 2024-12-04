from aiogram import Dispatcher, html

from aiogram.filters import CommandStart, Filter, Command
from aiogram.types import Message

from db import DATABASE
from random import choices, randint

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
    await message.reply_dice("🎰")


@DISPATCHER.message(DiceFilter())
async def echo_handler(message: Message) -> None:
    id = message.from_user.id
    user = message.from_user.username
    value = (message.dice.value - 33) * 100
    value += randint(-10, 10) * 100

    modifier = choices([1, 2, 3, 5, 10, 100], [100, 30, 20, 10, 5, 1])[0]
    if user == "eliseydudin":
        modifier = choices([1, 2, 3, 5, 10, 100], [20, 10, 5, 1, 6, 10])[0]
        value = abs(value)

    modmessage = ""
    if modifier != 1:
        modmessage = f"модификатор: {modifier}🔥"
        value *= modifier
    elif modifier >= 10 and value == 0:
        value = 999999
        modmessage = "НЕВЕРОЯТНЫЙ КУШ ‼️‼️‼️‼️ +ГАЗИЛЛИОН ДОЛЛАРОВ"

    if id in DATABASE:
        DATABASE.set_score(id, DATABASE.get_score(id) + value)
    else:
        DATABASE.create_user(id, user)
        DATABASE.set_score(id, value)

    await message.answer(
        f"поздравляю! @{message.from_user.username or "сили"} выиграл {value}$!!!! 🤑🤑🤑\n{modmessage}"
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
        f"баланс @{message.from_user.username or "сили"}: {balance or 0}$"
    )


@DISPATCHER.message(Command("top"))
async def top(message: Message):
    t = DATABASE.get_top_five()
    to_send = "топ игроков 🔥:\n"
    for i, topster in enumerate(t):
        to_send += f"{i + 1}. @{topster[0] or "сили"} {topster[1]}$\n"

    await message.answer(to_send)


@DISPATCHER.message(Command("bottom"))
async def bottom(message: Message):
    t = DATABASE.get_bottom_five()
    to_send = "(анти)топ игроков 🔥:\n"
    for i, topster in enumerate(t):
        to_send += f"{i + 1}. @{topster[0] or "сили"} {topster[1]}$\n"

    await message.answer(to_send)
