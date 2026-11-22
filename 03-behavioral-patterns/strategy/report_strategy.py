"""Report generation using the Strategy design pattern."""

from abc import ABC, abstractmethod


class ReportFormatStrategy(ABC):
    """Common interface for every report format."""

    @abstractmethod
    def generate(self, data: list) -> str:
        pass

    @abstractmethod
    def extension(self) -> str:
        pass


class PDFFormatStrategy(ReportFormatStrategy):
    """Generate a PDF-style text report."""

    def generate(self, data: list) -> str:
        report = "PDF REPORT\n"
        report += "=" * 50 + "\n"

        for item in data:
            report += f"| {item['name']:20} | {item['value']:10} |\n"

        report += "=" * 50 + "\n"
        report += "End of PDF Report"
        return report

    def extension(self) -> str:
        return ".pdf"


class ReportGenerator:
    """Context that delegates formatting to a strategy."""

    def __init__(self, data: list):
        self.data = data
        self._strategy = None

    def set_strategy(self, strategy: ReportFormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        if self._strategy is None:
            raise ValueError("No report strategy selected")

        return self._strategy.generate(self.data)

    def save_report(self, filename: str) -> None:
        if self._strategy is None:
            raise ValueError("No report strategy selected")

        content = self.generate_report()
        output_path = filename + self._strategy.extension()

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(content)


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]

    generator = ReportGenerator(data)
    generator.set_strategy(PDFFormatStrategy())

    print(generator.generate_report())


class ExcelFormatStrategy(ReportFormatStrategy):
    def generate(self, data: list) -> str:
        report = "EXCEL REPORT\n"
        report += "-" * 50 + "\n"
        report += "Name\tValue\n"
        for item in data:
            report += f"{item['name']}\t{item['value']}\n"
        report += "-" * 50 + "\n"
        return report

    def extension(self) -> str:
        return ".xlsx"


class CSVFormatStrategy(ReportFormatStrategy):
    def generate(self, data: list) -> str:
        report = "name,value\n"
        for item in data:
            report += f"{item['name']},{item['value']}\n"
        return report

    def extension(self) -> str:
        return ".csv"


class JSONFormatStrategy(ReportFormatStrategy):
    def generate(self, data: list) -> str:
        import json
        return json.dumps(data, indent=2)

    def extension(self) -> str:
        return ".json"


class HTMLFormatStrategy(ReportFormatStrategy):
    def generate(self, data: list) -> str:
        import html

        rows = []
        for item in data:
            name = html.escape(str(item["name"]))
            value = html.escape(str(item["value"]))
            rows.append(f"<tr><td>{name}</td><td>{value}</td></tr>")

        return (
            "<html><body><table>"
            "<tr><th>Name</th><th>Value</th></tr>"
            + "".join(rows)
            + "</table></body></html>"
        )

    def extension(self) -> str:
        return ".html"
