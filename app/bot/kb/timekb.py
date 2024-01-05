from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import date, timedelta
from aiogram.filters.callback_data import CallbackData
from typing import Optional
from emoji import emojize

class CallbackTime(CallbackData, prefix="timeset"):
    value: Optional[timedelta] = None
    action: str


def timekb(data: date):

    time_builder = InlineKeyboardBuilder()
    time_builder.button(
        text=f"{emojize(':up_arrow:')} 1 год.", callback_data="+1hour")
    time_builder.button(
        text=f"{emojize(':up_arrow:')} 30 хв.", callback_data="+30min")
    time_builder.button(
        text=f"{emojize(':up_arrow:')} 10 хв.", callback_data="+10min")
    time_builder.button(
        text=f"{emojize(':up_arrow:')} 1 хв.", callback_data="+1min")

    time_builder.button(text=f"{data}", callback_data="set_time")

    time_builder.button(
        text=f"{emojize(':down_arrow:')} 1 год.", callback_data="-1hour")
    time_builder.button(
        text=f"{emojize(':down_arrow:')} 30 хв.", callback_data="-30min")
    time_builder.button(
        text=f"{emojize(':down_arrow:')} 10 хв.", callback_data="-10min")
    time_builder.button(
        text=f"{emojize(':down_arrow:')} 1 хв.", callback_data="-1min")

    time_builder.adjust(4, 1, 4)
    return time_builder.as_markup()
