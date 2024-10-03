from constants import *
from config import *
from states.FSMad_user import *
from permission.roles import UserBot

from aiogram.dispatcher.filters import Text
from aiogram.types import *
from aiogram.dispatcher import FSMContext
import json

@dp.message_handler(Text(equals='🏮 Доп. Функции'))
async def additional_services(message: Message) -> None:
    ''' ➕ Доп услуги '''

    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        KeyboardButton('⬆️ Разместить объявление'),
        KeyboardButton('➕ Добавить чат'),
        KeyboardButton('📝Заказать направление'),
        KeyboardButton('Реклама в боте 💸'),
        KeyboardButton('В главное меню'),
    ]

    keyboard.add(*buttons)

    await message.reply('«⬆️ Найти специалиста» - разместить объявление в боте о поиске специалиста\n\n«➕ Добавить чат» - добавление в бота чата для дальнейших пересылок сообщений из него.\n\n«📝 Заказать новое направление» - если вашего направления нет в "Категории заявок", то можете заказать его разработку', reply_markup=keyboard)

@dp.message_handler(Text(equals='⬆️ Разместить объявление'), state=None)
async def set_ad(message: Message) -> None:
    ''' Машина состояния и заполнение заявки '''
    # TODO: Дальнейшая обработка будет через callback_query

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(name, callback_data=name) for name in CATEGORY_BUTTONS]
    keyboard.add(*buttons)

    await message.reply('Выберите категорию вашей заявки', reply_markup=keyboard)
    await SetAd.category.set()


@dp.callback_query_handler(lambda callback: True, state=SetAd.category)
async def write_ad(callback_query: CallbackQuery, state: FSMContext) -> None:
    message = callback_query.message

    await state.update_data(category=callback_query.data)
    await message.answer(f'Вы выбрали категорию {callback_query.data}. Теперь пришлите вашу заявку, мы выложим её в нашем боте после проверки модераторами. ВАЖНО! Мы не публикуем рекламные посты про специалиста; если вы ищете клиентов, то активируйте бота и получайте заявки. Объявления по типу: Я таргетолог, помогу настроить рекламу и тому подобное не публикуются!\n(/cancel для отмены)')
    await SetAd.next()

@dp.message_handler(state=SetAd.text_request)
async def save_ad(message: Message, state: FSMContext) -> None:

    if message.text == '/cancel':
        await message.answer('Операция прервана')
        await state.finish()

        return

    await message.answer('Заявка успешно сохранена, если модерация одобрит заявку, то вам придет уведомление')

    await state.update_data(text=message.text)
    data = await state.get_data()

    with open(f'{DB_LOC}/user_ads.json', encoding='utf-8') as file:
        all_ads = json.load(file)
        all_ads.append({
            "user" : "@" + message.from_user.username,
            "text" : data.get('text'),
            "category" : data.get('category')
        })
    with open(f'{DB_LOC}/user_ads.json', 'w', encoding='utf-8') as file:
        json.dump(all_ads, file, ensure_ascii=False, indent=4)

    with open(f'{DB_LOC}/admins.json', encoding='utf-8') as file:
        admins = json.load(file)

    with open(f'{DB_LOC}/names.json', encoding='utf-8') as file:
        names = json.load(file)

    for name in names:
        if names[name] in admins:

            await bot.send_message(name, 'Появилось новое обращение по объявлению, проверьте через команду "Админка"')


    await state.finish()


@dp.message_handler(Text(equals='➕ Добавить чат'), state=None)
async def add_to_chat(message: Message) -> None:

    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton('Пригласить аккаунт', callback_data='Пригласить аккаунт'),
        InlineKeyboardButton('Отправить ссылку', callback_data='Отправить ссылку')
    ]
    keyboard.add(*buttons)

    await message.reply('Чтобы добавить чат, из которого, возможно, в будущем мы будем пересылать заявки, вы можете либо пригласить в него наш специальный аккаунт, либо отправить нам ссылку на чат.\nВыберите действие:', reply_markup=keyboard)

@dp.message_handler(Text(equals='📝Заказать направление'))
async def order_direction(message: Message) -> None:
    await message.reply('Если твоего направления нет в "Категории заявок", то можешь его заказать. Стоимость 5000 руб, это предоплата за 3 месяца работы бота. Запуск в течение недели. Если все устраивает пиши свое направление мне в лс @COJ_ZhIV')

@dp.message_handler(Text(equals='Реклама в боте 💸'))
async def buy_advertising(message: Message) -> None:
    await message.reply('Вы можете узнать актуальные цены на рекламу в боте через https://t.me/+2Grf99Dpkf4zM2Zi')





