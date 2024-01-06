import asyncio
import logging
import sys
from settings import settings
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot.kb.startkb import startkb
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.handlers import starthandler, cancelhandler, postcreatinghandler
from emoji import emojize
dp = Dispatcher()
bot = Bot(token=settings.TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
router = Router()

logging.basicConfig(level=logging.INFO)
dp.include_routers(
    starthandler.router,
    cancelhandler.router,
    postcreatinghandler.router,
)



async def main() -> None:
    await dp.start_polling(bot, drop_pending_updates=True)
if __name__ == "__main__":
    asyncio.run(main())
