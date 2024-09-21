from aiogram.dispatcher.filters.state import State, StatesGroup


class ScheduleCreateState(StatesGroup):
    user_id = State()
    arrival_time = State()
    departure_time = State()


class ScheduleUpdateState(StatesGroup):
    user_id = State()
    arrival_time = State()
    departure_time = State()
