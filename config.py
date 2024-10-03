import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import importlib
import json
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

from constants import *

TOKEN = os.environ.get('TOKEN')
storage = MemoryStorage()

shopApi_id = os.environ.get('shopID')
shopApi_key = os.environ.get('shopKey')

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

apps = [
    'handlers.selecttraffic',
    'handlers.support',
    'handlers.partners',
    'handlers.user_profile',
    'handlers.additional_services',
    'handlers.admin_commands',
    'handlers.safety'
]

for app in apps:
    importlib.import_module(app)

async def update_subs() -> None:
    with open(f'{DB_LOC}/data.json', encoding='utf-8') as file:
        data = json.load(file)

    current_date = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")

    result_data = dict(data).copy()

    # Список для хранения элементов, которые нужно удалить
    items_to_remove = []

    for user in data:
        for sub in data[user]['subscribes']:
            end_date = data[user]['subscribes'][sub]['end_sub'].replace('.', '-')

            if datetime.datetime.strptime(end_date, "%Y-%m-%d") < current_date:
                items_to_remove.append((user, sub))

            if (datetime.datetime.strptime(end_date, "%Y-%m-%d") - current_date).days == 1:
                await bot.send_message(user, f"Ваша подписка на <b>{sub}</b> скоро закончится!\nОбновите подписку, чтобы бот продолжил свою работу")

    # Удаление элементов после завершения итерации
    for user, sub in items_to_remove:
        del result_data[user]['subscribes'][sub]

    with open(f'{DB_LOC}/data.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, ensure_ascii=False, indent=4)


scheduler = AsyncIOScheduler()
scheduler.add_job(update_subs, 'interval', seconds=24 * 60 * 60)

scheduler.start()
