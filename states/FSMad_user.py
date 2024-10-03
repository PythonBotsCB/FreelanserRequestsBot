from aiogram.dispatcher.filters.state import StatesGroup, State

class SetAd(StatesGroup):

    category = State()
    text_request = State()
