import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_chat_id: int | None


TEXTS = {
    "start": "милая леди, здесь ты можешь выбрать украшения ✨",
    "main_menu": "Главное меню:",
    "catalog_title": "Выбери браслет:",
    "chokers_stub": "Скоро здесь появятся чокеры ✨",
    "product_card": "{name}\n{price_old} ₽ → {price_new} ₽\n\n{description}",
    "choose_delivery": "Выбери способ доставки:",
    "enter_delivery_data_post": (
        "Отправь данные доставки одним сообщением.\n"
        "Например: ФИО, телефон, индекс, город, улица, дом, квартира"
    ),
    "enter_delivery_data_cdek": (
        "Отправь данные доставки одним сообщением.\n"
        "Например: ФИО, телефон, город, адрес ПВЗ СДЭК"
    ),
    "choose_payment": "Выбери способ оплаты:",
    "order_done": (
        "Спасибо за заказ! 🎉\n"
        "Мы получили данные и скоро свяжемся для подтверждения."
    ),
    "unknown": (
        "Я пока не понимаю это сообщение 🙏\n"
        "Используй кнопки ниже или введи данные доставки на соответствующем шаге."
    ),
}


PRODUCTS = {
    "bracelets": [
        {
            "id": "b1",
            "name": "браслет Мелисса",
            "price_old": 3500,
            "price_new": 2500,
            "description": "Лаконичный браслет с мягким сиянием. Тип замка: тоггл.",
        },
        {
            "id": "b2",
            "name": "браслет Сияние",
            "price_old": 2700,
            "price_new": 1700,
            "description": "Легкий акцентный браслет на каждый день. Тип замка: карабин.",
        },
        {
            "id": "b3",
            "name": "браслет Нежность",
            "price_old": 3500,
            "price_new": 2500,
            "description": "Нежный браслет с воздушной посадкой. Тип замка: карабин.",
        },
    ],
       "chokers": [],
}


def load_settings() -> Settings:
    """Загружает настройки из переменных окружения."""
    bot_token = os.getenv("BOT_TOKEN", "")
    admin_chat_id_raw = os.getenv("ADMIN_CHAT_ID", "")

    if not bot_token:
        raise ValueError("Переменная окружения BOT_TOKEN не задана")
    admin_chat_id: int | None = None
    if admin_chat_id_raw:
        try:
            admin_chat_id = int(admin_chat_id_raw)
        except ValueError as exc:
            raise ValueError("ADMIN_CHAT_ID должен быть целым числом") from exc

    return Settings(bot_token=bot_token, admin_chat_id=admin_chat_id)
