from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_contact = State()
    waiting_location = State()
    confirming_order = State()
