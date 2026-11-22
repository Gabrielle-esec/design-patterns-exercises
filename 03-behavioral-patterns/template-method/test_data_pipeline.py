import unittest
from contextlib import redirect_stdout
from io import StringIO

from data_pipeline import (
    DataPipeline,
    CSVPipeline,
    APIPipeline,
    DatabasePipeline,
    XMLPipeline,
)


class DataPipelineTests(unittest.TestCase):

    def test_all_pipelines_run(self):
        pipelines = [
            CSVPipeline("data/users.csv"),
            APIPipeline("https://api.example.com/users"),
            DatabasePipeline("postgresql://localhost/mydb"),
            XMLPipeline("data/orders.xml"),
        ]

        for pipeline in pipelines:
            with self.subTest(pipeline=type(pipeline).__name__):
                with redirect_stdout(StringIO()):
                    result = pipeline.run()

                self.assertEqual(
                    result, f"{type(pipeline).__name__} finished"
                )
                self.assertIsNone(pipeline.data)

    def test_csv_transformation(self):
        pipeline = CSVPipeline("data/users.csv")
        pipeline.extract()
        pipeline.transform()

        self.assertEqual(pipeline.data[0]["name"], "ALICE")
        self.assertEqual(pipeline.data[0]["age"], 30)

    def test_api_transformation(self):
        pipeline = APIPipeline("https://api.example.com/users")
        pipeline.extract()
        pipeline.transform()

        self.assertEqual(pipeline.data[0]["grade"], "B")
        self.assertEqual(pipeline.data[1]["grade"], "A")

    def test_database_transformation(self):
        pipeline = DatabasePipeline("database")
        pipeline.extract()
        pipeline.transform()

        self.assertEqual(pipeline.data[0]["tax"], 240.0)
        self.assertEqual(pipeline.data[1]["tax"], 5.0)

    def test_xml_transformation(self):
        pipeline = XMLPipeline("data/orders.xml")
        pipeline.extract()
        pipeline.transform()

        self.assertEqual(pipeline.data[0]["id"], 1)
        self.assertEqual(pipeline.data[0]["amount"], 49.99)

    def test_missing_required_fields(self):
        pipeline = CSVPipeline("data/users.csv")
        pipeline.data = [{"id": 1}]

        with self.assertRaisesRegex(ValueError, "name"):
            pipeline.validate()

    def test_cleanup_even_when_step_fails(self):
        class FailingPipeline(CSVPipeline):
            def transform(self):
                raise RuntimeError("Transformation failed")

        pipeline = FailingPipeline("data/users.csv")

        with redirect_stdout(StringIO()):
            with self.assertRaises(RuntimeError):
                pipeline.run()

        self.assertIsNone(pipeline.data)

    def test_optional_hook(self):
        class CustomPipeline(CSVPipeline):
            def before_load(self):
                self.hook_called = True

        pipeline = CustomPipeline("data/users.csv")
        pipeline.hook_called = False

        with redirect_stdout(StringIO()):
            pipeline.run()

        self.assertTrue(pipeline.hook_called)


if __name__ == "__main__":
    unittest.main()
