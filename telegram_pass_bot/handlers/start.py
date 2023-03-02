from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=["start"]))
async def start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Этот бот создан для хранения паролей. Для того, "
                         "чтобы зарегистрироваться введите команду "
                         "/registration")
