from aiogram import Router, F, types, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from bot.kb.startkb import startkb
from bot.kb.cancelkb import cancelkb
from bot.kb.timekb import timekb
from bot.kb.picturedenykb import picturedenykb
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.callback_answer import CallbackAnswer
from random import randint
from emoji import emojize
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.handlers.starthandler import StatesUser
from datetime import date, timedelta, datetime
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
from utils.time import Time
router = Router()
time = Time()


@router.callback_query()
async def callback_query_handler(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    if callback_query.data == "start_create_post":
        await state.set_state(StatesUser.name)
        await bot.send_message(callback_query.from_user.id,
                               text=f"Чудово, нумо зануримось у його створення{emojize(':smiling_face_with_smiling_eyes:')} \
                                        \nПридумайте назву вашому посту:",
                               reply_markup=cancelkb())
        await callback_query.answer()
    if callback_query.data == "+1hour":
        time.time += timedelta(hours=1)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))
    if callback_query.data == "+30min":
        time.time += timedelta(minutes=30)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))
    if callback_query.data == "+10min":
        time.time += timedelta(minutes=10)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))
    if callback_query.data == "+1min":
        time.time += timedelta(minutes=1)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))
    if callback_query.data == "-1hour":
        time.time -= timedelta(hours=1)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))
    if callback_query.data == "-30min":
        time.time -= timedelta(minutes=30)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))
    if callback_query.data == "-10min":
        time.time -= timedelta(minutes=10)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))
    if callback_query.data == "-1min":
        time.time -= timedelta(minutes=1)
        await callback_query.message.edit_reply_markup(reply_markup=timekb(time.time.strftime("%H:%M")))
    if callback_query.data == "set_time":
        await state.update_data(time=time.time.strftime('%H:%M'))
        await callback_query.message.answer(f"Ви обрали час <b>{time.time.strftime('%H:%M')}</b> \nОберіть дату відправлення поста:")
        await state.set_state(StatesUser.time)
        await callback_query.message.delete()
        await callback_query.answer()
    if callback_query.data == "picture_deny":
        await state.set_state(StatesUser.saving)
        await state.update_data(emptyphoto=True)
        await bot.send_message(
            callback_query.from_user.id,
            text="Ви відмовились від завантаження фото для посту!"
        )
        await callback_query.message.delete()
        await callback_query.answer()
    if callback_query.data == "picture_upload":
        await bot.send_message(
            callback_query.from_user.id,
            text="Завантажте бажане зображення:"

        )
        await state.set_state(StatesUser.saving)
        await callback_query.answer()


@router.message(StatesUser.name)
async def process_name(message: Message, state: FSMContext) -> None:
    if isinstance(message.text, str):
        await state.update_data(name=message.text)
        await state.set_state(StatesUser.description)
        await message.answer(
            f"{emojize(':check_mark_button:')} Ваш пост буде мати назву <b>\"{message.text}\"</b>.\nТепер, надайте опис даного посту:",
        )
    elif message.text == "":
        await message.answer(
            f"{emojize(':warning:')} Пост не може не мати назви!"
        )
    else:
        await message.answer(
            f"{emojize(':warning:')} Некоректне заповнення поля, спробуйте ще раз"
        )


@router.message(StatesUser.description, F.text)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.update_data(sender_time=message.date)
    # user_data = await state.get_data()
    await message.answer(text=f"{emojize(':check_mark_button:')} Опис збережено! \nОберіть запланований час для допису",
                         reply_markup=timekb(time.time))
    await state.set_state(StatesUser.time)


def valid_date(date_str):
    try:
        date_user = datetime.strptime(date_str, '%d.%m.%Y')
        if date_user.date() >= date.today():
            return True
    except ValueError:
        return False


@router.message(StatesUser.time)
async def process_time(message: Message, state: FSMContext):
    if valid_date(message.text):
        await state.update_data(chosen_data=message.text)
        await message.answer(
            text=f"Дату успішно збережено! \nПри бажанні, завантажте зображення для посту",
            reply_markup=picturedenykb()
        )
        await state.set_state(StatesUser.picture)
    else:
        await message.answer(
            "Я не розумію наданої вами дати, оскільки вона вже пройшла або записана в неправильному форматі! Спробуйте ще раз в форматі дд.мм.рррр!"
        )


@router.message(StatesUser.saving, F.photo)
async def process_all_data(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id, emptyphoto=False)
    post_data = await state.get_data()
    name = post_data['name'].upper()
    description = post_data['description']
    post_time = post_data['time']
    data = post_data['chosen_data']
    post = f"<b>{name}</b>\n<i>{description}</i>\n{emojize(':three_oclock:')}Час викладення посту: <b>{post_time}</b>\n{emojize(':calendar:')}Дата викладення посту: <b>{data}</b> "
    await message.answer("Ваш пост має наступний вигляд:")
    if not post_data['emptyphoto']:
        photo = post_data['photo']
        await message.answer_photo(
            photo=photo,
            caption=post
        )
        await state.clear()
    else:
        await message.answer(text=post)


@router.message(StatesUser.saving)
async def sent_picture(message: Message, state: FSMContext):
    await message.answer(
        "Будь ласка, завантажте фотографію."
    )
