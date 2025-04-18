"""
Helper utility functions for the test question checker bot.

This file contains utility functions used across the application for common
tasks like parsing command line arguments, handling file paths, and loading
environment variables.
"""

import os
import sys
import logging
from typing import Dict, Tuple, Any, List, Optional
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)


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
        "TELEGRAM_BOT_TOKEN": os.getenv("BOT_TOKEN", ""),
    }


def parse_command_line_args() -> Tuple[str, str, str, Dict[str, bool]]:
    """
    Parse command line arguments for the CLI tool.
    
    Returns:
        Tuple containing (input_path, output_folder, output_name, formats)
        where formats is a dictionary of enabled output formats.
    
    Raises:
        SystemExit: If required arguments are missing or input file doesn't exist.
    """
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    input_path = sys.argv[1]
    output_folder = sys.argv[2]
    output_name = sys.argv[3]

    if not os.path.exists(input_path):
        logger.error(f"Input file {input_path} does not exist")
        sys.exit(1)

    # Default to all formats
    formats = {"student": True, "program": True, "word": True}

    if len(sys.argv) > 4:
        arg = sys.argv[4].lower()

        format_options = {
            "--help": None,  # Special case, handled below
            "-a": {"student": True, "program": True, "word": True},
            "--all": {"student": True, "program": True, "word": True},
            "-s": {"student": True, "program": False, "word": False},
            "--student": {"student": True, "program": False, "word": False},
            "-h": {"student": False, "program": True, "word": False},
            "--hemis": {"student": False, "program": True, "word": False},
            "-w": {"student": False, "program": False, "word": True},
            "--word": {"student": False, "program": False, "word": True}
        }

        if arg in format_options:
            if arg == "--help":
                print_usage()
                sys.exit(0)
            else:
                formats = format_options[arg]
        else:
            print(f"Unknown option: {arg}")
            print_usage()
            sys.exit(1)

    return input_path, output_folder, output_name, formats


def print_usage() -> None:
    """
    Print command line usage instructions.
    """
    print("Usage: python main.py input_path output_folder output_name [options]")
    print("Options:")
    print("  -a, --all       Generate all formats (default)")
    print("  -s, --student   Generate only student formats (with and without variants)")
    print("  -h, --hemis     Generate only program format")
    print("  -w, --word      Generate only Word document format")
    print("  --help          Show this help message")


def get_output_paths(output_folder: str, output_name: str) -> Dict[str, str]:
    """
    Generate paths for output files.
    
    Args:
        output_folder: Folder to store output files
        output_name: Base name for output files
        
    Returns:
        Dictionary with paths for different output formats
    """
    name_without_ext = os.path.splitext(output_name)[0]
    
    # Use dictionary comprehension for clarity
    base_filenames = {
        "student": f"{name_without_ext}TalabaVariant.txt",
        "student_novariant": f"{name_without_ext}TalabaNovariant.txt",
        "program": f"{name_without_ext}Hemis.txt",
        "word": f"{name_without_ext}Yakuniy.docx",
    }
    
    return {
        format_key: os.path.join(output_folder, filename)
        for format_key, filename in base_filenames.items()
    }


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure that the specified directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory to check/create
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Created directory: {directory_path}")