from datetime import datetime, timezone

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.config import PRODUCTS, TEXTS
from bot.dialogs.states import MainMenuSG
from bot.models import Order
from bot.services.notification_service import NotificationService
from bot.services.order_service import OrderService

order_service: OrderService | None = None
notification_service: NotificationService | None = None


def set_order_service(service: OrderService) -> None:
    global order_service
    order_service = service


def set_notification_service(service: NotificationService) -> None:
    global notification_service
    notification_service = service


def _build_order(manager: DialogManager, payment_type: str) -> Order:
    product_id = manager.dialog_data.get("product_id")
    product = next((p for p in PRODUCTS["bracelets"] if p["id"] == product_id), None)
    if product is None:
        raise ValueError("Не удалось определить выбранный товар")

    event = manager.event
    if event is None or getattr(event, "from_user", None) is None:
        raise ValueError("Не удалось определить данные пользователя")

    user = event.from_user
    delivery_type = manager.dialog_data.get("delivery_method")
    delivery_data = manager.dialog_data.get("delivery_data")
    if not delivery_type or not delivery_data:
        raise ValueError("Не заполнены данные доставки")

    return Order(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        product_name=product["name"],
        product_price_old=None,
        product_price_new=product["price"],
        delivery_type=delivery_type,
        delivery_data=delivery_data,
        payment_type=payment_type,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


async def _save_and_finish(manager: DialogManager, payment_type: str) -> None:
    if order_service is None:
        await manager.event.answer("Ошибка сервиса заказа. Попробуйте позже.")
        return

    try:
        order = _build_order(manager, payment_type)
        order_service.create_order(order)
        if notification_service is not None:
            await notification_service.send_order_notification(manager.event.bot, order)
    except Exception:
        await manager.event.answer("Не удалось сохранить заказ. Проверьте данные и попробуйте снова.")
        return

    manager.dialog_data["payment_method"] = payment_type
    await manager.switch_to(MainMenuSG.done)


async def set_card(_, __, manager: DialogManager):
    await _save_and_finish(manager, "Картой")


async def set_sbp(_, __, manager: DialogManager):
    await _save_and_finish(manager, "СБП")


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
