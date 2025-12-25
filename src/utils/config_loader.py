
import os

class ConfigLoader:
    @staticmethod
    def load_config():
        # Example: Load from environment variables or a config file
        config = {
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "data_dir": os.getenv("DATA_DIR", "./data")
        }
        print(f"Loaded config: {config}")
        return config
