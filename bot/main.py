import asyncio
import logging

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
from bot.dialogs.payment import set_order_service
from bot.dialogs.states import MainMenuSG
from bot.services.order_service import OrderService


async def start_handler(message: Message, dialog_manager: DialogManager):
    # Запускаем диалог с главного меню.
    await dialog_manager.start(MainMenuSG.start)


async def delivery_input_handler(message: Message, dialog_manager: DialogManager):
    # Сохраняем данные доставки и переводим пользователя к оплате.
    dialog_manager.dialog_data["delivery_data"] = message.text or ""
    await dialog_manager.switch_to(MainMenuSG.payment)


async def fallback_handler(message: Message):
    # Отвечаем на неизвестные сообщения дружелюбной подсказкой.
    await message.answer(TEXTS["unknown"])


async def main():
    # Инициализируем основные компоненты бота.
    logging.basicConfig(level=logging.INFO)
    settings = load_settings()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    router = Router()

    db = SQLiteDatabase()
    order_service = OrderService(db)
    set_order_service(order_service)

    router.message.register(start_handler, CommandStart())
    router.message.register(delivery_input_handler, MainMenuSG.delivery_input, F.text)
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
