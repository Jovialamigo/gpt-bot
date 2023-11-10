from aiogram import Bot, types


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="start", description="Начать использовать"),
            types.BotCommand(command="chat", description="Выбрать тип чата"),
        ],
    )
