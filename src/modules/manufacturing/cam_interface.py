from abc import ABC, abstractmethod

class CAMInterface(ABC):
    """Abstract base class for CAM software integrations."""
    def __init__(self, config=None):
        self.config = config or {}
        print(f"CAMInterface initialized.")

    @abstractmethod
    def generate_toolpath(self, design_path, process_params):
        """Generates toolpaths for manufacturing the design."""
        pass

    @abstractmethod
    def optimize_toolpath(self, toolpath_data):
        """Optimizes an existing toolpath for efficiency or quality."""
        pass
