from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from telegram_pass_bot.handlers.sign_in import SignIn
from telegram_pass_bot.handlers.user_db_interactions.delete_pass import DeletePassFromDb
from telegram_pass_bot.handlers.user_db_interactions.get_pass import GetOnePass
from telegram_pass_bot.handlers.user_db_interactions.put_pass import PutPassInDb

router = Router()

authorized_states = [SignIn.got_right_pass, DeletePassFromDb.awaiting_service_name,
                     PutPassInDb.awaiting_service_name, PutPassInDb.awaiting_password,
                     GetOnePass.awaiting_service_name]


@router.message(Command("start"))
async def handler_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Этот бот создан для хранения паролей. Для того, "
                         "чтобы зарегистрироваться введите команду "
                         "/registration.")


@router.message(Command("stop"))
async def handler_stop(message: Message, state: FSMContext):
    state_to_check = await state.get_state()
    if state_to_check not in authorized_states:
        await state.clear()
        await message.answer("Состояние бота сброшено.")
        return
    await state.set_state(SignIn.got_right_pass)
    await message.answer("Состояние бота сброшено.")


@router.message(Command("sign_out"))
async def handler_log_out(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы успешно вышли из аккаунта.")
