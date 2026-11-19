import unittest
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from unittest.mock import patch

from config_manager import ConfigManager


class ConfigManagerTests(unittest.TestCase):
    def setUp(self):
        instance_patch = patch.object(ConfigManager, "_instance", None)
        instance_patch.start()
        self.addCleanup(instance_patch.stop)

    def test_loads_only_once_on_first_access(self):
        data = '{"database": {"host": "localhost"}}'
        with patch("config_manager.Path.open", return_value=StringIO(data)) as read:
            read.assert_not_called()
            first = ConfigManager.get_instance()
            self.assertIs(first, ConfigManager.get_instance())
            self.assertIs(first, ConfigManager())
            self.assertEqual(first.get("database.host"), "localhost")
            read.assert_called_once_with(encoding="utf-8")

    def test_concurrent_access_shares_one_instance(self):
        with patch("config_manager.Path.open", return_value=StringIO("{}")) as read:
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(ConfigManager.get_instance) for _ in range(16)]
                instances = [future.result() for future in futures]
            self.assertTrue(all(instance is instances[0] for instance in instances))
            read.assert_called_once()

    def test_reads_nested_values(self):
        config = ConfigManager.get_instance()
        self.assertEqual(config.get("database.port"), 5432)
        self.assertIs(config.get("app.debug"), True)

    def test_missing_keys_raise_key_error(self):
        config = ConfigManager.get_instance()
        for key in ("missing", "database.missing", "app.debug.enabled", "database.", ""):
            with self.subTest(key=key), self.assertRaises(KeyError) as error:
                config.get(key)
            self.assertEqual(error.exception.args, (key,))

    def test_returned_section_does_not_change_shared_configuration(self):
        config = ConfigManager.get_instance()
        database = config.get("database")
        database["port"] = 9999
        self.assertEqual(config.get("database.port"), 5432)

    def test_failed_load_can_be_retried(self):
        results = [StringIO("[]"), StringIO('{"app": {"debug": false}}')]
        with patch("config_manager.Path.open", side_effect=results) as read:
            with self.assertRaises(ValueError):
                ConfigManager.get_instance()
            self.assertIs(ConfigManager.get_instance().get("app.debug"), False)
            self.assertEqual(read.call_count, 2)


if __name__ == "__main__":
    unittest.main()
