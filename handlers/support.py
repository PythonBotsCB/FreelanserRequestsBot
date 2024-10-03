from constants import *
from config import *
from states.FSMsupport import *
from permission.roles import *

from aiogram.dispatcher.filters import Text
from aiogram.types import *
from aiogram.dispatcher import FSMContext
import json

@dp.message_handler(Text(equals='⚙️ Техподдержка'), state=None)
async def help_support(message: Message) -> None:
    await message.reply('''Опишите возникшую проблему одним сообщением (или отправьте /cancel для отмены)''')

    await HelpSupport.message.set()

@dp.message_handler(content_types=['text'], state=HelpSupport.message)
async def send_message(message: Message, state: FSMContext) -> None:

    if message.text == '/cancel':

        bot_msg = message.message_id - 1
        user_msg = message.message_id
        await bot.delete_message(message.chat.id, bot_msg)
        await bot.delete_message(message.chat.id, user_msg)

        await message.answer('Обращение отменено!')
        await state.finish()
        return

    await state.update_data(message=message.text)
    with open(f'{DB_LOC}/comments.json', 'r', encoding='windows-1251') as file:
        data = json.load(file)

    with open(f'{DB_LOC}/names.json', 'r', encoding='windows-1251') as file:
        names = json.load(file)
        current_name = names.get(str(message.chat.id))

    '''Проверить на налчиие символов'''

    result_data = {

    }

    for i in message.text:
        if i not in ALPHABET:
            break
    else:
        result_data = {
            'user' : current_name,
            'comment' : message.text
        }

        data.append(result_data)

    try:
        if result_data != {}:
            with open(f'{DB_LOC}/comments.json', 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            await message.answer('Спасибо за ваше сообщение, в ближайшее время мы вам ответим',
                                 reply_markup=UserBot.get_keyboard())

            ''' Отсылаем всем админам сообщение '''
            with open(f'{DB_LOC}/admins.json', encoding='utf-8') as file:
                admins = json.load(file)

            with open(f'{DB_LOC}/names.json', encoding='utf-8') as file:
                names = json.load(file)

            for name in names:
                if names[name] in admins:
                    await bot.send_message(name, 'Появилось новое обращение в техподдержку, проверьте через команду "Админка"')
        else:
            raise Exception

    except Exception as ex:
        await message.answer('Сообщение не было отправлено, попробуйте отправить его еще раз без эмодзи '
                             'или других запрещенных знаков', reply_markup=UserBot.get_keyboard())

    await state.finish()