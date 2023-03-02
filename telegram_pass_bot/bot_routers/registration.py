from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telegram_pass_bot.db_interactions.db_get_data import get_hash_pass
from telegram_pass_bot.db_interactions.db_put_data import put_user_in_db
from telegram_pass_bot.main import con, cur
import zlib

router = Router()


class RegistrationState(StatesGroup):
    password = State()


@router.message(Command("registration"))
async def registration_handler(message: Message, state: FSMContext):
    password = get_hash_pass(cur, message.from_user.id)
    if password is not None:
        await message.answer("Вы уже зарегистрированы.")
    await message.answer("Введите пароль для вашего аккаунта в боте:")
    await state.set_state(RegistrationState.password)


@router.message(RegistrationState.password)
async def password_saving(message: Message, state: FSMContext):
    hash_password = zlib.crc32(bytes(message.text))
    put_user_in_db(con, cur, message.from_user.id, hash_password)
    await message.answer("Пароль сохранен")
