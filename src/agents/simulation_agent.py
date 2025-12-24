from src.agents.base_agent import BaseAgent

class SimulationAgent(BaseAgent):
    def __init__(self, name="SimulationAgent", config=None, sim_interface=None):
        super().__init__(name, config)
        self.sim_interface = sim_interface
        if not self.sim_interface:
            print("Warning: No Simulation interface provided to SimulationAgent.")

    def perceive(self, observation):
        print(f"{self.name} perceiving: {observation}")
        # Observation might be a path to a design file
        self.design_file = observation
        pass

    def plan(self):
        print(f"{self.name} planning for goal: {self.current_goal}")
        if self.design_file and self.sim_interface:
            return "run_simulation"
        return "wait"

    def act(self, action):
        print(f"{self.name} acting: {action}")
        if action == "run_simulation" and self.design_file and self.sim_interface:
            try:
                sim_config = self.config.get('simulation_params', {{'type': 'FEA', 'load': '100N'}})
                results_path = self.sim_interface.run_simulation(self.design_file, sim_config)
                print(f"Simulation complete. Results at: {results_path}")
                self.state = "completed"
                return results_path
            except Exception as e:
                print(f"Error during simulation: {e}")
                self.state = "error"
                return None
        elif action == "wait":
            self.state = "idle"
            return None
        else:
            print(f"Action '{action}' not supported or simulation interface missing/design file not provided.")
            self.state = "error"
            return None
