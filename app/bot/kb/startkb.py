from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_builder = InlineKeyboardBuilder()
start_builder.add(types.InlineKeyboardButton(
    text="Створити пост",
    callback_data="start_create_post")
)