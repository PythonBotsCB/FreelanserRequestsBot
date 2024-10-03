from aiogram.types import *
from states.FSMcategory import *
from config import *
from constants import *
from permission.roles import *
from items import *
from subscribes import *
from payments import *

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import json

@dp.message_handler(Text(equals='🙋‍♂️ Заявки на услугу'), state=None)
async def category_queries(message: Message) -> None:

    keyboard = InlineKeyboardMarkup()

    for category in CATEGORY_BUTTONS:
        keyboard.add(InlineKeyboardButton(category, callback_data=category))

    await message.reply('<b><i>Здесь вы можете выбрать услугу на которую вам нужны заявки</i></b>\n\nПодписка на бота даст вам посстоянный поток и неограниченный поток заявок с различных чатов и площадок на ваши услуги\n\nВыбери категорию:', reply_markup=keyboard)
    await SelectCategory.category.set()

@dp.message_handler(state=SelectCategory.category)
async def cancel_request(message: Message, state: FSMContext) -> None:
    await message.answer('Операция выбора заявки была прервана!')
    await state.finish()

@dp.callback_query_handler(lambda callback_query: True, state=SelectCategory.category)
async def select_category(callback_query: types.CallbackQuery, state: FSMContext) -> None:

    message = callback_query.message

    await bot.delete_message(message.chat.id, message.message_id)

    category = callback_query.data
    await callback_query.answer(category)
    await state.update_data(category=category)

    prices = Prices(category).get_prices()

    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(f'12 мес. {prices.get(365)} р', callback_data=f'12 мес. {prices.get(365)} р'),
        InlineKeyboardButton(f'6 мес. {prices.get(180)} р', callback_data=f'6 мес. {prices.get(180)} р'),
        InlineKeyboardButton(f'3 мес. {prices.get(90)} р', callback_data=f'3 мес. {prices.get(90)} р'),
        InlineKeyboardButton(f'1 мес. {prices.get(30)} р', callback_data=f'1 мес. {prices.get(30)} р'),
        InlineKeyboardButton(f'1 неделя {prices.get(7)} р', callback_data=f'1 неделя {prices.get(7)} р'),
        InlineKeyboardButton(f'1 день {prices.get(1)} р', callback_data=f'1 день {prices.get(1)} р'),
        InlineKeyboardButton('Пробный период на три дня', callback_data='Пробный период на три дня'),
        InlineKeyboardButton('◀️Назад', callback_data='◀️Назад')
    ]

    # сообщение с кнопками
    for button in buttons:
        keyboard.add(button)

    await callback_query.message.answer('''При оплате из других стран (не РФ) или через криптовалюту пишите на аккаунт @COJ_ZhIV\nПри оплате годового тарифа консультация по продажам с создателем бота - в подарок.\nВыберите период:''', reply_markup=keyboard)
    await SelectCategory.next()

@dp.callback_query_handler(lambda callback_query: True, state=SelectCategory.traffic)
async def select_traffic(callback_query: types.CallbackQuery, state: FSMContext) -> None:

    traffic = callback_query.data
    message = callback_query.message

    await bot.delete_message(message.chat.id, message.message_id)

    if traffic == '◀️Назад':
        await state.finish()
        await message.answer('Операция прервана.')
        return


    await state.update_data(traffic=traffic)
    data = await state.get_data()

    category = data.get("category")

    # получаем количество дней
    # days = CONVERT_MONTH.get(int(traffic.split()[0]))

    if traffic != 'Пробный период на три дня':

        date_type = ' '.join([traffic.split()[0], traffic.split()[1]]) # 1 день, 1 мес.
        days = CONVERT_MONTH.get(date_type)
        price = PRICE.get(days)

        await state.update_data(days=days, price=price)

        url, payment_check = create_payment(price, f'Подписка на {traffic.split()[0] + " " + traffic.split()[1]}. Категория: {category}')

        keyboard = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton('Оплатить', url=url),
            InlineKeyboardButton('✅Оплатил✅', callback_data=payment_check),
            InlineKeyboardButton('◀️Назад', callback_data='Назад')
        ]

        keyboard.add(*buttons)

        await callback_query.answer(traffic)

    if traffic == 'Пробный период на три дня':
        '''проверка на наличие бесплатного тарифа для клиента'''

        with open(f'{DB_LOC}/data.json', 'r', encoding='utf-8') as file:
            data_users = json.load(file)

        if not data_users[str(message.chat.id)]['free_sub']:
            await message.answer('Вы выбрали пробный период')
            data = await state.get_data()
            print(data)
            data['days'] = 3

            subs = Subscribe(data.get('traffic'), data.get('days'))

            data_users[str(message.chat.id)]['subscribes'][data.get('category')] = subs.get_info()
            data_users[str(message.chat.id)]['free_sub'] = True
            print(data.get('traffic'), subs.get_info())

            with open(f'{DB_LOC}/data.json', 'w', encoding='utf-8') as file:
                json.dump(data_users, file, indent=4, ensure_ascii=False)

            await state.finish()
        else:

            await message.answer('Тестовый период уже был использовал!')
            await state.finish()
    else:
        ''' Проверка на тариф '''
        await message.answer(f'''Вы выбрали тариф на <b>{days}</b> дней (категория <b>{category}</b>), стоимость: <b>{Prices(category).get_needprice(CONVERT_MONTH.get(date_type))}</b> руб.''', reply_markup=keyboard)
        await SelectCategory.next()

@dp.callback_query_handler(lambda callback_query: True, state=SelectCategory.paid)
async def buy_or_bought(callback_query: types.CallbackQuery, state: FSMContext) -> None:

    message = callback_query.message

    if callback_query.data == 'Назад':
        await bot.delete_message(message.chat.id, message.message_id)
        await state.finish()
        await message.answer('Операция прервана!')
        return

    if check_payment(callback_query.data):

        paid = callback_query.data

        data = await state.get_data()

        await message.answer('Оплата проведена успешно!')

        with open(f'{DB_LOC}/data.json', 'r', encoding='utf-8') as file:
            data_users = json.load(file)

        subs = Subscribe(data.get('traffic'), data.get('days'))

        data_users[str(message.chat.id)]['subscribes'][data.get('category')] = subs.get_info()
        print(data.get('traffic'), subs.get_info())

        with open(f'{DB_LOC}/data.json', 'w', encoding='utf-8') as file:
            json.dump(data_users, file, indent=4, ensure_ascii=False)

        await state.finish()

        #TODO: нужно обработать запрос покупки
    else:
        await message.answer('Платеж не прошел')