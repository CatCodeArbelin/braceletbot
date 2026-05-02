from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bot.config import (
    DELIVERY_CDEK_INPUT_TEXT,
    DELIVERY_CHOICE_TEXT,
    DELIVERY_POST_INPUT_TEXT,
    PRODUCTS,
)
from bot.dialogs.states import MainMenuSG


async def set_post(_, __, manager: DialogManager):
    manager.dialog_data["delivery_method"] = "Почта"
    await manager.switch_to(MainMenuSG.delivery_input)


async def set_cdek(_, __, manager: DialogManager):
    manager.dialog_data["delivery_method"] = "СДЭК"
    await manager.switch_to(MainMenuSG.delivery_input)


async def back_to_product(_, __, manager: DialogManager):
    await manager.switch_to(MainMenuSG.product)


async def back_delivery(_, __, manager: DialogManager):
    await manager.switch_to(MainMenuSG.delivery)


async def delivery_getter(dialog_manager: DialogManager, **_kwargs):
    product_id = dialog_manager.dialog_data.get("product_id")
    product = next((p for p in PRODUCTS["bracelets"] if p["id"] == product_id), None)
    product_name = product["name"] if product is not None else "выбранный товар"
    return {"delivery_choice_text": DELIVERY_CHOICE_TEXT.format(product_name=product_name)}


async def delivery_input_getter(dialog_manager: DialogManager, **_kwargs):
    delivery_method = dialog_manager.dialog_data.get("delivery_method")
    if delivery_method == "СДЭК":
        return {"delivery_input_text": DELIVERY_CDEK_INPUT_TEXT}
    return {"delivery_input_text": DELIVERY_POST_INPUT_TEXT}


delivery_dialog = Dialog(
    Window(
        Format("{delivery_choice_text}"),
        Button(Const("Почта"), id="delivery_post", on_click=set_post),
        Button(Const("СДЭК"), id="delivery_cdek", on_click=set_cdek),
        Button(Const("назад"), id="back_product", on_click=back_to_product),
        state=MainMenuSG.delivery,
        getter=delivery_getter,
    ),
    Window(
        Format("{delivery_input_text}"),
        Button(Const("назад"), id="back_delivery", on_click=back_delivery),
        state=MainMenuSG.delivery_input,
        getter=delivery_input_getter,
    ),
)
