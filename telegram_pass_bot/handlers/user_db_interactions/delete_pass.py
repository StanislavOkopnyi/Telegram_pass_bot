from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telegram_pass_bot.handlers.sign_in import SignIn
from telegram_pass_bot.db_interactions import cur, con,  delete_from_db, delete_all


router = Router()


class DeletePassFromDb(StatesGroup):
    awaiting_service_name = State()


@router.message(SignIn.got_right_pass, Command("delete"))
async def handler_delete_from_db(message: Message, state: FSMContext):
    await message.answer("Введите название сервиса, пароль для которого вы хотите удалить.\n"
                         "Если вы хотите удалить все пароли из бота - введите команду /all.")
    await state.set_state(DeletePassFromDb.awaiting_service_name)


@router.message(DeletePassFromDb.awaiting_service_name)
async def handler_got_service_name_to_delete_from_db(message: Message, state: FSMContext):
    service = message.text
    telegram_id = message.from_user.id
    if service == "/all":
        delete_all(con, cur, telegram_id)
        await message.answer("Все пароли успешно удалены.")
        await state.set_state(SignIn.got_right_pass)
        return
    delete_from_db(con, cur, telegram_id, service)
    await message.answer(f"Пароли для сервиса {service} успешно удалены.")
    await state.set_state(SignIn.got_right_pass)
