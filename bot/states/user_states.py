from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStatesGroup(StatesGroup):
    lang = State()
    name = State()
    phone = State()
    confirm_code = State()
