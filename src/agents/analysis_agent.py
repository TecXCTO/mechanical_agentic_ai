from src.agents.base_agent import BaseAgent

class AnalysisAgent(BaseAgent):
    def __init__(self, name="AnalysisAgent", config=None, analysis_module=None):
        super().__init__(name, config)
        self.analysis_module = analysis_module
        if not self.analysis_module:
            print("Warning: No Analysis module provided to AnalysisAgent.")

    def perceive(self, observation):
        print(f"{self.name} perceiving: {observation}")
        # Observation might be a path to simulation results
        self.results_file = observation
        pass

    def plan(self):
        print(f"{self.name} planning for goal: {self.current_goal}")
        if self.results_file and self.analysis_module:
            return "perform_analysis"
        return "wait"

    def act(self, action):
        print(f"{self.name} acting: {action}")
        if action == "perform_analysis" and self.results_file and self.analysis_module:
            try:
                analysis_config = self.config.get('analysis_params', {{'metrics': ['stress', 'displacement']}})
                analysis_results = self.analysis_module.analyze(self.results_file, analysis_config)
                print(f"Analysis complete. Results: {analysis_results}")
                self.state = "completed"
                return analysis_results
            except Exception as e:
                print(f"Error during analysis: {e}")
                self.state = "error"
                return None
        elif action == "wait":
            self.state = "idle"
            return None
        else:
            print(f"Action '{action}' not supported or analysis module missing/results file not provided.")
            self.state = "error"
            return None
