import argparse
from src.agents.design_agent import DesignAgent
from src.modules.cad.solidworks import SolidWorksInterface # Example
from src.core.config import ConfigManager

def main():
    parser = argparse.ArgumentParser(description="Generate CAD models using the Design Agent.")
    parser.add_argument('--output_filename', type=str, default='generated_design.stl', help='Filename for the generated CAD model.')
    parser.add_argument('--config', type=str, default='data/config/design_agent.yaml', help='Path to design agent configuration file.')
    args = parser.parse_args()

    # Load configurations
    config_manager = ConfigManager(config_dir="data/config")
    design_agent_config = config_manager.get_section('design_agent')
    # Merge specific config if provided
    if args.config != 'data/config/design_agent.yaml':
        specific_config_manager = ConfigManager(config_dir=os.path.dirname(args.config))
        design_agent_config.update(specific_config_manager.get_section(os.path.basename(args.config).split('.')[0]))

    # Initialize CAD Interface (example using SolidWorks)
    # You might need to pass actual paths or settings from config
    cad_interface = SolidWorksInterface(config=design_agent_config.get('cad_settings'))

    # Initialize Design Agent
    design_agent = DesignAgent(cad_interface=cad_interface, config=design_agent_config)

    # Set goal and prepare parameters
    design_agent.set_goal(f"Create CAD model {args.output_filename}")
    # The design parameters are expected to be in the agent's config
    # If you need to override, you could pass them directly:
    # design_params = {'type': 'custom', 'size': 'large'}
    # design_agent.current_goal = design_params # Or pass via set_goal

    # Manually trigger act with the design creation action
    # In a real scenario, this might be part of a larger orchestration
    print(f"Attempting to create design with parameters: {design_agent_config.get('design_params')}")
    # The create_design action uses parameters from the agent's config
    design_path = design_agent.act("create_new_design")

    if design_path:
        print(f"CAD model generated successfully: {design_path}")
        # Optionally export to a specific file if needed
        # exported_file = cad_interface.export_model(export_format=args.output_filename.split('.')[-1], output_path=args.output_filename)
        # print(f"Exported to {exported_file}")
    else:
        print("CAD model generation failed.")

if __name__ == '__main__':
    main()
