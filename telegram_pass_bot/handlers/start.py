from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Этот бот создан для хранения паролей. Для того, "
                         "чтобы зарегистрироваться введите команду "
                         "/registration")


@router.message(Command("stop"))
async def stop_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Состояние бота сброшено")
