from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telegram_pass_bot.db_interactions import get_hash_pass, put_user_in_db
from telegram_pass_bot.db_interactions import con, cur

router = Router()


class RegistrationState(StatesGroup):
    password = State()


@router.message(Command("registration"))
async def handler_registration(message: Message, state: FSMContext):

    user_and_pass = get_hash_pass(cur, message.from_user.id)

    if user_and_pass:
        await message.answer("Вы уже зарегистрированы.")
        await message.answer("Для авторизации введите команду /sign_in.")
        return

    await message.answer("Если вы хотите сгенерировать "
                         "пароль для вашего аккаунта "
                         "введите команду /generate.")
    await message.answer("В ином случае - введите "
                         "пароль для вашего аккаунта в боте:")
    await state.set_state(RegistrationState.password)


@router.message(RegistrationState.password)
async def handler_password_saving(message: Message, state: FSMContext):

    password = message.text
    put_user_in_db(con, cur, message.from_user.id, password)

    await message.answer("Пароль сохранен")
    await message.answer("Для авторизации введите команду - /sign_in.")
    await state.clear()
