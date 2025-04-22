"""
Logging configuration for the test question converter bot.

This module configures logging to track bot operations in both console and file.
"""

import logging
import os
from datetime import datetime


def setup_logger() -> logging.Logger:
    """
    Configure and return the application logger.

    Sets up logging to both console and a date-stamped file.

    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # Get the current date for the log file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(logs_dir, f"bot_{current_date}.log")

    # Configure the formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add the handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Create and return a logger for this module
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Writing to {log_file}")

    return logger


# Create the logger on module import
logger = setup_logger()


# Helper functions for standardized log messages
def log_user_action(user_id: int, username: str, action: str) -> None:
    """
    Log a user action with standardized format.

    Args:
        user_id: Telegram user ID
        username: Telegram username
        action: Description of the action
    """
    logger.info(f"User {user_id} ({username or 'No username'}): {action}")


def log_error(user_id: int, error_type: str, details: str) -> None:
    """
    Log an error with standardized format.

    Args:
        user_id: Telegram user ID
        error_type: Type or category of error
        details: Error details or message
    """
    logger.error(f"Error for user {user_id} - {error_type}: {details}")
