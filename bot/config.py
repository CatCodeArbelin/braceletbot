import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_chat_id: int | None


TEXTS = {
    "start": (
        "милая леди, здесь ты можешь выбрать украшения ✨\n\n"
        "{first_name}, выбери что тебя интересует:"
    ),
    "main_menu": "Главное меню:",
    "catalog_title": "Выбери браслет:",
    "chokers_stub": (
        "Скоро здесь появятся чокеры ✨\n"
        "Следите за обновлениями — а пока выберите браслеты в каталоге 💖"
    ),
    "product_card": (
        "{name}\n"
        "Цена: {price_old} ₽\n"
        "✅ Цена сегодня: {price_new} ₽\n\n"
        "{description}"
    ),
    "choose_delivery": "Выбери способ доставки:",
    "choose_payment": "Остался последний шаг, выбери удобный способ оплаты:",
    "order_done": (
        "Поздравляю 💖✨ с покупкой...\n\n"
        "После отправки заказа я пришлю тебе трек-номер, "
        "чтобы ты могла отслеживать доставку на каждом этапе.\n\n"
        "Хорошего тебе дня 🙏🏻"
    ),
    "unknown": (
        "Я пока не понимаю это сообщение 🙏\n"
        "Используй кнопки ниже или введи данные доставки на соответствующем шаге."
    ),
}

DELIVERY_CHOICE_TEXT = "Выбери способ доставки для товара: {product_name}"
DELIVERY_POST_INPUT_TEXT = (
    "Отправь данные доставки одним сообщением.\n"
    "Например: ФИО, телефон, индекс, город, улица, дом, квартира"
)
DELIVERY_CDEK_INPUT_TEXT = (
    "Отправь данные доставки одним сообщением.\n"
    "Например: ФИО, телефон, город, адрес ПВЗ СДЭК"
)


PRODUCTS = {
    "bracelets": [
        {
            "id": "b1",
            "name": "браслет Мелисса",
            "price_old": 3500,
            "price_new": 2500,
            "photos": ["bot/dialogs/melissa1.jpg", "bot/dialogs/melissa2.jpg"],
            "description": (
                "Лаконичный браслет с мягким сиянием для повседневных и вечерних образов.\n"
                "Материалы: премиальный бижутерный сплав и декоративные элементы.\n"
                "Тип замка: тоггл.\n"
                "Посадка: комфортная, с аккуратным прилеганием к запястью."
            ),
        },
        {
            "id": "b2",
            "name": "браслет Сияние",
            "price_old": 2700,
            "price_new": 1700,
            "photos": ["bot/dialogs/siyanie1.jpg", "bot/dialogs/siyanie2.jpg"],
            "description": (
                "Легкий акцентный браслет, который добавляет блеск даже базовым образам.\n"
                "Материалы: премиальный бижутерный сплав и сияющие декоративные элементы.\n"
                "Тип замка: карабин.\n"
                "Посадка: надежная и удобная на каждый день."
            ),
        },
        {
            "id": "b3",
            "name": "браслет Нежность",
            "price_old": 3500,
            "price_new": 2500,
            "photos": ["bot/dialogs/newsnost1.jpg", "bot/dialogs/newsnost2.jpg"],
            "description": (
                "Нежный браслет с воздушным силуэтом и деликатным акцентом в образе.\n"
                "Материалы: премиальный бижутерный сплав и изящные декоративные элементы.\n"
                "Тип замка: карабин.\n"
                "Посадка: легкая, женственная, комфортная в носке."
            ),
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
