from aiogram import Router, F, types, Bot   
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from bot.kb.startkb import startkb
from bot.kb.cancelkb import cancelkb
from bot.kb.timekb import timekb, CallbackTime
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.callback_answer import CallbackAnswer
from random import randint
from emoji import emojize
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.handlers.starthandler import StatesUser
from datetime import date, timedelta, datetime
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
from utils.time import Time
router = Router()
time = Time()

# class StatesUser(StatesGroup):
#     name = State()
#     description = State()
#     time = State()
#     calendar = State()
#     picture = State()
#     saving = State()


@router.callback_query()
async def callback_query_handler(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    if callback_query.data == "start_create_post":
        await state.set_state(StatesUser.name)
        await bot.send_message(callback_query.from_user.id,
                               text=f"Чудово, нумо зануримось у його створення{emojize(':smiling_face_with_smiling_eyes:')} \
                                        \nПридумайте назву вашому посту:",
                               reply_markup=cancelkb())
        await callback_query.answer()
    if callback_query.data == "+1hour":
        time.time += timedelta(hours=1)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))


@router.message(StatesUser.name)
async def process_name(message: Message, state: FSMContext) -> None:
    if isinstance(message.text, str):
        await state.update_data(name=message.text)
        await state.set_state(StatesUser.description)
        await message.answer(
            f"{emojize(':check_mark_button:')} Ваш пост буде мати назву <b>\"{message.text}\"</b>.\nТепер, надайте опис даного посту:",
        )
    elif message.text == "":
        await message.answer(
            f"{emojize(':warning:')} Пост не може не мати назви!"
        )
    else:
        await message.answer(
            f"{emojize(':warning:')} Некоректне заповнення поля, спробуйте ще раз"
        )



@router.message(StatesUser.description, F.text)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(chosen_description=message.text)
    await state.update_data(sender_time=message.date)
    user_data = await state.get_data()
    await message.answer(text="Оберіть запланований час для допису",
                         reply_markup=timekb(user_data['sender_time']))
    await state.set_state(StatesUser.time)



