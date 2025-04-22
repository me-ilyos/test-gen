"""
Helper utility functions for the test question converter bot.

This file contains utility functions used across the application for common
tasks like loading environment variables and handling file paths.
"""

import os
from dotenv import load_dotenv
from typing import Dict


def load_environment_variables() -> Dict[str, str]:
    """
    Load environment variables from .env file.

    Returns:
        Dictionary containing environment variables
    """
    # Load variables from .env file if it exists
    load_dotenv()

    # Return relevant environment variables
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN", ""),
    }


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure that the specified directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory to check/create
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_file_name_without_extension(file_path: str) -> str:
    """
    Get the file name without extension from a file path.

    Args:
        file_path: Path to the file

    Returns:
        File name without extension
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def format_file_size(size_bytes: int) -> str:
    """
    Format file size from bytes to a human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted file size string (e.g., "2.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024 or unit == "GB":
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
