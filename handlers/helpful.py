from constants import *
from config import *
from handlers.selecttraffic import *

from aiogram.dispatcher.filters import Text
from aiogram.types import *

@dp.message_handler(Text(equals='⭐️ Полезное'), state=None)
async def helpful(message: Message) -> None:

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton('Статья по продажам через бота', url='google.com'),
        InlineKeyboardButton('Статья с обзором на бота', url='google.com'),
        InlineKeyboardButton('Информация о боте', callback_data='Информация') # переход к тарифам
    ]

    keyboard.add(*buttons)

    await message.reply('Полезное:', reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'Информация')
async def bot_information(callback_query: CallbackQuery) -> None:
    message = callback_query.message

    await bot.delete_message(message.chat.id, message.message_id)

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton('Оформить подписку', callback_data='Подписка'),
        InlineKeyboardButton('◀️Назад', callback_data='Назад')
    ]

    keyboard.add(*buttons)

    await message.answer('''Бот парсит чаты по ключевым словам и переслывает сообщения от потенциальных клиентов. \nПример: "Ищу таргетолога", "ищу дизайнера" и др. Все что вам остается - это написать человеку на его запрос.\n\nЗаявки берутся из открытых источников, чаты, каналы, а также сторонние сайты.\n\nВ боте есть 11 направлений. По кнопке "Категории заявок" вы можете выбрать нужную категорию. \n\nПодбирать свои ключевые слова пока нельзя. Выбирать можно только из готовых категорий.''', reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: True)
async def exit_info_bot(callback_query: CallbackQuery) -> None:

    message = callback_query.message

    if callback_query.data == 'Назад':
        await message.answer('Операция отменена.')
        return

    await category_queries(message)


