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
    """Parse a text file containing test questions and answer variants."""
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(input_path, "r", encoding="cp1251") as file:
            content = file.read()

    # Split by double newlines to separate questions
    question_blocks = content.split("\n\n")
    questions = []
    
    for i, block in enumerate(question_blocks):
        if not block.strip():
            continue  # Skip empty blocks
            
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
            
        # First line is the question
        question_text = lines[0]
        
        # Initialize question object
        question = {
            "id": i + 1,
            "text": question_text,
            "variants": [],
            "correct": None,
        }
        
        # Process answer options
        variant_pattern = re.compile(r"^([a-d])\)\s*(\*?)(.+)$")
        for line in lines[1:]:
            variant_match = variant_pattern.match(line)
            if variant_match:
                variant_letter = variant_match.group(1)
                is_correct = bool(variant_match.group(2))
                variant_text = variant_match.group(3).strip()
                
                # Convert letter to number (a->1, b->2, etc.)
                variant_id = ord(variant_letter) - ord('a') + 1
                
                # Add variant
                question["variants"].append({
                    "id": variant_id, 
                    "text": variant_text
                })
                
                # Mark as correct if it has an asterisk
                if is_correct:
                    question["correct"] = variant_id
        
        # Only add if we have both a question and variants
        if question["text"] and question["variants"]:
            questions.append(question)
    
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