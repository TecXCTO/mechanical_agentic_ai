from abc import ABC, abstractmethod

class SimulationInterface(ABC):
    """Abstract base class for simulation software integrations (FEA, CFD, etc.)."""
    def __init__(self, config=None):
        self.config = config or {}
        self.current_simulation_job = None
        print(f"SimulationInterface initialized.")

    @abstractmethod
    def setup_simulation(self, model_path, simulation_config):
        """Sets up the simulation environment based on a model and configuration."""
        pass

    @abstractmethod
    def run_simulation(self, model_path, simulation_config):
        """Runs the simulation and returns the path to the results."""
        pass

    @abstractmethod
    def get_results_summary(self, results_path):
        """Parses simulation results and returns a summary."""
        pass

    @abstractmethod
    def clean_up(self):
        """Cleans up simulation temporary files or resources."""
        pass
