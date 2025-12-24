from abc import ABC, abstractmethod

class RobotInterface(ABC):
    """Abstract base class for robot control systems."""
    def __init__(self, config=None):
        self.config = config or {}
        print(f"RobotInterface initialized.")

    @abstractmethod
    def connect(self, ip_address):
        """Connects to the robot controller."""
        pass

    @abstractmethod
    def execute(self, task_data):
        """Executes a given task (e.g., move, pick, place, weld)."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnects from the robot controller."""
        pass
