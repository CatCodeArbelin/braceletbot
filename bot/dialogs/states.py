from aiogram.fsm.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    start = State()
    chokers_stub = State()


class CatalogSG(StatesGroup):
    catalog = State()


class ProductSG(StatesGroup):
    product = State()
    product_photo_2 = State()


class DeliverySG(StatesGroup):
    delivery = State()
    delivery_input = State()


class PaymentSG(StatesGroup):
    payment = State()
    done = State()
