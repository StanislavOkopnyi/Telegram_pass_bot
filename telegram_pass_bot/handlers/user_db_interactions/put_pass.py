from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telegram_pass_bot.handlers.sign_in import SignIn
from telegram_pass_bot.db_interactions import cur, con, put_service_pass_in_db


router = Router()


class PutPassInDb(StatesGroup):
    awaiting_service_name = State()
    awaiting_password = State()


@router.message(SignIn.got_right_pass, Command("put_pass"))
async def handler_put_pass(message: Message, state: FSMContext):
    await message.answer("Введите название сервиса:")
    await state.set_state(PutPassInDb.awaiting_service_name)


@router.message(PutPassInDb.awaiting_service_name)
async def handler_service_name(message: Message, state: FSMContext):
    await state.update_data(service_name=message.text)
    await message.answer("Введите пароль для сервиса:")
    await state.set_state(PutPassInDb.awaiting_password)


@router.message(PutPassInDb.awaiting_password)
async def handler_password(message: Message, state: FSMContext):

    data = await state.get_data()
    service_name = data["service_name"]
    password = message.text
    user_id = message.from_user.id
    put_service_pass_in_db(con, cur, user_id, service_name, password)

    await message.answer("Пароль успешно сохранен.")
    await state.set_state(SignIn.got_right_pass)
