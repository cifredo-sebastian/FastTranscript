import os
import json
import platform

CONFIG_FILE_NAME = 'config.json'

def get_config_path():
    system = platform.system()
    if system == "Windows":
        config_dir = os.path.join(os.getenv('LOCALAPPDATA'), "MyApp")
    elif system == "Darwin":  # macOS
        config_dir = os.path.join(os.path.expanduser('~'), "Library", "Application Support", "MyApp")
    else:  # Linux or other Unix-like systems
        config_dir = os.path.join(os.path.expanduser('~'), ".config", "MyApp")

    # Create the directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Return the full path to config.json
    return os.path.join(config_dir, CONFIG_FILE_NAME)

def get_config_path():
    ############################################################################################ THIS IS TEMPORARY - DEV ###########################################################################################
    # Save the config in the project directory for development
    return CONFIG_FILE_NAME

def load_config():
    config_path = get_config_path()
    # config_path = "config.json"

    # Default config settings
    config = {
        "api_key": "",
        "transcription": {
            "speaker_labels": False,
            "language_code": "en"
        }
    }

    # Load the config if the file exists
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            print(f"config loaded: {config}")

    return config

def save_config(config):
    config_path = get_config_path()
    # config_path = "config.json"
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)
    print(f"Saved config to {config_path}: {config}")
