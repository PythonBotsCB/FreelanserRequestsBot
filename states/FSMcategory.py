from aiogram.dispatcher.filters.state import StatesGroup, State

class SelectCategory(StatesGroup):

    category = State()
    traffic = State()
    paid = State()