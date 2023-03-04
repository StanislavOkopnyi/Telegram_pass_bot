from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from telegram_pass_bot.db_interactions import get_hash_pass, get_password_hash
from telegram_pass_bot.db_interactions import cur

router = Router()


class SignIn(StatesGroup):
    awaiting_password = State()
    got_right_pass = State()


def password_check(password: str, hashed_password: str) -> bool:
    password = get_password_hash(password)
    hashed_pass_from_db = hashed_password
    return password == hashed_pass_from_db


@router.message(Command("sign_in"))
async def pass_await(message: Message, state: FSMContext):

    user_id = message.from_user.id
    password = get_hash_pass(cur, user_id)

    if not password:
        await message.answer("Вы еще не зарегистрированы в боте. "
                             "Для регистрации введите комманду /registration.")
        return

    await message.answer("Введите пароль:")
    await state.set_state(SignIn.awaiting_password)
    await state.update_data(tries=1)


@router.message(SignIn.awaiting_password)
async def bot_password_check(message: Message, state: FSMContext):

    user_id = message.from_user.id
    password = get_hash_pass(cur, user_id)
    data = await state.get_data()
    tries_num = data["tries"]
    message_text = message.text

    if password_check(message_text, password):
        await message.answer("Авторизация прошла успешно.")
        await state.set_state(SignIn.got_right_pass)
        return

    await message.answer("Неверный пароль")

    if tries_num >= 3:
        await message.answer("Неудачная авторизация")
        await state.clear()
        return

    await state.update_data(tries=(tries_num + 1))
