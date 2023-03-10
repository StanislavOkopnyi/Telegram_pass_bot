from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from telegram_pass_bot.handlers.sign_in import SignIn
from telegram_pass_bot.handlers.templates.help_template import HELP_TEXT

router = Router()


@router.message(SignIn.got_right_pass, Command("help"))
async def handler_help(message: Message):
    await message.answer(HELP_TEXT)
