from src.modules.simulation.sim_interface import SimulationInterface
import os

class AbaqusInterface(SimulationInterface):
    def __init__(self, config=None):
        super().__init__(config)
        print("Abaqus Interface initialized. (Mock)")
        # In a real implementation: connect to Abaqus API or scripting interface

    def setup_simulation(self, model_path, simulation_config):
        print(f"Abaqus: Setting up simulation for {model_path} with config {simulation_config}. (Mock)")
        # Mock setup
        mock_setup_file = f"abaqus_setup_{hash(model_path+str(simulation_config))}.inp"
        from src.core.data_manager import DataManager
        dm = DataManager()
        setup_path = dm.save_simulation_results(f"Mock Abaqus setup for {model_path}", mock_setup_file)
        self.current_simulation_job = {"setup_file": setup_path, "model": model_path, "config": simulation_config}
        return setup_path

    def run_simulation(self, model_path, simulation_config):
        if not self.current_simulation_job or self.current_simulation_job['model'] != model_path:
            self.setup_simulation(model_path, simulation_config)

        print(f"Abaqus: Running simulation...")
        # Mock run
        mock_results_file = f"abaqus_results_{hash(str(self.current_simulation_job))}.dat"
        from src.core.data_manager import DataManager
        dm = DataManager()
        results_path = dm.save_simulation_results(f"Mock Abaqus simulation results for {model_path}", mock_results_file)
        print(f"Abaqus: Simulation completed. Results saved to {results_path}. (Mock)")
        self.current_simulation_job['results_file'] = results_path
        return results_path

    def get_results_summary(self, results_path):
        print(f"Abaqus: Getting summary for results at {results_path}. (Mock)")
        # Mock parsing
        summary = {"max_stress": 120.0, "max_displacement": 0.4, "status": "success"}
        return summary

    def clean_up(self):
        print("Abaqus: Cleaning up simulation resources. (Mock)")
        pass
