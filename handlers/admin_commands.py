from config import *
from constants import *
from permission.roles import *
from states.FSMadmins import *
from states.FSMcommon import *

from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import *
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import json

@dp.message_handler(Text(equals='Админка'))
async def administartion(message: Message) -> None:
    if AdminBot.is_admin(message.chat.id):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [
            KeyboardButton('Сообщения'),
            KeyboardButton('Добавить админа'),
            KeyboardButton('Просмотреть заявки'),
            KeyboardButton('Подписчики'),
            KeyboardButton('В главное меню'),
        ]

        keyboard.add(*buttons)
        await message.answer('Это панель администрирования, выберите команды', reply_markup=keyboard)

@dp.message_handler(Text(equals='Сообщения'), state=None)
async def user_requests(message: Message) -> None:

    if AdminBot.is_admin(message.chat.id):
        with open(f'{DB_LOC}/comments.json') as file:
            comments = json.load(file)

        if comments != []:
            for comment in comments:
                await message.answer(f'Пользователь {comment.get("user")} оставил обращение:\n{comment.get("comment")}')

            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Удалить все обращения', callback_data='Удалить'))
            await message.answer('Чтобы удалить все обращения нажмите на кнопку', reply_markup=keyboard)
            await SelectMessages.message.set()
        else:
            await message.answer('Обращения не поступали.')

@dp.callback_query_handler(lambda callback:True, state=SelectMessages.message)
async def delete_all_messages(callback_query: CallbackQuery, state: FSMContext) -> None:
    message = callback_query.message

    data = []
    with open(f'{DB_LOC}/comments.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    await message.answer('Все обращения были удалены')
    await state.finish()

@dp.message_handler(Text(equals='Добавить админа'), state=None)
async def add_admin(message: Message) -> None:
    if AdminBot.is_admin(message.chat.id):
        await message.answer('Чтобы добавить нового админа просто введите его id\nНапример: @user')
        await SetAdmin.admin.set()

@dp.message_handler(state=SetAdmin.admin)
async def creating_admin(message: Message, state: FSMContext) -> None:
    if AdminBot.is_admin(message.chat.id):
        if '@' not in message.text:
            await message.answer('Неверно введен id пользователя')
            return

        with open(f'{DB_LOC}/admins.json', encoding='utf-8') as file:
            admins = json.load(file)

        with open(f'{DB_LOC}/names.json') as file:
            names = json.load(file)

        print(message.text)
        for name in names:
            if names.get(name) == message.text:
                break
        else:
            await message.answer('Пользователь не зарегистрирован в боте')
            await state.finish()
            return

        admins.append(message.text)
        print(admins)

        with open(f'{DB_LOC}/admins.json', 'w') as file:
            json.dump(admins, file, indent=4, ensure_ascii=False)

        await message.answer('Новый админ был успешно добавлен')
        await state.finish()

@dp.callback_query_handler(lambda callback: True, state=SelectAds.ad)
async def vote_request(callback_query: CallbackQuery, state: FSMContext) -> None:
    message = callback_query.message

    with open(f'{DB_LOC}/user_ads.json', encoding='utf-8') as file:
        data = json.load(file)

    with open(f'{DB_LOC}/names.json', encoding='utf-8') as file:
        names = json.load(file)

    user_id = "1244534534"
    if callback_query.data == 'Принять':
        await message.answer('Заявка принята!')
        for name in names:
            if names[name] == data[0].get("user"):
                user_id = name
                break

        try:
            await bot.send_message(int(user_id), f"Ваша заявка по категории {data[0].get('category')} была принята модерацией")
        except Exception as ex:
            ...

    elif callback_query.data == 'Отклонить':
        await message.answer('Заявка отклонена!')
        for name in names:
            if names[name] == data[0].get("user"):
                user_id = name
                break

        try:
            await bot.send_message(int(user_id),
                                   f"Ваша заявка по категории {data[0].get('category')} была отклонена модерацией")
        except Exception as ex:
            ...

    data.pop(0)

    with open(f'{DB_LOC}/user_ads.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    await state.finish()
    await show_requests(message)

@dp.message_handler(Text(equals='Просмотреть заявки'), state=None)
async def show_requests(message: Message) -> None:
    if AdminBot.is_admin(message.chat.id):
        with open(f'{DB_LOC}/user_ads.json', encoding='utf-8') as file:
            ads = json.load(file)

        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton('✅Принять✅', callback_data='Принять'),
            InlineKeyboardButton('❌Отклонить❌', callback_data='Отклонить'),
        ]
        keyboard.add(*buttons)

        if ads == []:
            await message.answer('Все заявки просмотрены!')
            return
        ad = ads[0]
        await message.answer(f'Категория: {ad.get("category")}\nПользователь: {ad.get("user")}\nЗаявка: {ad.get("text")}',
                             reply_markup=keyboard)

        await SelectAds.ad.set()

@dp.message_handler(Text(equals='Подписчики'))
async def show_subscribers(message: Message) -> None:
    if AdminBot.is_admin(message.chat.id):
        with open(f'{DB_LOC}/data.json', encoding='utf-8') as file:
            data = json.load(file)

        with open(f'{DB_LOC}/names.json', encoding='utf-8') as file:
            names = json.load(file)

        list_subs = 'Подписчики:\n'
        subs = 0
        for index, user in enumerate(data):
            if data[user]['subscribes'] != {}:
                subs += 1
                list_subs += f'{subs}. {names[user]} - {len(data[user]["subscribes"])}\n'

        list_subs += f'<b>Общее число - {subs}</b>'

        list_users = 'Зарегистрированные пользователи:\n'
        for index, user in enumerate(names):
            list_users += f'{index + 1}. {names[user]}\n'

        list_users += f'<b>Общее число - {index + 1}</b>'
        await message.answer(list_subs)
        await message.answer(list_users)