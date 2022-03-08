from aiogram import Dispatcher, types, Bot
from src.bot.bot import bot, dp

from decouple import config

from fastapi import FastAPI, Request
from pydantic import Json
from .models.Answers import DataAnswers, AnswersInDB
from src.database.tables import Answers, Sites
from pony.orm import db_session, select

app = FastAPI()
WEBHOOK_PATH = f'/bot/{config("token")}'
WEBHOOK_URL = 'https://b7dd-94-125-242-193.ngrok.io' + WEBHOOK_PATH


@app.get("/")
async def read_root():
    return 'hello, backend work on fastapi!'


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.get("/briefs")
async def read_item(data: str, r: Request):
    url = r.url.url.split('/')[2]
    answer = AnswersInDB.parse_raw(data)
    with db_session:
        if select(s for s in Sites
                  if s.name == answer.site_name
                  and s.address == url):
            Answers(
                site_name=answer.site_name,
                data=answer.data.json(),
                typ=answer.typ
            )
        else:
            return {'error': 'invalid values'}
    if answer.data:
        return answer
