from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from telegram_pass_bot.db_interactions import get_hash_pass, put_user_in_db, get_password_hash
from telegram_pass_bot.db_interactions import con, cur

router = Router()


class SignIn(StatesGroup):
    awaiting_password = State()
    got_right_pass = State()


def password_check(password: str, user_and_pass: tuple) -> bool:
    password = get_password_hash(password)
    hashed_pass_from_db = user_and_pass[1]
    return password == hashed_pass_from_db


@router.message(Command("sign_in"))
async def pass_await(message: Message, state: FSMContext):
    user_and_pass = get_hash_pass(cur, message.from_user.id)
    if not user_and_pass:
        await message.answer("Вы еще не зарегистрированы в боте. "
                             "Для регистрации введите комманду /registration.")
        return
    await message.answer("Введите пароль:")
    await state.set_state(SignIn.awaiting_password)
    await state.update_data(tries=0)


@router.message(SignIn.awaiting_password)
async def bot_password_check(message: Message, state: FSMContext):
    user_and_pass = get_hash_pass(cur, message.from_user.id)
    data = await state.get_data()
    tries_num = data["tries"]

    if tries_num >= 3:
        await message.answer("Неудачная авторизация")
        await state.clear()
        return

    if password_check(message.text, user_and_pass):
        await message.answer("Авторизация прошла успешно.")
        await state.set_state(SignIn.got_right_pass)
        return None

    await message.answer("Неверный пароль")
    await state.update_data(tries=(tries_num + 1))
