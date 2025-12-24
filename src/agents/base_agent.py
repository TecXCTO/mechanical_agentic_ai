from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name="BaseAgent", config=None):
        self.name = name
        self.config = config or {}
        self.current_goal = None
        self.state = "idle"
        print(f"{self.name} initialized.")

    def set_goal(self, goal):
        self.current_goal = goal
        self.state = "ready"
        print(f"{self.name} received goal: {self.current_goal}")

    @abstractmethod
    def perceive(self, observation):
        """Processes current observation from the environment."""
        pass

    @abstractmethod
    def plan(self):
        """Determines the next action based on the current goal and state."""
        pass

    @abstractmethod
    def act(self):
        """Executes the planned action."""
        pass

    def run(self, observation):
        if self.state == "idle" and self.current_goal is None:
            print(f"{self.name} is idle.")
            return None

        self.state = "processing"
        self.perceive(observation)
        action = self.plan()
        result = self.act(action)
        self.state = "idle" # Reset state after action, or manage state transitions more complexly
        return result

    def reset(self):
        self.current_goal = None
        self.state = "idle"
        print(f"{self.name} reset.")
