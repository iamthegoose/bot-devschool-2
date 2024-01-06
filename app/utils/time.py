from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import date, timedelta, datetime
from aiogram.filters.callback_data import CallbackData
from typing import Optional
from emoji import emojize


class Time:
    time = (datetime.now())