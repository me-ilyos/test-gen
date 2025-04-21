"""
Log viewer utility for the test question checker bot.

This script provides a simple command-line interface to view and filter the bot logs.
"""

import os
import argparse
import datetime
import sys
from typing import List, Optional


def list_log_files(logs_dir: str = "logs") -> List[str]:
    """
    List all log files in the logs directory.

    Args:
        logs_dir: Path to the logs directory

    Returns:
        List of log file paths
    """
    if not os.path.exists(logs_dir):
        print(f"Logs directory '{logs_dir}' does not exist.")
        return []

    log_files = [
        os.path.join(logs_dir, f)
        for f in os.listdir(logs_dir)
        if f.startswith("bot_") and f.endswith(".log")
    ]

    # Sort by date (newest first)
    log_files.sort(reverse=True)

    return log_files


def read_log_file(
    log_path: str,
    user_id: Optional[int] = None,
    keywords: List[str] = None,
    max_entries: int = 100,
) -> List[str]:
    """
    Read and filter entries from a log file.

    Args:
        log_path: Path to the log file
        user_id: Optional user ID to filter by
        keywords: Optional list of keywords to filter by
        max_entries: Maximum number of entries to return

    Returns:
        List of filtered log entries
    """
    if not os.path.exists(log_path):
        print(f"Log file '{log_path}' does not exist.")
        return []

    entries = []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                # Apply filters
                if (
                    user_id
                    and f"User ID: {user_id}" not in line
                    and f"ID: {user_id}" not in line
                ):
                    continue

                if keywords:
                    if not any(keyword.lower() in line.lower() for keyword in keywords):
                        continue

                entries.append(line.strip())

                if len(entries) >= max_entries:
                    break
    except Exception as e:
        print(f"Error reading log file: {e}")

    return entries


def display_log_summary(log_entries: List[str]) -> None:
    """
    Display a summary of log entries.

    Args:
        log_entries: List of log entries to display
    """
    if not log_entries:
        print("No matching log entries found.")
        return

    for entry in log_entries:
        print(entry)

    print(f"\nTotal entries: {len(log_entries)}")


def main() -> None:
    """
    Main function to parse arguments and display logs.
    """
    parser = argparse.ArgumentParser(description="Test Question Checker Bot Log Viewer")

    parser.add_argument("--date", help="View logs for a specific date (YYYY-MM-DD)")
    parser.add_argument("--user", type=int, help="Filter logs by user ID")
    parser.add_argument("--keywords", nargs="+", help="Filter logs by keywords")
    parser.add_argument(
        "--max", type=int, default=100, help="Maximum number of entries to display"
    )
    parser.add_argument("--list", action="store_true", help="List available log files")

    args = parser.parse_args()

    if args.list:
        log_files = list_log_files()
        if log_files:
            print("Available log files:")
            for i, log_file in enumerate(log_files, 1):
                print(f"{i}. {os.path.basename(log_file)}")
        return

    # Determine which log file to read
    if args.date:
        try:
            date_obj = datetime.datetime.strptime(args.date, "%Y-%m-%d")
            log_filename = f"bot_{args.date}.log"
            log_path = os.path.join("logs", log_filename)
        except ValueError:
            print(f"Invalid date format. Please use YYYY-MM-DD.")
            return
    else:
        # Use the most recent log file
        log_files = list_log_files()
        if not log_files:
            print("No log files found.")
            return
        log_path = log_files[0]

    # Read and display log entries
    log_entries = read_log_file(
        log_path, user_id=args.user, keywords=args.keywords, max_entries=args.max
    )

    display_log_summary(log_entries)


if __name__ == "__main__":
    main()
