from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from emoji import emojize


def picturedenykb():
    picturedeny_builder = InlineKeyboardBuilder()
    picturedeny_builder.add(types.InlineKeyboardButton(
        text=f"{emojize(':cross_mark: ')}Відмовитись від завантаження",
        callback_data="picture_deny")
    )
    picturedeny_builder.add(types.InlineKeyboardButton(
        text=f"{emojize(':up_arrow:')}Завантажити зображення",
        callback_data="picture_upload")
    )
    return picturedeny_builder.as_markup()
