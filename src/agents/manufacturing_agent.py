from src.agents.base_agent import BaseAgent

class ManufacturingAgent(BaseAgent):
    def __init__(self, name="ManufacturingAgent", config=None, cam_interface=None, robot_interface=None):
        super().__init__(name, config)
        self.cam_interface = cam_interface
        self.robot_interface = robot_interface
        if not self.cam_interface:
            print("Warning: No CAM interface provided to ManufacturingAgent.")
        if not self.robot_interface:
            print("Warning: No Robot interface provided to ManufacturingAgent.")

    def perceive(self, observation):
        print(f"{self.name} perceiving: {observation}")
        # Observation might be a design file or analysis results
        self.design_to_manufacture = observation
        pass

    def plan(self):
        print(f"{self.name} planning for goal: {self.current_goal}")
        # Example: if goal is 'manufacture_part' and we have a design
        if self.design_to_manufacture and self.cam_interface:
            return "generate_toolpath"
        return "wait"

    def act(self, action):
        print(f"{self.name} acting: {action}")
        if action == "generate_toolpath" and self.design_to_manufacture and self.cam_interface:
            try:
                process_params = self.config.get('manufacturing_params', {{'process': '3D_printing'}})
                toolpath_data = self.cam_interface.generate_toolpath(self.design_to_manufacture, process_params)
                print(f"Toolpath generated.")
                # Optional: use robot interface to execute
                if self.robot_interface:
                    print("Executing toolpath with robot...")
                    self.robot_interface.execute(toolpath_data)
                    print("Robot execution complete.")
                self.state = "completed"
                return toolpath_data
            except Exception as e:
                print(f"Error during manufacturing process: {e}")
                self.state = "error"
                return None
        elif action == "wait":
            self.state = "idle"
            return None
        else:
            print(f"Action '{action}' not supported or required interfaces missing.")
            self.state = "error"
            return None
