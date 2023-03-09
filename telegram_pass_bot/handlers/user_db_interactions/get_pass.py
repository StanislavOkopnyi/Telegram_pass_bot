from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telegram_pass_bot.handlers.sign_in import SignIn
from telegram_pass_bot.db_interactions import get_all_passwords, cur, get_service_passwords


router = Router()


class GetOnePass(StatesGroup):
    awaiting_service_name = State()


@router.message(SignIn.got_right_pass, Command("all_pass"))
async def handler_all_passwords(message: Message):

    password_list = get_all_passwords(cur, message.from_user.id)
    password_list = list(
        map(lambda x: f"{x[0]}   --->   {x[1]}", password_list))

    await message.answer(("Список паролей:\n" + "\n".join(password_list)))


@router.message(SignIn.got_right_pass, Command("one_pass"))
async def handler_one_password(message: Message, state: FSMContext):
    await message.answer("Введите название сервиса, пароль к которому вы хотите получить:")
    await state.set_state(GetOnePass.awaiting_service_name)


@router.message(GetOnePass.awaiting_service_name)
async def handler_service_pass_check_return(message: Message, state: FSMContext):
    service = message.text
    user_id = message.from_user.id
    service_passwords = get_service_passwords(cur, user_id, service)
    if service_passwords:
        await message.answer(
            "\n".join([f"{x[1]}   --->   {x[2]}" for x in service_passwords])
        )
        await state.set_state(SignIn.got_right_pass)
        return
    await message.answer("Для этого сервиса пароль не найден.")
    await state.set_state(SignIn.got_right_pass)
