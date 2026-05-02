from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.config import TEXTS
from bot.dialogs.states import MainMenuSG


async def set_card(_, __, manager: DialogManager):
    manager.dialog_data["payment_method"] = "Картой"
    await manager.switch_to(MainMenuSG.done)


async def set_sbp(_, __, manager: DialogManager):
    manager.dialog_data["payment_method"] = "СБП"
    await manager.switch_to(MainMenuSG.done)


async def back_to_delivery_input(_, __, manager: DialogManager):
    await manager.switch_to(MainMenuSG.delivery_input)


async def to_start(_, __, manager: DialogManager):
    await manager.switch_to(MainMenuSG.start)


payment_dialog = Dialog(
    Window(
        Const(TEXTS["choose_payment"]),
        Button(Const("Картой"), id="pay_card", on_click=set_card),
        Button(Const("СБП"), id="pay_sbp", on_click=set_sbp),
        Button(Const("Назад"), id="back_delivery_input", on_click=back_to_delivery_input),
        state=MainMenuSG.payment,
    ),
    Window(
        Const(TEXTS["order_done"]),
        Button(Const("Вернуться в начало"), id="back_start", on_click=to_start),
        state=MainMenuSG.done,
    ),
)
