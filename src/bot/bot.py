from aiogram import Bot
from aiogram.types.message import Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import Dispatcher

from decouple import config
from .keyboards import get_sites_kb, get_response_data_kb, get_site_data_kb

from src.database.tables import Sites, Answers
from pony.orm import db_session, select

from .form import text_form

bot = Bot(token=config('token'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(e: Message):
    sites = select(s.name for s in Sites
                   if e.from_user.id in s.users)
    if sites:
        return await e.answer("Выберите бриф", reply_markup=get_sites_kb(sites))
    return await e.answer("Ваш список сайтов пуст")


@dp.message_handler(commands=['add'])
async def add(e: Message):
    site_info = e.text.split(" ")
    if len(site_info) < 4:
        return await e.answer('Вы забыли ввести параметр')

    if not select(s for s in Sites if s.name == site_info[1]):
        Sites(
            name=site_info[1],
            address=site_info[2],
            password=site_info[3],
            users=[]
        )
        return await e.answer("Сайт был добавлен")

    return await e.answer('Сайт уже добавлен')


@dp.message_handler(commands=['remove'])
async def remove(e: Message):
    if len(e.text.split(' ')) < 2:
        return await e.answer('Вы забыли аргумент')

    s = select(s for s in Sites if s.name == e.text.split(' ')[1]).first()
    if s:
        users = s.users
        s.delete()
        await e.answer("Сайт был успешно удалён")
        for u in users:
            sites = select(s.name for s in Sites
                           if e.from_user.id in s.users)
            await bot.send_message(u, 'Список сайтов был обновлён',
                                   reply_markup=get_sites_kb(sites))
    else:
        await e.answer('Сайта не существует')


@dp.message_handler(commands=['auth'])
async def auth(e: Message):
    params = e.text.split(' ')
    if len(params) < 3:
        return await e.answer('Один из параметров не введён')
    ans = select(s.password for s in Sites if s.name == params[1])

    if params[2] != ans.first():
        return await e.answer('один из параметров введён неверно')

    s = select(s for s in Sites if s.name == params[1]).first()
    s.users.append(e.from_user.id)
    await e.answer('вы успешно авторизовались')

    sites = select(s.name for s in Sites
                   if e.from_user.id in s.users)
    await e.answer('Список сайтов был обновлён',
                   reply_markup=get_sites_kb(sites))


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith('response')
)
async def get_answer_list(e: CallbackQuery):
    responses = select(a for a in Answers
                       if a.site_name == e.data.split("_")[2]
                       and a.typ == e.data.split("_")[1])
    if responses:
        await bot.send_message(e.from_user.id, 'Список заявок')

        for response in responses:
            await bot.send_message(
                e.from_user.id, text_form(response.data),
                reply_markup=get_response_data_kb(response.id)
            )
    else:
        await bot.answer_callback_query(e.id, "Список заявок пуст", show_alert=True)


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith('set_answer')
)
async def set_answer_type(e: CallbackQuery):
    with db_session:
        Answers[int(e.data.split("_")[2])].typ = "answered"
    await e.answer("Вы отметили заявку отвеченной", show_alert=True)


@dp.message_handler()
async def site_get(e: Message):
    if not e.text.startswith('/') and e.text in select(s.name for s in Sites):
        return await e.answer('Просмотреть заявки', reply_markup=get_site_data_kb(e.text))
    return await e.answer('Такого сайта не существует')
