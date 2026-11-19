"""Adapt flat XML reports to the dashboard's JSON interface."""

import json
from abc import ABC, abstractmethod
from xml.etree import ElementTree


class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        """Returns XML format - old system"""
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


class AnalyticsDashboard:
    def display(self, json_data: str):
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        """Return a JSON report."""


class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy: LegacyReportGenerator) -> None:
        self._legacy = legacy

    def generate(self, data: dict) -> str:
        xml_report = self._legacy.generate_report(data)
        root = ElementTree.fromstring(xml_report)
        if root.tag != "report":
            raise ValueError("Expected a <report> root element")

        report = {}
        for field in root:
            if len(field) or field.tag in report:
                raise ValueError("Expected unique, flat report fields")
            report[field.tag] = self._convert_value(field.text or "")

        return json.dumps(report, ensure_ascii=False, allow_nan=False)

    @staticmethod
    def _convert_value(text: str) -> str | int | float:
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            return text
        # XML has no type metadata. Interpret only JSON-compatible numbers.
        return value if type(value) in (int, float) else text


def show_sales_report(
    generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard
) -> None:
    data = {"total_sales": 150000, "orders": 1234, "avg_order": 121.55}
    dashboard.display(generator.generate(data))


def show_inventory_report(
    generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard
) -> None:
    data = {"total_items": 5000, "low_stock": 45, "out_of_stock": 12}
    dashboard.display(generator.generate(data))


if __name__ == "__main__":
    generator = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()
    show_sales_report(generator, dashboard)
    show_inventory_report(generator, dashboard)
