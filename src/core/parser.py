"""
Question parser module for test question format converter.

This file contains functions for parsing test questions from text and JSON files.
It extracts question text, answer variants, and correct answer markers.
"""

import json
import re
import os
from typing import Dict, List, Optional


def parse_text_file(input_path: str) -> Dict:
    """
    Parse a text file containing test questions and answer variants.

    Args:
        input_path: Path to the text file

    Returns:
        Dictionary with parsed questions data
    """
    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split content into lines and remove empty lines
    lines = [line.strip() for line in content.split("\n") if line.strip()]

    questions = []
    current_question = None

    # Common regex patterns
    question_pattern = re.compile(r"(\d+)\.?\s+(.*)")
    # Support both a) and a. format for variants
    variant_pattern = re.compile(r"([a-z])[\.|\)]\s*(\*?)(.+)")

    for line in lines:
        # Check if line is a question
        question_match = question_pattern.match(line)
        if question_match:
            # Save previous question if exists
            if current_question:
                questions.append(current_question)

            # Create new question
            question_number = int(question_match.group(1))
            question_text = question_match.group(2).strip()

            current_question = {
                "id": question_number,
                "text": question_text,
                "variants": [],
                "correct": None,
            }
            continue

        # Check if line is an answer variant
        variant_match = variant_pattern.match(line)
        if variant_match and current_question is not None:
            variant_letter = variant_match.group(1)
            is_correct = bool(variant_match.group(2))
            variant_text = variant_match.group(3).strip()

            # Convert letter to number (a->1, b->2, etc.)
            variant_id = ord(variant_letter) - ord("a") + 1

            # Add variant to current question
            current_question["variants"].append(
                {"id": variant_id, "text": variant_text}
            )

            # Mark as correct if it has an asterisk
            if is_correct:
                current_question["correct"] = variant_id
        elif not current_question:
            # If we encounter text before any question number,
            # assume it's an unnumbered question
            current_question = {"id": 1, "text": line, "variants": [], "correct": None}

    # Add the last question
    if current_question:
        questions.append(current_question)

    return {"questions": questions}


def parse_json_file(input_path: str) -> Dict:
    """
    Parse a JSON file containing test questions data.

    Args:
        input_path: Path to the JSON file

    Returns:
        Dictionary with parsed questions data
    """
    with open(input_path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_input_file(input_path: str) -> Dict:
    """
    Parse an input file based on its file extension.

    Args:
        input_path: Path to the input file

    Returns:
        Dictionary with parsed questions data
    """
    _, file_extension = os.path.splitext(input_path)

    if file_extension.lower() == ".json":
        return parse_json_file(input_path)
    else:
        return parse_text_file(input_path)
