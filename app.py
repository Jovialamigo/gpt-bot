import asyncio
import logging

from handlers import chat, start
from loader import bot, dp

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
)


async def on_startup(bot):
    from utils.set_bot_commands import set_default_commands

    await set_default_commands(bot)
    logging.info("Бот запущен")


async def main():
    dp.include_routers(
        start.router,
        chat.router,
    )
    await dp.start_polling(bot, on_startup=await on_startup(bot))


if __name__ == "__main__":
    asyncio.run(main())
