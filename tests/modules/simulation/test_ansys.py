import unittest
from unittest.mock import MagicMock, patch
from src.modules.simulation.ansys import AnsysInterface
from src.core.data_manager import DataManager

class TestAnsysInterface(unittest.TestCase):
    def setUp(self):
        # Mock DataManager
        self.mock_data_manager = MagicMock(spec=DataManager)
        self.mock_data_manager.save_simulation_results.side_effect = lambda data, filename: f"/mock/path/to/{filename}"

        # Mock os.path.exists
        self.mock_os_path_exists = MagicMock()
        self.mock_os_path_exists.return_value = True

        # Patch modules
        self.patcher_dm = patch('src.modules.simulation.ansys.DataManager', return_value=self.mock_data_manager)
        self.patcher_os_path = patch('src.modules.simulation.ansys.os.path.exists', self.mock_os_path_exists)
        self.patcher_print = patch('src.modules.simulation.ansys.print')

        self.patcher_dm.start()
        self.patcher_os_path.start()
        self.patcher_print.start()

        self.ansys_interface = AnsysInterface()

    def tearDown(self):
        self.patcher_dm.stop()
        self.patcher_os_path.stop()
        self.patcher_print.stop()

    def test_setup_simulation(self):
        model_path = "/path/to/model.stl"
        sim_config = {"type": "FEA", "load": "100N"}
        
        setup_path = self.ansys_interface.setup_simulation(model_path, sim_config)

        self.mock_data_manager.save_simulation_results.assert_called_once()
        self.assertIn("ansys_setup_", setup_path)
        self.assertIsNotNone(self.ansys_interface.current_simulation_job)
        self.assertEqual(self.ansys_interface.current_simulation_job['model'], model_path)

    def test_run_simulation_without_setup(self):
        model_path = "/path/to/model.stl"
        sim_config = {"type": "FEA", "load": "100N"}

        results_path = self.ansys_interface.run_simulation(model_path, sim_config)

        self.mock_data_manager.save_simulation_results.assert_called_once()
        self.assertIn("ansys_results_", results_path)
        self.assertEqual(self.ansys_interface.current_simulation_job['results_file'], results_path)

    def test_run_simulation_after_setup(self):
        model_path = "/path/to/model.stl"
        sim_config = {"type": "FEA", "load": "100N"}
        self.ansys_interface.setup_simulation(model_path, sim_config)
        
        # Resetting mock calls to check only run_simulation calls
        self.mock_data_manager.save_simulation_results.reset_mock()
        
        results_path = self.ansys_interface.run_simulation(model_path, sim_config)

        self.mock_data_manager.save_simulation_results.assert_called_once()
        self.assertIn("ansys_results_", results_path)
        self.assertEqual(self.ansys_interface.current_simulation_job['results_file'], results_path)

    def test_get_results_summary(self):
        results_path = "/mock/path/to/ansys_results.csv"
        summary = self.ansys_interface.get_results_summary(results_path)
        self.assertIsInstance(summary, dict)
        self.assertIn("max_stress", summary)

    def test_clean_up(self):
        # This is a mock, just ensure it runs without errors
        try:
            self.ansys_interface.clean_up()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"clean_up raised an unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()
