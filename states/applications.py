from aiogram.dispatcher.filters.state import State, StatesGroup


class ApplicationState(StatesGroup):
    user_id = State()
    description = State()
    is_confirmed = State()
    confirmed_at = State()
    confirmed_by_id = State()
