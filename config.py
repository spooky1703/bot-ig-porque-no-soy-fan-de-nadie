"""
Bot IG - Configuration Module
Loads environment variables and defines constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
SESSION_FILE = BASE_DIR / os.getenv("SESSION_FILE", "session.json")

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")

# Rate limiting configuration (in seconds)
MIN_DELAY = float(os.getenv("MIN_DELAY", "1.0"))
MAX_DELAY = float(os.getenv("MAX_DELAY", "3.0"))

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)
