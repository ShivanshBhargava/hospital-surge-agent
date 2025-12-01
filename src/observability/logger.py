# src/observability/logger.py
import logging
import os

LOG_FILE = "data/agent.log"

# Create directory if missing
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("hospital_agent")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger.addHandler(file_handler)
