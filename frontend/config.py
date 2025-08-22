"""Configuration settings for the frontend application."""

import json
import os
from dotenv import load_dotenv

load_dotenv()
env = os.getenv

MODEL_OPTIONS = {
    "Claude 3 Haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    "Claude 3.5 Sonnet": "anthropic.claude-3-5-sonnet-20240620-v1:0",
}

config_path = os.path.join(".", "servers_config.json")
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        SERVER_CONFIG = json.load(f)
