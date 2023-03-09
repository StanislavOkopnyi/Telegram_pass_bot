from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from telegram_pass_bot.handlers.sign_in import SignIn
from telegram_pass_bot.handlers.templates.help_template import help_text

router = Router()


@router.message(SignIn.got_right_pass, Command("help"))
async def handler_help(message: Message):
    await message.answer(help_text)
