from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import data, timedelta

def startkb():
    start_builder = InlineKeyboardBuilder()
    start_builder.add(types.InlineKeyboardButton(
        text="Створити пост",
        callback_data="start_create_post")
    )
    return start_builder.as_markup()
