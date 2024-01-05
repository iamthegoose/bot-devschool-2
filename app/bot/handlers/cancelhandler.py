from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from bot.kb.startkb import startkb
from bot.kb.cancelkb import cancelkb
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.callback_answer import CallbackAnswer
from random import randint
from emoji import emojize

router = Router()
dp = Dispatcher()


@router.message(F.text == "Скасувати заповнення поста")
async def cancel_press(message: Message):
    await message.answer(
        f"Нам дуже шкода, що ви скасували заповнення поста{emojize(':downcast_face_with_sweat:')} Сподіваємось, що ви спробуєте знову!",
        reply_markup=startkb(),
    )


@router.callback_query()
async def callback_query_handler(callback_query: types.CallbackQuery, bot: Bot):
    if callback_query.data == "start_create_post":
        await bot.send_message(callback_query.from_user.id, text="Hello", reply_markup=cancelkb())
        await callback_query.answer()
