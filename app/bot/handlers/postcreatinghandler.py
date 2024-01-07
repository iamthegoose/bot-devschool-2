from aiogram import Router, F, types, Bot
from aiogram.types import Message
from bot.kb.startkb import startkb
from bot.kb.cancelkb import cancelkb
from bot.kb.timekb import timekb
from bot.kb.picturedenykb import picturedenykb
from emoji import emojize
from aiogram.fsm.context import FSMContext
from bot.handlers.starthandler import StatesUser
from datetime import date, timedelta, datetime
from utils.time import Time
router = Router()
time = Time()


@router.callback_query()
async def callback_query_handler(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    if callback_query.data == "start_create_post":
        await bot.send_message(callback_query.from_user.id,
                               text=f"Чудово, нумо зануримось у його створення{emojize(':smiling_face_with_smiling_eyes:')} \
                                        \nПридумайте назву вашому посту:",
                               reply_markup=cancelkb())
        await callback_query.answer()
        await state.set_state(StatesUser.name)
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
        await callback_query.message.answer(f"Ви обрали час <b>{time.time.strftime('%H:%M')}</b> \nВкажіть в форматі дд.мм.рррр дату відправлення поста:")
        await callback_query.message.delete()
        await callback_query.answer()
        await state.set_state(StatesUser.time)
    if callback_query.data == "picture_deny":
        await state.update_data(emptyphoto=True)
        await bot.send_message(
            callback_query.from_user.id,
            text="Ви відмовились від завантаження фото для посту!"
        )
        await callback_query.message.delete()
        await process_all_data(callback_query.message, state)
    if callback_query.data == "picture_upload":
        await state.update_data(emptyphoto=False)
        await bot.send_message(
            callback_query.from_user.id,
            text="Завантажте бажане зображення:"

        )
        await callback_query.answer()
        await state.set_state(StatesUser.picture_receiving)


@router.message(StatesUser.name)
async def process_name(message: Message, state: FSMContext) -> None:
    if isinstance(message.text, str):
        await state.update_data(name=message.text)
        await message.answer(
            f"{emojize(':check_mark_button:')} Ваш пост буде мати назву <b>\"{message.text}\"</b>.\nТепер, надайте опис даного посту:",
        )
        await state.set_state(StatesUser.description)
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


@router.message(StatesUser.picture_receiving)
async def picture_receiving(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
        await message.answer(
            "Ваше фото отримане!"
        )
        await process_all_data(message, state)
    else:
        await message.answer(
            "Будь ласка, завантажте фотографію."
        )

async def process_all_data(message: Message, state: FSMContext):
    post_data = await state.get_data()
    name = post_data['name'].upper()
    description = post_data['description']
    post_time = post_data['time']
    data = post_data['chosen_data']
    post = f"<b>{name}</b>\n<i>{description}</i>\n{emojize(':watch:')}Час викладення посту: <b>{post_time}</b>\n{emojize(':calendar:')}Дата викладення посту: <b>{data}</b> "
    await message.answer("Ваш пост має наступний вигляд:")
    if not post_data['emptyphoto']:
        photo = post_data['photo']
        await message.answer_photo(
            photo=photo,
            caption=post,
            reply_markup=startkb()
        )
        await state.clear()
    else:
        await message.answer(text=post, reply_markup=startkb())
        await state.clear()
