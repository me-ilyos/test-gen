"""
Logging module for the test question checker bot.

This module configures and provides logging functionality to track user interactions,
file uploads, and document generation throughout the application.
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Configure root logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Create logger for this module
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Add file handler to write logs to a file
file_handler = logging.FileHandler(
    f"logs/bot_{datetime.now().strftime('%Y-%m-%d')}.log"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

# Get the root logger and add our file handler
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)


def log_user_start(user_id: int, username: Optional[str], full_name: str) -> None:
    """
    Log when a user starts a conversation with the bot.

    Args:
        user_id: Telegram user ID
        username: Telegram username (if available)
        full_name: User's full name
    """
    logger.info(
        f"User started conversation - ID: {user_id}, "
        f"Username: {username or 'Not provided'}, Name: {full_name}"
    )


def log_user_help(user_id: int, username: Optional[str]) -> None:
    """
    Log when a user requests help.

    Args:
        user_id: Telegram user ID
        username: Telegram username (if available)
    """
    logger.info(
        f"User requested help - ID: {user_id}, Username: {username or 'Not provided'}"
    )


def log_file_received(
    user_id: int, username: Optional[str], file_name: str, file_size: int
) -> None:
    """
    Log when a user uploads a file.

    Args:
        user_id: Telegram user ID
        username: Telegram username (if available)
        file_name: Name of the uploaded file
        file_size: Size of the file in bytes
    """
    logger.info(
        f"File received - User ID: {user_id}, Username: {username or 'Not provided'}, "
        f"File: {file_name}, Size: {_format_file_size(file_size)}"
    )


def log_duplicate_check(
    user_id: int, has_duplicates: bool, num_duplicates: int = 0
) -> None:
    """
    Log the results of duplicate checking.

    Args:
        user_id: Telegram user ID
        has_duplicates: Whether duplicates were found
        num_duplicates: Number of duplicates found (if any)
    """
    if has_duplicates:
        logger.info(
            f"Duplicate check for User ID: {user_id} - "
            f"Found {num_duplicates} duplicates"
        )
    else:
        logger.info(f"Duplicate check for User ID: {user_id} - No duplicates found")


def log_format_selection(
    user_id: int, username: Optional[str], format_type: str
) -> None:
    """
    Log when a user selects a format.

    Args:
        user_id: Telegram user ID
        username: Telegram username (if available)
        format_type: The format selected by the user
    """
    logger.info(
        f"Format selected - User ID: {user_id}, Username: {username or 'Not provided'}, "
        f"Format: {format_type}"
    )


def log_file_generated(user_id: int, format_type: str, file_name: str) -> None:
    """
    Log when a file is generated and sent to a user.

    Args:
        user_id: Telegram user ID
        format_type: The format of the generated file
        file_name: Name of the generated file
    """
    logger.info(
        f"File generated - User ID: {user_id}, Format: {format_type}, File: {file_name}"
    )


def log_generation_complete(user_id: int, num_files_generated: int) -> None:
    """
    Log when the file generation process is complete.

    Args:
        user_id: Telegram user ID
        num_files_generated: Number of files generated
    """
    logger.info(
        f"Generation complete - User ID: {user_id}, Files generated: {num_files_generated}"
    )


def log_error(user_id: int, error_type: str, error_message: str) -> None:
    """
    Log errors that occur during bot operation.

    Args:
        user_id: Telegram user ID
        error_type: Type of error
        error_message: Error message
    """
    logger.error(
        f"Error - User ID: {user_id}, Type: {error_type}, Message: {error_message}"
    )


def _format_file_size(size_bytes: int) -> str:
    """
    Format file size from bytes to a human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted file size string
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024 or unit == "GB":
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
