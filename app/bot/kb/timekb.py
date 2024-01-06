from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import date, timedelta, datetime
from aiogram.filters.callback_data import CallbackData
from typing import Optional
from emoji import emojize





def timekb(time):
    time_builder = InlineKeyboardBuilder()
    time_builder.button(
        text=f"{emojize(':up_arrow:')} 1 год.", callback_data="+1hour")
    time_builder.button(
        text=f"{emojize(':up_arrow:')} 30 хв.", callback_data="+30min")
    time_builder.button(
        text=f"{emojize(':up_arrow:')} 10 хв.", callback_data="+10min")
    time_builder.button(
        text=f"{emojize(':up_arrow:')} 1 хв.", callback_data="+1min")

    time_builder.button(text=f"{time}", callback_data="set_time")

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
