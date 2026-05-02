class InMemoryDatabase:
    """Простая заглушка БД для будущего хранения заказов."""

    def __init__(self) -> None:
        # Храним заказы в памяти процесса.
        self.orders: list[dict] = []

    def save_order(self, order_data: dict) -> None:
        """Сохраняет заказ в локальный список."""
        self.orders.append(order_data)
