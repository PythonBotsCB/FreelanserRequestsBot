from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from constants import *
import json

class UserBot():
    @staticmethod
    def get_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [
            KeyboardButton('🙋‍♂️ Заявки на услугу'),
            KeyboardButton('⚙️ Техподдержка'),
            KeyboardButton('🏢 Личный кабинет'),
            KeyboardButton('🏮 Доп. Функции'),
        ]
        keyboard.add(*buttons)

        return keyboard


class AdminBot(UserBot):

    @staticmethod
    def get_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [
            KeyboardButton('🙋‍♂️ Заявки на услугу'),
            KeyboardButton('⚙️ Сообщения'),
            KeyboardButton('🏢 Личный кабинет'),
            KeyboardButton('🏮 Доп. Функции'),
        ]
        keyboard.add(*buttons)

        return keyboard

    @staticmethod
    def is_admin(user_id: int) -> bool:
        with open(f"{DB_LOC}/admins.json") as file:
            admins = json.load(file)

        with open(f'{DB_LOC}/names.json') as file:
            names = json.load(file)

        if names.get(str(user_id)) in admins:
            return True

        return False