import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from report_strategy import (
    ReportGenerator,
    ReportFormatStrategy,
    PDFFormatStrategy,
    ExcelFormatStrategy,
    CSVFormatStrategy,
    JSONFormatStrategy,
    HTMLFormatStrategy,
)


class ReportStrategyTests(unittest.TestCase):

    def setUp(self):
        self.data = [
            {"name": "Sales Q1", "value": 15000},
            {"name": "Sales Q2", "value": 18000},
        ]
        self.generator = ReportGenerator(self.data)

    def test_all_strategies_follow_interface(self):
        strategies = [
            PDFFormatStrategy(),
            ExcelFormatStrategy(),
            CSVFormatStrategy(),
            JSONFormatStrategy(),
            HTMLFormatStrategy(),
        ]
        for strategy in strategies:
            with self.subTest(strategy=type(strategy).__name__):
                self.assertIsInstance(strategy, ReportFormatStrategy)
                self.assertTrue(strategy.generate(self.data))

    def test_switch_strategies_dynamically(self):
        self.generator.set_strategy(PDFFormatStrategy())
        self.assertIn("PDF REPORT", self.generator.generate_report())

        self.generator.set_strategy(CSVFormatStrategy())
        self.assertEqual(
            self.generator.generate_report(),
            "name,value\nSales Q1,15000\nSales Q2,18000\n",
        )

    def test_json_strategy(self):
        self.generator.set_strategy(JSONFormatStrategy())
        result = json.loads(self.generator.generate_report())
        self.assertEqual(result, self.data)

    def test_html_strategy(self):
        self.generator.set_strategy(HTMLFormatStrategy())
        result = self.generator.generate_report()
        self.assertIn("<table>", result)
        self.assertIn("<td>Sales Q1</td>", result)

    def test_excel_strategy(self):
        self.generator.set_strategy(ExcelFormatStrategy())
        result = self.generator.generate_report()
        self.assertIn("Name\tValue", result)
        self.assertIn("Sales Q1\t15000", result)

    def test_missing_strategy(self):
        with self.assertRaises(ValueError):
            self.generator.generate_report()

        with TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                self.generator.save_report(
                    str(Path(folder) / "report")
                )

    def test_save_report(self):
        with TemporaryDirectory() as folder:
            for strategy in [
                PDFFormatStrategy(),
                ExcelFormatStrategy(),
                CSVFormatStrategy(),
                JSONFormatStrategy(),
                HTMLFormatStrategy(),
            ]:
                with self.subTest(strategy=type(strategy).__name__):
                    self.generator.set_strategy(strategy)

                    filename = str(Path(folder) / "report")
                    self.generator.save_report(filename)

                    output = Path(filename + strategy.extension())
                    self.assertTrue(output.exists())
                    self.assertEqual(
                        output.read_text(encoding="utf-8"),
                        self.generator.generate_report(),
                    )


if __name__ == "__main__":
    unittest.main()
