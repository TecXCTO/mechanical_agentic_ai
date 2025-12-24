import unittest
from unittest.mock import MagicMock, patch
from src.modules.cad.solidworks import SolidWorksInterface
from src.core.data_manager import DataManager # Import DataManager to potentially mock its interactions

class TestSolidWorksInterface(unittest.TestCase):
    def setUp(self):
        # Mock DataManager to avoid actual file creation during tests
        self.mock_data_manager = MagicMock(spec=DataManager)
        # Configure mock save_design to return a predictable path
        self.mock_data_manager.save_design.return_value = "/mock/path/to/sw_design.stl"

        # Patch os.path.exists for load_model tests
        self.mock_os_path_exists = MagicMock()
        self.mock_os_path_exists.return_value = True # Assume file exists for load tests

        # Patch the module's DataManager and os
        self.patcher_dm = patch('src.modules.cad.solidworks.DataManager', return_value=self.mock_data_manager)
        self.patcher_os_path = patch('src.modules.cad.solidworks.os.path.exists', self.mock_os_path_exists)
        self.patcher_print = patch('src.modules.cad.solidworks.print') # To suppress print statements

        self.patcher_dm.start()
        self.patcher_os_path.start()
        self.patcher_print.start()

        self.sw_interface = SolidWorksInterface()

    def tearDown(self):
        self.patcher_dm.stop()
        self.patcher_os_path.stop()
        self.patcher_print.stop()

    def test_create_design(self):
        design_params = {'type': 'bracket', 'size': 'large'}
        expected_filename = "sw_design_XXXXXX.sldprt" # The actual hash will be different
        
        # Call the method
        result_path = self.sw_interface.create_design(design_params)

        # Assert DataManager.save_design was called with expected data and filename structure
        self.mock_data_manager.save_design.assert_called_once()
        # Check if the returned path matches what DataManager would return
        self.assertEqual(result_path, "/mock/path/to/sw_design.stl")
        self.assertIn("sw_design_", self.mock_data_manager.save_design.call_args[0][1]) # Check filename part

    def test_load_model_exists(self):
        model_path = "/path/to/existing/model.sldasm"
        self.mock_os_path_exists.return_value = True

        loaded_path = self.sw_interface.load_model(model_path)

        self.assertEqual(loaded_path, model_path)
        self.assertEqual(self.sw_interface.current_model_path, model_path)

    def test_load_model_not_exists(self):
        model_path = "/path/to/nonexistent/model.sldasm"
        self.mock_os_path_exists.return_value = False

        loaded_path = self.sw_interface.load_model(model_path)

        self.assertIsNone(loaded_path)
        self.assertIsNone(self.sw_interface.current_model_path)

    def test_export_model(self):
        # Set a current model path first
        self.sw_interface.current_model_path = "/mock/path/to/sw_design.stl"
        mock_export_path = "/mock/path/to/exported_design.stl"
        
        # Mock the DataManager save_design for export
        self.mock_data_manager.save_design.return_value = mock_export_path

        exported_path = self.sw_interface.export_model(export_format='stl', output_path=mock_export_path)

        self.assertEqual(exported_path, mock_export_path)
        # Assert DataManager.save_design was called for the export
        self.mock_data_manager.save_design.assert_called_once()

    def test_export_model_no_current_model(self):
        self.sw_interface.current_model_path = None
        exported_path = self.sw_interface.export_model()
        self.assertIsNone(exported_path)

    def test_modify_feature(self):
        # This is a mock, so we just check if it runs without error
        try:
            self.sw_interface.modify_feature("Extrude1", {"depth": 50})
            # If no exception is raised, the mock worked
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"modify_feature raised an unexpected exception: {e}")

    def test_get_model_info(self):
        # Set a current model path for the test
        self.sw_interface.current_model_path = "/mock/path/to/sw_design.stl"
        info = self.sw_interface.get_model_info()
        self.assertIsInstance(info, dict)
        self.assertIn("mass", info)
        self.assertIn("volume", info)
        self.assertIn("dimensions", info)

if __name__ == '__main__':
    unittest.main()
