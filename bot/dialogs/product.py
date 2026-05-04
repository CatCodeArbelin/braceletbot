from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format

from bot.config import PRODUCTS, TEXTS
from bot.dialogs.states import CatalogSG, DeliverySG, ProductSG


def _format_price(value: int) -> str:
    return f"{value:,}".replace(",", " ")


async def product_getter(dialog_manager: DialogManager, **_):
    product_id = dialog_manager.start_data.get("product_id")
    product = next(p for p in PRODUCTS["bracelets"] if p["id"] == product_id)
    return {
        "photo_1": product["photos"][0],
        "photo_2": product["photos"][1],
        "card": TEXTS["product_card"].format(
            name=product["name"],
            price_old=_format_price(product["price_old"]),
            price_new=_format_price(product["price_new"]),
            description=product["description"],
        )
    }


async def to_delivery(_, __, manager: DialogManager):
    await manager.start(DeliverySG.delivery, data={"product_id": manager.start_data.get("product_id")})


async def back_to_catalog(_, __, manager: DialogManager):
    await manager.start(CatalogSG.catalog)


product_dialog = Dialog(
    Window(
        Format("{card}"),
        StaticMedia(path=Format("{photo_1}"), type="photo"),
        StaticMedia(path=Format("{photo_2}"), type="photo"),
        Button(Format("заказать"), id="order", on_click=to_delivery),
        Button(Format("назад"), id="back_catalog", on_click=back_to_catalog),
        state=ProductSG.product,
        getter=product_getter,
    )
)
