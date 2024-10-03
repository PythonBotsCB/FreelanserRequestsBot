from aiogram.dispatcher.filters.state import StatesGroup, State

class SelectMessages(StatesGroup):
    message = State()

class SelectAds(StatesGroup):
    ad = State()