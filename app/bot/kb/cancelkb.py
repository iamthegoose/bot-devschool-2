from aiogram import types

cancelkb = [
    [
        types.KeyboardButton(text="Скасувати заповнення поста"),
    ],
]
cancel_keyboard = types.ReplyKeyboardMarkup(
    keyboard=cancelkb,
    resize_keyboard=True,
    input_field_placeholder="Выберите способ подачи"
)