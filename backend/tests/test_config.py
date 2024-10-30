# test_config.py
import sys
import os

# Add the backend directory to sys.path to locate app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.core.config import settings

def print_settings():
    """
    Prints the configuration settings to confirm they are loading correctly.
    """
    try:
        # Convert settings to a dictionary and print each key-value pair
        settings_dict = settings.dict()
        print("Configuration Settings:")
        for key, value in settings_dict.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error loading settings: {e}")

if __name__ == "__main__":
    print_settings()
