from aiogram.fsm.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    start = State()
    chokers_stub = State()
    catalog = State()
    product = State()
    delivery = State()
    delivery_input = State()
    payment = State()
    done = State()
