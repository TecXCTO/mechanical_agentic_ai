from src.agents.base_agent import BaseAgent

class DesignAgent(BaseAgent):
    def __init__(self, name="DesignAgent", config=None, cad_interface=None):
        super().__init__(name, config)
        self.cad_interface = cad_interface
        if not self.cad_interface:
            print("Warning: No CAD interface provided to DesignAgent.")

    def perceive(self, observation):
        print(f"{self.name} perceiving: {observation}")
        # Update internal state based on observation
        pass

    def plan(self):
        print(f"{self.name} planning for goal: {self.current_goal}")
        # Logic to determine design actions
        if self.current_goal and "design" in self.current_goal.lower():
            return "create_new_design"
        return "wait"

    def act(self, action):
        print(f"{self.name} acting: {action}")
        if action == "create_new_design" and self.cad_interface:
            try:
                # Example: Use config for design parameters
                design_params = self.config.get('design_params', {{'type': 'bracket', 'size': 'medium'}})
                design_path = self.cad_interface.create_design(design_params)
                print(f"Design created at: {design_path}")
                self.state = "completed"
                return design_path
            except Exception as e:
                print(f"Error during design creation: {e}")
                self.state = "error"
                return None
        elif action == "wait":
            self.state = "idle"
            return None
        else:
            print(f"Action '{action}' not supported or CAD interface missing.")
            self.state = "error"
            return None
