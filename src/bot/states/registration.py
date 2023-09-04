from aiogram.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    username = State()
    email = State()
