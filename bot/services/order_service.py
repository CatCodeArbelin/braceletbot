from bot.database import InMemoryDatabase


class OrderService:
    """Сервис для сохранения заказов из диалога."""

    def __init__(self, db: InMemoryDatabase) -> None:
        self.db = db

    def create_order(self, order_data: dict) -> None:
        """Создает заказ и передает его в БД."""
        self.db.save_order(order_data)
