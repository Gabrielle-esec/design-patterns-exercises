from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
import re


class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> bool:
        """Check the details required by this payment method."""

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        """Return the result of a simulated payment."""


def payment_result(payment_type: str, amount: float, fee: Decimal) -> dict:
    fee = fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return {
        "status": "success",
        "payment_type": payment_type,
        "amount": amount,
        "fee": float(fee),
        "total": float(Decimal(str(amount)) + fee),
    }


class CreditCardProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number")
        cvv = details.get("cvv")
        return (
            isinstance(card_number, str)
            and re.fullmatch(r"[0-9]{16}", card_number) is not None
            and isinstance(cvv, str)
            and re.fullmatch(r"[0-9]{3}", cvv) is not None
        )

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            raise ValueError("Expected a 16-digit card number and a 3-digit CVV.")
        fee = Decimal(str(amount)) * Decimal("0.029")
        return payment_result("credit_card", amount, fee)


class BankTransferProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        iban = details.get("iban")
        return isinstance(iban, str) and len(iban) >= 15

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            raise ValueError("Expected an IBAN of at least 15 characters.")
        return payment_result("bank_transfer", amount, Decimal("1.50"))


class PayPalProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        email = details.get("email")
        return isinstance(email, str) and "@" in email

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            raise ValueError("Expected an email address containing @.")
        fee = Decimal(str(amount)) * Decimal("0.034") + Decimal("0.30")
        return payment_result("paypal", amount, fee)


class PaymentFactory:
    _processors = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    @classmethod
    def get_processor(cls, payment_type: str) -> PaymentProcessor:
        processor_class = cls._processors.get(payment_type)
        if processor_class is None:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return processor_class()


if __name__ == "__main__":
    import unittest

    class PaymentFactoryTests(unittest.TestCase):
        def test_credit_card(self):
            processor = PaymentFactory.get_processor("credit_card")
            self.assertIsInstance(processor, CreditCardProcessor)
            details = {"card_number": "4242424242424242", "cvv": "012"}
            self.assertTrue(processor.validate(details))
            result = processor.process(100.0, details)
            self.assertEqual(result["fee"], 2.90)
            self.assertEqual(result["total"], 102.90)
            with self.assertRaises(ValueError):
                processor.process(100.0, {**details, "cvv": "12"})
            self.assertFalse(processor.validate({**details, "card_number": "4242"}))

        def test_bank_transfer(self):
            processor = PaymentFactory.get_processor("bank_transfer")
            self.assertIsInstance(processor, BankTransferProcessor)
            details = {"iban": "FR1234567890123"}
            self.assertTrue(processor.validate(details))
            result = processor.process(100.0, details)
            self.assertEqual(result["fee"], 1.50)
            self.assertEqual(result["total"], 101.50)
            with self.assertRaises(ValueError):
                processor.process(100.0, {"iban": "FR123456789012"})

        def test_paypal(self):
            processor = PaymentFactory.get_processor("paypal")
            self.assertIsInstance(processor, PayPalProcessor)
            details = {"email": "demo@example.com"}
            self.assertTrue(processor.validate(details))
            result = processor.process(100.0, details)
            self.assertEqual(result["fee"], 3.70)
            self.assertEqual(result["total"], 103.70)
            with self.assertRaises(ValueError):
                processor.process(100.0, {"email": "demo.example.com"})

        def test_unknown_payment_type(self):
            with self.assertRaises(ValueError):
                PaymentFactory.get_processor("cash")

    unittest.main()
