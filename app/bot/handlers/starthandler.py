from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from bot.kb.startkb import startkb
from bot.kb.cancelkb import cancelkb
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.callback_answer import CallbackAnswer
from emoji import emojize
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State



class StatesUser(StatesGroup):
    name = State()
    description = State()
    time = State()
    picture = State()
    picture_waiting = State()
    saving = State()


router = Router()
dp = Dispatcher()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привіт!{emojize(':smiling_face_with_smiling_eyes:')} Я гусь-хелпер{emojize(':goose:')} бот, що допоможе тобі написати ідеальний пост! ",
        reply_markup=startkb()
    )
