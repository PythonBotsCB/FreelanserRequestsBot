from constants import *
from config import *
from permission.roles import UserBot

from aiogram.dispatcher.filters import Text
from aiogram.types import *
import json

@dp.message_handler(Text(equals='🏢 Личный кабинет'))
async def user_profile(message: Message) -> None:

    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        KeyboardButton('✅ Мои подписки'),
        KeyboardButton('📊 Статистика'),
        KeyboardButton('📋 Гугл таблицы'),
        KeyboardButton('В главное меню'),

    ]

    keyboard.add(*buttons)

    await message.answer('«✅ Мои подписки» -  список твоих активных подписок, приостановка или перенос подписки\n\n«📊 Статистика» - сколько заявок получено от старта подписки\n\n«📋 Гугл таблицы» - выгрузка статистики в гугл таблицу*\n\n*Доступно только при годовой подписке', reply_markup=keyboard)

@dp.message_handler(Text(equals='В главное меню'))
async def backmenu(message: Message) -> None:
    await message.answer(TEXT_HELLO, reply_markup=UserBot.get_keyboard())



@dp.message_handler(Text(equals='📋 Гугл таблицы'))
async def google_sheets(message: Message) -> None:
    ''' Проверяем на наличие у пользователя годовой подписки '''
    await message.answer('Вы можете подключить гугл таблицы для выгрузки статистики отмеченных вами заявок. Для того, чтобы подключить свою таблицу, вам нужно оплатить годовую подписку.')



@dp.message_handler(Text(equals='📊 Статистика'))
async def statistics(message: Message) -> None:
    ''' Выгружаем статистику и проверяем на наличие годовой подписки '''
    await message.answer('Для того, чтобы пользоваться статистикой вам нужно купить годовую подписку')



@dp.message_handler(Text(equals='✅ Мои подписки'))
async def subscribes(message: Message) -> None:
    ''' Читаем файл data.json и показываем подписки '''

    with open(f'{DB_LOC}/data.json', 'r', encoding='utf-8') as file:
        data_users = json.load(file)

    subs_info = data_users.get(str(message.chat.id)).get('subscribes')
    print(subs_info)
    if len(subs_info) == 0:
        await message.answer('Список подписок пуст!')
    else:
        text_answer = 'Ваши подписки:\n'
        for index, sub in enumerate(subs_info):
            string_answer = f'<b>{index + 1}</b>. {sub} ({subs_info.get(sub).get("type_sub")}):\n\tС <b>{subs_info.get(sub).get("start_sub")}</b> по' \
                            f' <b>{subs_info.get(sub).get("end_sub")}</b>\n\n'
            text_answer += string_answer

        await message.answer(text_answer)