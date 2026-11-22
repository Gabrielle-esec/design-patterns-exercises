import unittest

from order_decorators import (
    BaseOrder,
    DiscountDecorator,
    ExpressShippingDecorator,
    GiftWrapDecorator,
    InsuranceDecorator,
    PremiumMemberDecorator,
)


class OrderDecoratorTests(unittest.TestCase):
    def test_base_order(self):
        order = BaseOrder(100.00)
        self.assertEqual(order.get_cost(), 100.00)
        self.assertEqual(order.get_description(), "Base price: 100.00€")

    def test_fixed_fees_leave_the_wrapped_order_unchanged(self):
        base = BaseOrder(100.00)
        express = ExpressShippingDecorator(base)
        gift = GiftWrapDecorator(express)
        self.assertEqual(gift.get_cost(), 120.00)
        self.assertEqual(express.get_cost(), 115.00)
        self.assertEqual(base.get_cost(), 100.00)

    def test_insurance_uses_the_original_base_price(self):
        order = InsuranceDecorator(ExpressShippingDecorator(BaseOrder(200.00)))
        self.assertEqual(order.get_cost(), 225.00)
        self.assertIn("Insurance (5%): +10.00€", order.get_description())

    def test_discount_applies_to_the_wrapped_subtotal(self):
        base = BaseOrder(100.00)
        discount_last = DiscountDecorator(ExpressShippingDecorator(base), percent=20)
        shipping_last = ExpressShippingDecorator(DiscountDecorator(base, percent=20))
        self.assertAlmostEqual(discount_last.get_cost(), 92.00)
        self.assertAlmostEqual(shipping_last.get_cost(), 95.00)

    def test_discount_percentage_limits(self):
        base = BaseOrder(100.00)
        self.assertEqual(DiscountDecorator(base, percent=0).get_cost(), 100.00)
        self.assertEqual(DiscountDecorator(base, percent=100).get_cost(), 0.00)
        for percent in (-1, 101, float("nan")):
            with self.subTest(percent=percent), self.assertRaises(ValueError):
                DiscountDecorator(base, percent=percent)

    def test_all_options_itemized_in_order(self):
        order = ExpressShippingDecorator(BaseOrder(100.00))
        insured = InsuranceDecorator(order)
        wrapped = GiftWrapDecorator(insured)
        discounted = DiscountDecorator(wrapped, percent=15)
        premium = PremiumMemberDecorator(discounted)

        self.assertAlmostEqual(premium.get_cost(), 95.625)
        self.assertEqual(premium.get_description().splitlines(), [
            "Base price: 100.00€",
            "Express shipping: +15.00€",
            "Insurance (5%): +5.00€",
            "Gift wrap: +5.00€",
            "Discount (15%): -18.75€",
            "Premium member (10%): -10.62€",
        ])


if __name__ == "__main__":
    unittest.main()
