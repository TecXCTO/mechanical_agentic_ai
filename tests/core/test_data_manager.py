import unittest
import os
from unittest.mock import patch, MagicMock

from src.core.data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.base_data_dir = "test_data"
        self.mock_os_makedirs = MagicMock()
        self.mock_os_path_exists = MagicMock()
        self.mock_open = MagicMock()
        self.mock_file_handle = MagicMock()

        # Mock the built-in open function
        self.mock_open.return_value.__enter__.return_value = self.mock_file_handle

        # Patch os.makedirs and os.path.exists
        self.patcher_makedirs = patch('src.core.data_manager.os.makedirs', self.mock_os_makedirs)
        self.patcher_path_exists = patch('src.core.data_manager.os.path.exists', self.mock_os_path_exists)
        self.patcher_open = patch('src.core.data_manager.open', self.mock_open)
        self.patcher_print = patch('src.core.data_manager.print') # To suppress print statements during test

        self.patcher_makedirs.start()
        self.patcher_path_exists.start()
        self.patcher_open.start()
        self.patcher_print.start()

        # Instantiate DataManager with a specific test directory
        self.dm = DataManager(data_dir=self.base_data_dir)

    def tearDown(self):
        # Stop patching
        self.patcher_makedirs.stop()
        self.patcher_path_exists.stop()
        self.patcher_open.stop()
        self.patcher_print.stop()

        # Clean up the created mock directories if they were actually created (unlikely with mocks)
        # In a real test, you'd use tempfile and actual file operations, or a more robust mocking strategy
        pass

    def test_create_directories(self):
        # Check if makedirs was called for the expected directories
        expected_dirs = [
            os.path.join(self.base_data_dir, "datasets"),
            os.path.join(self.base_data_dir, "designs"),
            os.path.join(self.base_data_dir, "simulations"),
            os.path.join(self.base_data_dir, "models")
        ]
        self.mock_os_makedirs.assert_any_call(expected_dirs[0], exist_ok=True)
        self.mock_os_makedirs.assert_any_call(expected_dirs[1], exist_ok=True)
        self.mock_os_makedirs.assert_any_call(expected_dirs[2], exist_ok=True)
        self.mock_os_makedirs.assert_any_call(expected_dirs[3], exist_ok=True)

    def test_save_design(self):
        mock_data = "Mock Design Data"
        filename = "test_design.stl"
        expected_filepath = os.path.join(self.base_data_dir, "designs", filename)

        # Ensure path exists returns True for the created file
        self.mock_os_path_exists.return_value = True

        filepath = self.dm.save_design(mock_data, filename)

        self.mock_open.assert_called_once_with(expected_filepath, "w")
        self.mock_file_handle.write.assert_called_once_with(f"Mock CAD data for {filename}\n")
        self.assertEqual(filepath, expected_filepath)

    def test_save_design_io_error(self):
        self.mock_open.side_effect = IOError("Disk full")
        filepath = self.dm.save_design("Mock Data", "error.stl")
        self.assertIsNone(filepath)

    def test_load_design_exists(self):
        filename = "existing_design.stl"
        expected_filepath = os.path.join(self.base_data_dir, "designs", filename)
        self.mock_os_path_exists.return_value = True

        loaded_path = self.dm.load_design(filename)

        self.assertEqual(loaded_path, expected_filepath)

    def test_load_design_not_exists(self):
        filename = "non_existent.stl"
        self.mock_os_path_exists.return_value = False

        loaded_path = self.dm.load_design(filename)
        self.assertIsNone(loaded_path)

    def test_save_simulation_results(self):
        mock_data = "Mock Simulation Results"
        filename = "sim_results.csv"
        expected_filepath = os.path.join(self.base_data_dir, "simulations", filename)

        self.mock_os_path_exists.return_value = True
        filepath = self.dm.save_simulation_results(mock_data, filename)

        self.mock_open.assert_called_once_with(expected_filepath, "w")
        self.mock_file_handle.write.assert_called_once_with(f"Mock simulation results for {filename}\n")
        self.assertEqual(filepath, expected_filepath)

    def test_load_simulation_results_exists(self):
        filename = "existing_results.csv"
        expected_filepath = os.path.join(self.base_data_dir, "simulations", filename)
        self.mock_os_path_exists.return_value = True

        loaded_path = self.dm.load_simulation_results(filename)
        self.assertEqual(loaded_path, expected_filepath)

    def test_load_model_exists(self):
        model_name = "model.pth"
        expected_filepath = os.path.join(self.base_data_dir, "models", model_name)
        self.mock_os_path_exists.return_value = True
        # Mock reading file content
        self.mock_file_handle.read.return_value = b"mock_model_bytes"

        model_data = self.dm.load_model(model_name)

        self.mock_open.assert_called_once_with(expected_filepath, "rb")
        self.assertEqual(model_data, b"mock_model_bytes")

    def test_load_model_not_exists(self):
        model_name = "non_existent_model.pth"
        self.mock_os_path_exists.return_value = False

        model_data = self.dm.load_model(model_name)
        self.assertIsNone(model_data)

if __name__ == '__main__':
    unittest.main()
