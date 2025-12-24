import unittest
from unittest.mock import patch, MagicMock
from src.core.config import ConfigManager
import yaml

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        # Mock the os module to control directory listing and file existence
        self.mock_os = MagicMock()
        # Mock the yaml module to control yaml.safe_load
        self.mock_yaml = MagicMock()

        # Create a dummy config directory structure for tests
        self.config_dir = "mock_data/config"
        self.mock_os.path.join.side_effect = lambda *args: '/'.join(args)
        self.mock_os.listdir.return_value = ["design_agent.yaml", "simulation_agent.yml"]
        self.mock_os.path.exists.return_value = True
        self.mock_os.path.splitext.side_effect = lambda x: (x, '.yaml' if x.endswith('.yaml') else '.yml')

        # Mock the yaml load function to return predefined data
        self.mock_yaml.safe_load.side_effect = [
            {"design_params": {"type": "bracket"}, "optimizer_settings": {"iterations": 100}},
            {"simulation_type": "FEA", "solver_settings": {"mesh_size": 0.5}}
        ]

        # Patch the modules
        self.patcher_os = patch('src.core.config.os', self.mock_os)
        self.patcher_yaml = patch('src.core.config.yaml', self.mock_yaml)

        self.patcher_os.start()
        self.patcher_yaml.start()

        # Instantiate ConfigManager using the mocked config directory
        self.config_manager = ConfigManager(config_dir=self.config_dir)

    def tearDown(self):
        # Stop patching
        self.patcher_os.stop()
        self.patcher_yaml.stop()

    def test_load_all_configs(self):
        # Check if os.listdir was called correctly
        self.mock_os.listdir.assert_called_once_with(self.config_dir)
        # Check if yaml.safe_load was called for each file
        self.assertEqual(self.mock_yaml.safe_load.call_count, 2)
        # Check if configs were loaded correctly
        self.assertIn('design_agent', self.config_manager.configs)
        self.assertIn('simulation_agent', self.config_manager.configs)
        self.assertEqual(self.config_manager.configs['design_agent']['design_params']['type'], 'bracket')

    def test_get_existing_key(self):
        design_params = self.config_manager.get('design_agent.design_params')
        self.assertEqual(design_params, {'type': 'bracket'})

    def test_get_nested_key(self):
        optimizer_iter = self.config_manager.get('design_agent.optimizer_settings.iterations')
        self.assertEqual(optimizer_iter, 100)

    def test_get_non_existent_key(self):
        non_existent = self.config_manager.get('non_existent.key', default='default_value')
        self.assertEqual(non_existent, 'default_value')

    def test_get_section(self):
        simulation_section = self.config_manager.get_section('simulation_agent')
        self.assertEqual(simulation_section['simulation_type'], 'FEA')

    def test_get_section_non_existent(self):
        non_existent_section = self.config_manager.get_section('another_agent', default={'status': 'unknown'})
        self.assertEqual(non_existent_section, {'status': 'unknown'})

    def test_load_all_configs_empty_dir(self):
        self.mock_os.listdir.return_value = []
        cm = ConfigManager(config_dir="empty_dir")
        self.assertEqual(cm.configs, {})

    def test_load_all_configs_error(self):
        self.mock_yaml.safe_load.side_effect = yaml.YAMLError("Parse error")
        # Expecting print output or logging for error
        with unittest.mock.patch('builtins.print') as mock_print:
            ConfigManager(config_dir=self.config_dir)
            mock_print.assert_any_call("Error loading config design_agent.yaml: Parse error")

if __name__ == '__main__':
    unittest.main()
