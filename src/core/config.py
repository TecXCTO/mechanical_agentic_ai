import yaml
import os

class ConfigManager:
    def __init__(self, config_dir="data/config"):
        self.config_dir = config_dir
        self.configs = {}
        self.load_all_configs()

    def load_all_configs(self):
        if not os.path.exists(self.config_dir):
            print(f"Config directory not found: {self.config_dir}")
            return

        for filename in os.listdir(self.config_dir):
            if filename.endswith(('.yaml', '.yml')):
                filepath = os.path.join(self.config_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        self.configs[os.path.splitext(filename)[0]] = yaml.safe_load(f)
                    print(f"Loaded config: {filename}")
                except Exception as e:
                    print(f"Error loading config {filename}: {e}")

    def get(self, key, default=None):
        """Get a configuration value. Supports dot notation for nested keys."""
        keys = key.split('.')
        value = self.configs
        try:
            for k in keys:
                if isinstance(value, dict):
                    value = value[k]
                else: # Handle list indices if necessary, e.g. key='list.0.item'
                    value = value[int(k)]
            return value
        except (KeyError, IndexError, TypeError):
            return default

    def get_section(self, section_name, default={}):
        return self.configs.get(section_name, default)

# Example usage:
# config_manager = ConfigManager()
# design_params = config_manager.get('design_agent.design_params')
# simulation_type = config_manager.get_section('simulation_agent').get('simulation_type')
