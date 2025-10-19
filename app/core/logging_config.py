# app/core/logging_config.py
import logging

# Nivel de logging
LOG_LEVEL = logging.INFO

# Formato
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
