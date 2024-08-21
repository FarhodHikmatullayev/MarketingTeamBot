from aiogram.dispatcher.filters.state import State, StatesGroup


class WarningState(StatesGroup):
    user_id = State()
    text = State()
    warned_by_id = State()
