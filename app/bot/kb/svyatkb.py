from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def svyatkb():
    svyat_keyboard = [
        [
            types.KeyboardButton(text="Скасувати заповнення поста"),
        ],
    ]
    svyatkb = types.ReplyKeyboardMarkup(
        keyboard=svyat_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    return svyatkb