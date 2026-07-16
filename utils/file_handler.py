import json
import os

def read_json(filepath, default = None):
    
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
        return data

    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Returning empty data.")
        return default if default is not None else {}

    except json.JSONDecodeError:
        print(f"Warning: {filepath} is corrupted or empty. Returning empty data.")
        return default if default is not None else {}

    except PermissionError:
        print(f"Error: No permission to read {filepath}.")
        return default if default is not None else {}


def write_json(filepath, data):
    
    try:
        
        folder = os.path.dirname(filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
        return True

    except PermissionError:
        print(f"Error: No permission to write to {filepath}.")
        return False

    except TypeError as e:
        print(f"Error: Data is not JSON-serializable — {e}")
        return False

