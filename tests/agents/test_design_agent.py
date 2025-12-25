import unittest
from unittest.mock import MagicMock
from src.agents.design_agent import DesignAgent

class TestDesignAgent(unittest.TestCase):
    def setUp(self):
        # Mock the CAD interface
        self.mock_cad_interface = MagicMock()
        # Configure the mock to return a dummy path when create_design is called
        self.mock_cad_interface.create_design.return_value = "/path/to/mock/design.stl"

        # Instantiate the DesignAgent with the mock
        self.design_agent = DesignAgent(cad_interface=self.mock_cad_interface)

    def test_set_goal(self):
        self.design_agent.set_goal("Design a bracket")
        self.assertEqual(self.design_agent.current_goal, "Design a bracket")
        self.assertEqual(self.design_agent.state, "ready")

    def test_plan_action_create_design(self):
        self.design_agent.set_goal("Create a new design")
        action = self.design_agent.plan()
        self.assertEqual(action, "create_new_design")

    def test_plan_action_wait(self):
        self.design_agent.set_goal("Do nothing") # Example of a goal that might not trigger design
        action = self.design_agent.plan()
        self.assertEqual(action, "wait")

    def test_act_create_design(self):
        self.design_agent.set_goal("Create a new design")
        # Call plan first to get the action
        action = self.design_agent.plan()
        result = self.design_agent.act(action)

        # Assert that the mock CAD interface's create_design was called
        self.mock_cad_interface.create_design.assert_called_once()
        # Assert the result is the path returned by the mock
        self.assertEqual(result, "/path/to/mock/design.stl")
        self.assertEqual(self.design_agent.state, "completed")

    def test_act_create_design_with_config(self):
        mock_config = {"design_params": {"type": "gear", "teeth": 32}}
        self.design_agent = DesignAgent(cad_interface=self.mock_cad_interface, config=mock_config)
        self.design_agent.set_goal("Create a new design")
        action = self.design_agent.plan()
        result = self.design_agent.act(action)

        # Assert that create_design was called with the correct parameters
        self.mock_cad_interface.create_design.assert_called_once_with({"type": "gear", "teeth": 32})
        self.assertEqual(result, "/path/to/mock/design.stl")

    def test_act_wait(self):
        action = "wait"
        result = self.design_agent.act(action)
        self.assertIsNone(result)
        self.assertEqual(self.design_agent.state, "idle")

    def test_act_without_cad_interface(self):
        no_cad_agent = DesignAgent()
        no_cad_agent.set_goal("Create a design")
        action = no_cad_agent.plan()
        result = no_cad_agent.act(action)
        self.assertIsNone(result)
        self.assertEqual(no_cad_agent.state, "error")

if __name__ == '__main__':
    unittest.main()
