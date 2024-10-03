from config import *
from constants import *
from permission.roles import *
from states.FSMcategory import *

from aiogram.types import *

import json

from datetime import date, timedelta

@dp.message_handler(commands=['start'])
async def start(message:Message):

    with open(f'{DB_LOC}/names.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    ''' проверить на валидность никнейм, чтобы не было смайликов и запрещенных символов '''

    if str(message.chat.id) not in users:
        users[message.chat.id] = f'@{message.chat.username}'

        with open(f'{DB_LOC}/names.json', 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=4)

        with open(f'{DB_LOC}/data.json', 'r', encoding='utf-8') as file:
            data_users = json.load(file)

        data_users[message.chat.id] = {
            "type_user": "user",
            "subscribes": {

            },
            'statistics' : {
                # количество заявок по различным категориям (для категории "разместить объявление")
            },
            "free_sub" : False
        }

        with open(f'{DB_LOC}/data.json', 'w', encoding='utf-8') as file:
            json.dump(data_users, file, ensure_ascii=False, indent=4)

    user_admin = AdminBot.is_admin(message.chat.id)

    await bot.send_message(message.chat.id, TEXT_HELLO, reply_markup=AdminBot.get_keyboard() if\
        user_admin else UserBot.get_keyboard())