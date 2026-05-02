from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from bot.config import PRODUCTS, TEXTS
from bot.dialogs.states import MainMenuSG


async def product_getter(dialog_manager: DialogManager, **_):
    product_id = dialog_manager.dialog_data.get("product_id")
    product = next(p for p in PRODUCTS["bracelets"] if p["id"] == product_id)
    return {
        "card": TEXTS["product_card"].format(
            name=product["name"],
            price_old=product["price_old"],
            price_new=product["price_new"],
            description=product["description"]
        )
    }


async def to_delivery(_, __, manager: DialogManager):
    await manager.switch_to(MainMenuSG.delivery)


async def back_to_catalog(_, __, manager: DialogManager):
    await manager.switch_to(MainMenuSG.catalog)


product_dialog = Dialog(
    Window(
        Format("{card}"),
        Button(Format("заказать"), id="order", on_click=to_delivery),
        Button(Format("назад"), id="back_catalog", on_click=back_to_catalog),
        state=MainMenuSG.product,
        getter=product_getter,
    )
)
