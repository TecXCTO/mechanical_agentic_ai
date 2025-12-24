import os
import json

def load_json(filepath):
    """Loads JSON data from a file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON from {filepath}: {e}")
    except IOError as e:
        raise IOError(f"Error reading file {filepath}: {e}")

def save_json(data, filepath):
    """Saves data to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise IOError(f"Error writing JSON to {filepath}: {e}")

def convert_to_list(item):
    """Ensures an item is a list, wrapping it if it's a single element."""
    if isinstance(item, list):
        return item
    return [item]

# Add more utility functions as needed
