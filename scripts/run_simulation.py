import argparse
from src.agents.simulation_agent import SimulationAgent
from src.modules.simulation.ansys import AnsysInterface # Example
from src.core.config import ConfigManager

def main():
    parser = argparse.ArgumentParser(description="Run a simulation using the Simulation Agent.")
    parser.add_argument('--design_file', type=str, required=True, help='Path to the CAD design file to simulate.')
    parser.add_argument('--config', type=str, default='data/config/simulation_agent.yaml', help='Path to simulation configuration file.')
    args = parser.parse_args()

    # Load configurations
    config_manager = ConfigManager(config_dir="data/config")
    sim_config = config_manager.get_section('simulation_agent')
    # If a specific config file is provided, merge it
    if args.config != 'data/config/simulation_agent.yaml':
        specific_config_manager = ConfigManager(config_dir=os.path.dirname(args.config))
        sim_config.update(specific_config_manager.get_section(os.path.basename(args.config).split('.')[0]))

    # Initialize Simulation Interface (example using Ansys)
    # You might need to pass actual paths or settings from config
    sim_interface = AnsysInterface(config=sim_config.get('solver_settings'))

    # Initialize Simulation Agent
    sim_agent = SimulationAgent(sim_interface=sim_interface, config=sim_config)

    # Set goal and perceive the design file
    sim_agent.set_goal(f"Run simulation on {args.design_file}")
    sim_agent.perceive(args.design_file)

    # Run the simulation workflow
    results_path = sim_agent.run(observation=None) # Observation already perceived

    if results_path:
        print(f"Simulation successfully completed. Results: {results_path}")
    else:
        print("Simulation failed.")

if __name__ == '__main__':
    main()
