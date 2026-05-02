import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_chat_id: int


TEXTS = {
    "start": "Привет! Добро пожаловать в мастерскую украшений ✨\nВыбери раздел ниже:",
    "main_menu": "Главное меню:",
    "catalog_title": "Каталог браслетов✨\nВыбери товар:",
    "chokers_stub": "Раздел чокеров✨ скоро появится. Возвращайся позже 💫",
    "product_card": "{name}\nЦена: {price} ₽\n\n{description}",
    "choose_delivery": "Выбери способ доставки:",
    "enter_delivery_data": (
        "Отправь данные доставки одним сообщением.\n"
        "Например: ФИО, телефон, индекс, город, улица, дом, квартира"
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
            "name": "Браслет «Лунный блеск»",
            "price": 1490,
            "description": "Нежный браслет с перламутровыми бусинами.",
        },
        {
            "id": "b2",
            "name": "Браслет «Северный ветер»",
            "price": 1790,
            "description": "Минималистичный браслет в холодных оттенках.",
        },
        {
            "id": "b3",
            "name": "Браслет «Золотой час»",
            "price": 1990,
            "description": "Акцентный браслет с фурнитурой под золото.",
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
    if not admin_chat_id_raw:
        raise ValueError("Переменная окружения ADMIN_CHAT_ID не задана")

    try:
        admin_chat_id = int(admin_chat_id_raw)
    except ValueError as exc:
        raise ValueError("ADMIN_CHAT_ID должен быть целым числом") from exc

    return Settings(bot_token=bot_token, admin_chat_id=admin_chat_id)
