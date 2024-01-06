from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def cancelkb():
    cancel_keyboard = [
        [
            types.KeyboardButton(text="Скасувати заповнення поста"),
        ],
    ]
    cancelkb = types.ReplyKeyboardMarkup(
        keyboard=cancel_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    return cancelkb
