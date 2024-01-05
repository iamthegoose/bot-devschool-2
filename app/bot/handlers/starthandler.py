from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from bot.kb.startkb import start_builder
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from random import randint
from emoji import emojize

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привіт!{emojize(':smiling_face_with_smiling_eyes:')} Я гусь-хелпер{emojize(':goose:')} бот, що допоможе тобі написати ідеальний пост! ",
        reply_markup=start_builder.as_markup(),
    )

@router.message.register(F.data == "start_create_post")
async def start_create_post(callback: CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer()
