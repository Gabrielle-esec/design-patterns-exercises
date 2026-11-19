"""Simulate four consumers of the shared configuration."""

from config_manager import ConfigManager


def start_application() -> None:
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")


def connect_database() -> None:
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to: str, subject: str) -> None:
    config = ConfigManager.get_instance()
    sender = config.get("email.sender")
    smtp_host = config.get("email.smtp_host")
    print(f"Sending {subject!r} to {to} from {sender} via {smtp_host}")


def process_payment(amount: float) -> None:
    config = ConfigManager.get_instance()
    print(f"Processing {amount:.2f}€ in {config.get('payment.environment')} mode")


if __name__ == "__main__":
    start_application()
    connect_database()
    send_email("user@test.com", "Welcome")
    process_payment(99.99)
