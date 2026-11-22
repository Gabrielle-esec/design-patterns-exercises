"""Data ETL pipelines using the Template Method pattern."""

from abc import ABC, abstractmethod


class DataPipeline(ABC):
    required_fields: tuple[str, ...] = ()

    def __init__(self, source: str):
        self.source = source
        self.data = None

    def run(self) -> str:
        try:
            self.connect()
            self.extract()
            self.transform()
            self.validate()
            self.before_load()
            self.load()
            return f"{self.__class__.__name__} finished"
        finally:
            self.cleanup()

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def extract(self) -> None:
        pass

    @abstractmethod
    def transform(self) -> None:
        pass

    def validate(self) -> None:
        if not isinstance(self.data, list):
            raise ValueError("Pipeline data must be a list")

        for record in self.data:
            if not isinstance(record, dict):
                raise ValueError("Every record must be a dictionary")

            for field in self.required_fields:
                if field not in record:
                    raise ValueError(f"Missing required field: {field}")

        print("Validation passed")

    def before_load(self) -> None:
        pass

    def load(self) -> None:
        print(f"Loaded {len(self.data)} records successfully")

    def cleanup(self) -> None:
        print("Cleaning up resources...")
        self.data = None
        print("Cleanup complete")


class CSVPipeline(DataPipeline):
    required_fields = ("id", "name")

    def connect(self) -> None:
        print(f"Connecting to CSV file: {self.source}")
        print("CSV connection established")

    def extract(self) -> None:
        print("Extracting data from CSV...")
        self.data = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
        ]

    def transform(self) -> None:
        print("Transforming CSV data...")
        for record in self.data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()


class APIPipeline(DataPipeline):
    required_fields = ("user_id", "username")

    def connect(self) -> None:
        print(f"Connecting to API: {self.source}")
        print("API connection established")

    def extract(self) -> None:
        print("Extracting data from API...")
        self.data = [
            {"user_id": 101, "username": "charlie", "score": 85},
            {"user_id": 102, "username": "diana", "score": 92},
        ]

    def transform(self) -> None:
        print("Transforming API data...")
        for record in self.data:
            record["score"] = int(record["score"])
            record["username"] = record["username"].lower()
            record["grade"] = "A" if record["score"] >= 90 else "B"


class DatabasePipeline(DataPipeline):
    required_fields = ("product_id", "price")

    def connect(self) -> None:
        print(f"Connecting to database: {self.source}")
        print("Database connection established")

    def extract(self) -> None:
        print("Extracting data from database...")
        self.data = [
            {"product_id": 501, "product_name": "Laptop", "price": 1200},
            {"product_id": 502, "product_name": "Mouse", "price": 25},
        ]

    def transform(self) -> None:
        print("Transforming database data...")
        for record in self.data:
            record["price"] = float(record["price"])
            record["product_name"] = record["product_name"].title()
            record["tax"] = record["price"] * 0.2


class XMLPipeline(DataPipeline):
    required_fields = ("id", "amount")

    def connect(self) -> None:
        print(f"Connecting to XML file: {self.source}")
        print("XML connection established")

    def extract(self) -> None:
        print("Extracting XML data...")
        from xml.etree import ElementTree

        xml = """
        <orders>
            <order id="1" amount="49.99"/>
            <order id="2" amount="120.00"/>
        </orders>
        """
        root = ElementTree.fromstring(xml)
        self.data = [dict(order.attrib) for order in root.findall("order")]

    def transform(self) -> None:
        print("Transforming XML data...")
        for record in self.data:
            record["id"] = int(record["id"])
            record["amount"] = float(record["amount"])


if __name__ == "__main__":
    pipelines = [
        CSVPipeline("data/users.csv"),
        APIPipeline("https://api.example.com/users"),
        DatabasePipeline("postgresql://localhost/mydb"),
        XMLPipeline("data/orders.xml"),
    ]

    for pipeline in pipelines:
        print(f"\n===== {type(pipeline).__name__} =====")
        print(pipeline.run())
