#
#//  loader.py
#//  
#//
#//  Created by ytguest on 2/3/26.
#//
"""
Configuration loader for service monitor.
- load_config: loads raw JSON from file
- parse_config: extracts services and validates fields
- Stores parsed configuration in global memory for easy access
"""

import json
import os

# Global memory for configuration
CONFIG = {
    "services": []
}

def load_config(path: str) -> dict:
    """
    Load configuration file from JSON.
    Args:
        path (str): Path to configuration file
    Returns:
        dict: Raw JSON configuration
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with open(path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {path}: {e}")
    return config


def parse_config(config: dict) -> None:
    """
    Parse configuration dictionary, extract services.
    Updates global CONFIG.
    Args:
        config (dict): Raw configuration dictionary
    """
    services = []

    # Validate and extract service entries from "services" array
    if "services" not in config or not isinstance(config["services"], list):
        raise ValueError("Configuration must contain a 'services' list")

    for entry in config["services"]:
        if not isinstance(entry, dict):
            raise ValueError(f"Invalid service entry: {entry}")
        
        name = entry.get("name")
        uri = entry.get("uri")
        expected_version = entry.get("expected_version", None)
        interval_check = int(entry.get("interval_check", 60))

        if not name or not uri:
            raise ValueError(f"Service entry missing required fields: {entry}")

        services.append({
            "name": name,
            "uri": uri,
            "expected_version": expected_version,
            "interval_check": interval_check
        })

    CONFIG["services"] = services


def get_services() -> list:
    """
    Access parsed services from global CONFIG.
    Returns:
        list: List of service dictionaries
    """
    return CONFIG["services"]


# Example usage for testing
#if __name__ == "__main__":
#    raw_config = load_config("../services.json")
#    parse_config(raw_config)
#
#    services = get_services()
#    for item in services:
#        print(item)
#        print()

