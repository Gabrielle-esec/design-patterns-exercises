"""Compose order pricing options using the Decorator pattern."""

from abc import ABC, abstractmethod


class OrderComponent(ABC):
    @property
    @abstractmethod
    def base_price(self) -> float:
        """Original price before any pricing options."""

    @abstractmethod
    def get_cost(self) -> float:
        """Return the accumulated price."""

    @abstractmethod
    def get_description(self) -> str:
        """Return the itemized price breakdown."""


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float) -> None:
        self._base_price = base_price

    @property
    def base_price(self) -> float:
        return self._base_price

    def get_cost(self) -> float:
        return self.base_price

    def get_description(self) -> str:
        return f"Base price: {self.base_price:.2f}€"


class OrderDecorator(OrderComponent):
    def __init__(self, order: OrderComponent) -> None:
        self._order = order

    @property
    def base_price(self) -> float:
        return self._order.base_price

    @abstractmethod
    def _adjustment(self, subtotal: float) -> tuple[str, float]:
        """Return the adjustment label and its signed amount."""

    def get_cost(self) -> float:
        subtotal = self._order.get_cost()
        _, amount = self._adjustment(subtotal)
        return subtotal + amount

    def get_description(self) -> str:
        label, amount = self._adjustment(self._order.get_cost())
        return f"{self._order.get_description()}\n{label}: {amount:+.2f}€"


class ExpressShippingDecorator(OrderDecorator):
    def _adjustment(self, subtotal: float) -> tuple[str, float]:
        return "Express shipping", 15.00


class InsuranceDecorator(OrderDecorator):
    def _adjustment(self, subtotal: float) -> tuple[str, float]:
        return "Insurance (5%)", self.base_price * 0.05


class GiftWrapDecorator(OrderDecorator):
    def _adjustment(self, subtotal: float) -> tuple[str, float]:
        return "Gift wrap", 5.00


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float) -> None:
        super().__init__(order)
        if not 0 <= percent <= 100:
            raise ValueError("Discount percent must be between 0 and 100")
        self._percent = percent

    def _adjustment(self, subtotal: float) -> tuple[str, float]:
        return f"Discount ({self._percent:g}%)", -subtotal * (self._percent / 100)


class PremiumMemberDecorator(DiscountDecorator):
    def __init__(self, order: OrderComponent) -> None:
        super().__init__(order, percent=10)

    def _adjustment(self, subtotal: float) -> tuple[str, float]:
        _, amount = super()._adjustment(subtotal)
        return "Premium member (10%)", amount


def main() -> None:
    base_order = BaseOrder(100.00)
    print(base_order.get_description())
    print(f"Total: {base_order.get_cost():.2f}€\n")

    order: OrderComponent = base_order
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)

    print(order.get_description())
    print(f"Total: {order.get_cost():.2f}€")


if __name__ == "__main__":
    main()
