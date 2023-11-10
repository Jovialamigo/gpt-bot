from aiogram import Router, types
from aiogram.filters.command import Command

router = Router()


@router.message(Command("start"))
async def command_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! 😃\n"
        f"Воспользуйся командой /chat чтобы начать.\n"
    )
