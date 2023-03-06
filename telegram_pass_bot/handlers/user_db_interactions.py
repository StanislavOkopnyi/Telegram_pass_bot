from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telegram_pass_bot.handlers.sign_in import SignIn
from telegram_pass_bot.db_interactions import get_all_passwords, cur, con, put_service_pass_in_db, get_service_passwords, delete_from_db, delete_all


router = Router()


class PutPassInDb(StatesGroup):
    awaiting_service_name = State()
    awaiting_password = State()


class GetOnePass(StatesGroup):
    awaiting_service_name = State()


class DeletePassFromDb(StatesGroup):
    awaiting_service_name = State()


@router.message(SignIn.got_right_pass, Command("all_pass"))
async def handler_all_passwords(message: Message):

    password_list = get_all_passwords(cur, message.from_user.id)
    password_list = list(map(lambda x: f"{x[0]} --> {x[1]}", password_list))

    await message.answer(("Список паролей:\n" + "\n".join(password_list)))


@router.message(SignIn.got_right_pass, Command("one_pass"))
async def handler_one_password(message: Message, state: FSMContext):
    await message.answer("Введите название сервиса, пароль к которому вы хотите получить:")
    await state.set_state(GetOnePass.awaiting_service_name)


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


@router.message(GetOnePass.awaiting_service_name)
async def handler_service_pass_check_return(message: Message, state: FSMContext):
    service = message.text
    user_id = message.from_user.id
    service_passwords = get_service_passwords(cur, user_id, service)
    if service_passwords:
        await message.answer(
            "\n".join([f"{x[1]} --> {x[2]}" for x in service_passwords])
        )
        await state.set_state(SignIn.got_right_pass)
        return
    await message.answer("Для этого сервиса нет пароля")
    await state.set_state(SignIn.got_right_pass)


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
