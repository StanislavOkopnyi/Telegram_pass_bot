import asyncio
import logging
from telegram_pass_bot.handlers import start, registration, sign_in
from telegram_pass_bot.handlers import help_router
from telegram_pass_bot.handlers.user_db_interactions import put_pass, get_pass
from telegram_pass_bot.handlers.user_db_interactions import delete_pass
from aiogram import Bot, Dispatcher
from telegram_pass_bot.bot_token import TOKEN


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(sign_in.router)
    dp.include_router(put_pass.router)
    dp.include_router(get_pass.router)
    dp.include_router(delete_pass.router)
    dp.include_router(help_router.router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
