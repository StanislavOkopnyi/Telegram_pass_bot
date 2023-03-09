from aiogram import Router
from aiogram.types import Message

from telegram_pass_bot.handlers.sign_in import SignIn


router = Router()


@router.message(SignIn.got_right_pass)
async def handler_signed_in(message: Message):
    await message.answer("Список команд, которые "
                         "поддерживает бот можно узнать при помощи - /help.")


@router.message()
async def handler_not_signed_in(message: Message):
    await message.answer("Для регистрации введите команду /registration.")
