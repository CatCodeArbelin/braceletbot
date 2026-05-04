import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, setup_dialogs

from bot.config import TEXTS, load_settings
from bot.database import SQLiteDatabase
from bot.dialogs import (
    catalog_dialog,
    delivery_dialog,
    main_menu_dialog,
    payment_dialog,
    product_dialog,
)
from bot.dialogs.payment import set_notification_service, set_order_service
from bot.dialogs.states import DeliverySG, MainMenuSG
from bot.services.notification_service import NotificationService
from bot.services.order_service import OrderService

PHONE_PATTERN = re.compile(r"^\+?[0-9]+$")


async def start_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuSG.start)


async def full_name_input_handler(message: Message, dialog_manager: DialogManager):
    dialog_manager.dialog_data["full_name"] = (message.text or "").strip()
    await dialog_manager.switch_to(DeliverySG.full_name_confirm)


async def phone_input_handler(message: Message, dialog_manager: DialogManager):
    phone = (message.text or "").strip()
    if not PHONE_PATTERN.match(phone):
        await message.answer("Телефон может содержать только цифры и символ +. Попробуйте еще раз.")
        return
    dialog_manager.dialog_data["phone"] = phone
    await dialog_manager.switch_to(DeliverySG.phone_confirm)


async def address_input_handler(message: Message, dialog_manager: DialogManager):
    dialog_manager.dialog_data["address"] = (message.text or "").strip()
    await dialog_manager.switch_to(DeliverySG.address_confirm)


async def fallback_handler(message: Message):
    await message.answer(TEXTS["unknown"])


async def main():
    logging.basicConfig(level=logging.INFO)
    settings = load_settings()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    router = Router()

    db = SQLiteDatabase()
    order_service = OrderService(db)
    notification_service = NotificationService(-670831477)
    set_order_service(order_service)
    set_notification_service(notification_service)

    router.message.register(start_handler, CommandStart())
    router.message.register(full_name_input_handler, DeliverySG.full_name_input, F.text)
    router.message.register(phone_input_handler, DeliverySG.phone_input, F.text)
    router.message.register(address_input_handler, DeliverySG.address_input, F.text)
    router.message.register(fallback_handler)

    dp.include_router(router)
    dp.include_router(main_menu_dialog)
    dp.include_router(catalog_dialog)
    dp.include_router(product_dialog)
    dp.include_router(delivery_dialog)
    dp.include_router(payment_dialog)

    setup_dialogs(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
