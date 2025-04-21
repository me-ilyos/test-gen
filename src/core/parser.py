"""
Question parser module for test question format converter.

This file contains functions for parsing test questions from text and JSON files.
It extracts question text, answer variants, and correct answer markers from
formatted input files.
"""

import json
import re
import os
from typing import Dict, List, Optional, Any


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

    # Split content into lines and parse questions
    lines = [line.strip() for line in content.split("\n")]

    # Try to determine if the file has numbered questions or not
    has_numbered_questions = any(re.match(r"^\d+\.\s+.+", line) for line in lines)

    if has_numbered_questions:
        return _parse_numbered_question_lines(lines)
    else:
        return _parse_unnumbered_question_lines(lines)


def _parse_numbered_question_lines(lines: List[str]) -> Dict:
    """
    Parse lines of text into structured question data where questions have numbers.

    Args:
        lines: List of text lines from input file

    Returns:
        Dictionary with parsed questions data
    """
    # Filter out empty lines
    lines = [line for line in lines if line]

    questions = []
    current_question = None
    question_pattern = r"(\d+)\.\s+(.*)"
    variant_pattern = r"([a-z])\)\s+(\*?)(.+)"

    for line in lines:
        # Check if line is a question
        question_match = re.match(question_pattern, line)
        if question_match:
            # Save previous question if exists
            if current_question:
                questions.append(current_question)

            # Create new question
            current_question = _create_question_dict(question_match)
            continue

        # Check if line is an answer variant
        if current_question is not None:
            variant_match = re.match(variant_pattern, line)
            if variant_match:
                _add_variant_to_question(current_question, variant_match)

    # Add the last question
    if current_question:
        questions.append(current_question)

    return {"questions": questions}


def _parse_unnumbered_question_lines(lines: List[str]) -> Dict:
    """
    Parse lines of text into structured question data where questions don't have numbers.

    Args:
        lines: List of text lines from input file

    Returns:
        Dictionary with parsed questions data
    """
    # Filter out empty lines
    lines = [line for line in lines if line]

    questions = []
    current_question = None
    variant_pattern = r"([a-z])\)\s+(\*?)(.+)"
    variant_count = 0
    question_id = 1

    for line in lines:
        # Check if line is an answer variant
        variant_match = re.match(variant_pattern, line)

        if variant_match:
            variant_count += 1

            # If this is the first variant and we have text stored
            if variant_count == 1 and current_question is not None:
                # Add the current question's variants
                _add_variant_to_question(current_question, variant_match)
            elif current_question is not None:
                # Add more variants to existing question
                _add_variant_to_question(current_question, variant_match)
        else:
            # If we've been collecting variants and find a non-variant line,
            # it's probably a new question
            if variant_count > 0:
                if current_question:
                    questions.append(current_question)
                variant_count = 0

            # If the line isn't a variant, it's likely a question text
            current_question = {
                "id": question_id,
                "text": line.strip(),
                "variants": [],
                "correct": None,
            }
            question_id += 1

    # Add the last question
    if current_question:
        questions.append(current_question)

    return {"questions": questions}


def _create_question_dict(question_match: re.Match) -> Dict:
    """
    Create a question dictionary from regex match.

    Args:
        question_match: Regex match object for question line

    Returns:
        Dictionary with question data structure
    """
    question_number = int(question_match.group(1))
    question_text = question_match.group(2).strip()

    return {
        "id": question_number,
        "text": question_text,
        "variants": [],
        "correct": None,
    }


def _add_variant_to_question(question: Dict, variant_match: re.Match) -> None:
    """
    Add answer variant to question from regex match.

    Args:
        question: Question dictionary to update
        variant_match: Regex match object for variant line
    """
    variant_letter = variant_match.group(1)
    is_correct = bool(variant_match.group(2))
    variant_text = variant_match.group(3).strip()

    variant_id = ord(variant_letter) - ord("a") + 1
    question["variants"].append({"id": variant_id, "text": variant_text})

    if is_correct:
        question["correct"] = variant_id


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
