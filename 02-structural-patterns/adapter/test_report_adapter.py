import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock
from xml.etree import ElementTree

from report_adapter import (
    AnalyticsDashboard,
    LegacyReportAdapter,
    LegacyReportGenerator,
    ReportGeneratorInterface,
    show_inventory_report,
    show_sales_report,
)


class LegacyReportAdapterTests(unittest.TestCase):
    def test_implements_interface_and_preserves_numeric_metrics(self):
        adapter = LegacyReportAdapter(LegacyReportGenerator())
        self.assertIsInstance(adapter, ReportGeneratorInterface)
        data = {"total_sales": 150000, "orders": 1234, "avg_order": 121.55}
        self.assertEqual(json.loads(adapter.generate(data)), data)

    def test_uses_xml_output_as_source(self):
        legacy = Mock(spec=LegacyReportGenerator)
        legacy.generate_report.return_value = (
            "<report><orders>7</orders><label>Ventes &amp; stocks</label>"
            "<empty/><code>007</code></report>"
        )
        data = {"orders": 1}
        report = json.loads(LegacyReportAdapter(legacy).generate(data))
        self.assertEqual(
            report, {"orders": 7, "label": "Ventes & stocks", "empty": "", "code": "007"}
        )
        legacy.generate_report.assert_called_once_with(data)

    def test_empty_report(self):
        adapter = LegacyReportAdapter(LegacyReportGenerator())
        self.assertEqual(json.loads(adapter.generate({})), {})

    def test_invalid_xml_raises_parse_error(self):
        legacy = Mock(spec=LegacyReportGenerator)
        legacy.generate_report.return_value = "<report>"
        with self.assertRaises(ElementTree.ParseError):
            LegacyReportAdapter(legacy).generate({})

    def test_unsupported_report_structure(self):
        legacy = Mock(spec=LegacyReportGenerator)
        adapter = LegacyReportAdapter(legacy)
        for xml in (
            "<other/>",
            "<report><field><nested/></field></report>",
            "<report><orders>1</orders><orders>2</orders></report>",
        ):
            with self.subTest(xml=xml), self.assertRaises(ValueError):
                legacy.generate_report.return_value = xml
                adapter.generate({})

    def test_both_reports_reach_dashboard(self):
        adapter = LegacyReportAdapter(LegacyReportGenerator())
        dashboard = AnalyticsDashboard()
        output = StringIO()
        with redirect_stdout(output):
            show_sales_report(adapter, dashboard)
            show_inventory_report(adapter, dashboard)

        self.assertEqual(output.getvalue().count("=== Analytics Dashboard ==="), 2)
        self.assertIn("avg_order: 121.55", output.getvalue())
        self.assertIn("out_of_stock: 12", output.getvalue())


if __name__ == "__main__":
    unittest.main()
