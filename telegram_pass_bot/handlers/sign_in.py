from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from telegram_pass_bot.db_interactions import get_hash_pass, get_password_hash
from telegram_pass_bot.db_interactions import cur
from telegram_pass_bot.handlers.templates.help_template import HELP_TEXT

router = Router()


class SignIn(StatesGroup):
    awaiting_password = State()
    got_right_pass = State()


def password_check(password_from_user: str, hashed_pass_from_db: int) -> bool:
    hashed_pass_from_user = get_password_hash(password_from_user)
    return hashed_pass_from_user == hashed_pass_from_db


@router.message(Command("sign_in"))
async def handler_pass_await(message: Message, state: FSMContext):

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
async def handler_password_check(message: Message, state: FSMContext):

    user_id = message.from_user.id
    password_from_db = get_hash_pass(cur, user_id)
    data = await state.get_data()
    tries_num = data["tries"]
    password_from_user = message.text

    if password_check(password_from_user, password_from_db):
        await message.answer("Авторизация прошла успешно.")
        await message.answer(HELP_TEXT)
        await state.set_state(SignIn.got_right_pass)
        return

    await message.answer("Неверный пароль.")

    if tries_num >= 3:
        await message.answer("Неудачная авторизация.")
        await message.answer("Для повторной попытки введите "
                             "комманду /sign_in.")
        await state.clear()
        return

    await state.update_data(tries=(tries_num + 1))
