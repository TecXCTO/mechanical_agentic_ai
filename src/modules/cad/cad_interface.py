from abc import ABC, abstractmethod

class CADInterface(ABC):
    """Abstract base class for CAD software integrations."""
    def __init__(self, config=None):
        self.config = config or {}
        self.current_model_path = None
        print(f"CADInterface initialized.")

    @abstractmethod
    def create_design(self, design_params):
        """Creates a new design based on parameters."""
        pass

    @abstractmethod
    def load_model(self, model_path):
        """Loads an existing CAD model."""
        pass

    @abstractmethod
    def export_model(self, export_format='stl', output_path=None):
        """Exports the current model to a specified format."""
        pass

    @abstractmethod
    def modify_feature(self, feature_name, parameters):
        """Modifies an existing feature in the model."""
        pass

    @abstractmethod
    def get_model_info(self):
        """Retrieves information about the current model (e.g., dimensions, mass)."""
        pass
