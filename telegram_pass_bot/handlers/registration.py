from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telegram_pass_bot.db_interactions import get_hash_pass, put_user_in_db, get_password_hash
from telegram_pass_bot.db_interactions import con, cur
import zlib

router = Router()


class RegistrationState(StatesGroup):
    password = State()


@router.message(Command("registration"))
async def registration_handler(message: Message, state: FSMContext):
    user_and_pass = get_hash_pass(cur, message.from_user.id)
    if user_and_pass:
        await message.answer("Вы уже зарегистрированы.")
        return
    await message.answer("Введите пароль для вашего аккаунта в боте:")
    await state.set_state(RegistrationState.password)


@router.message(RegistrationState.password)
async def password_saving(message: Message, state: FSMContext):
    hash_password = get_password_hash(message.text)
    put_user_in_db(con, cur, message.from_user.id, hash_password)
    await message.answer("Пароль сохранен")
    await state.clear()
