from config import *
from constants import *

import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.types import *

@dp.message_handler(Text(equals='🤝 Партнерская витрина'))
async def partner_watch(message: Message) -> None:
    with open(f'{DB_LOC}/partners.json', encoding='windows-1251') as file:
        data = json.load(file)

    if len(data) == 0:
        await message.answer('Партнерская витрина пуста!')
        return

    button_link = InlineKeyboardButton('Ссылка на партнера', url=data.get('link'))
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_link)

    await message.answer(f"{data.get('text')}", reply_markup=keyboard)