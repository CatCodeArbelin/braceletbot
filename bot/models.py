from dataclasses import dataclass


@dataclass
class Product:
    """Модель товара для отображения в каталоге."""

    id: str
    name: str
    price: int
    description: str


@dataclass
class OrderDraft:
    """Черновик заказа, который собирается по шагам диалога."""

    product_id: str
    delivery_method: str | None = None
    delivery_data: str | None = None
    payment_method: str | None = None
