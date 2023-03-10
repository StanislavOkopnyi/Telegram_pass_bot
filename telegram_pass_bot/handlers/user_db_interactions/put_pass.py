from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telegram_pass_bot.handlers.sign_in import SignIn
from telegram_pass_bot.db_interactions import cur, con, put_service_pass_in_db
from telegram_pass_bot.pass_generator.pass_generator import get_password

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
    service = message.text
    if len(service) > 80:
        await message.answer("Максимально допустимая дл"
                             "ина названия сервиса - 80 символов.")
        return
    await state.update_data(service_name=service)
    await message.answer("Если вы хотите сгенирировать "
                         "пароль введите команду /gen_pass.")
    await message.answer("В ином случае - введите пароль для сервиса:")
    await state.set_state(PutPassInDb.awaiting_password)


@router.message(PutPassInDb.awaiting_password)
async def handler_password(message: Message, state: FSMContext):

    data = await state.get_data()
    service_name = data["service_name"]
    password = message.text
    user_id = message.from_user.id

    if password == "/gen_pass":
        password = get_password()
    put_service_pass_in_db(con, cur, user_id, service_name, password)

    await message.answer(f"Пароль \"{password}\"  успешно сохранен.")
    await state.set_state(SignIn.got_right_pass)
