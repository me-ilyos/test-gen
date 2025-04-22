"""
Simple duplicate question detector.

This file contains functions for identifying duplicate questions and
duplicate answer options within questions.
"""

from typing import Dict, List, Tuple


def check_for_duplicates(json_data: Dict) -> str:
    """
    Check for duplicate questions and duplicate options within questions.

    Args:
        json_data: Dictionary containing questions data

    Returns:
        A report string describing any duplicates found
    """
    results = []
    questions = json_data["questions"]

    # Check for duplicate questions
    question_texts = {}
    for i, question in enumerate(questions):
        text = question["text"].lower()
        if text in question_texts:
            results.append(
                f"IDENTICAL QUESTIONS FOUND:\n"
                f"Question {question['id']} and Question {question_texts[text]['id']} - 100% identical\n"
                f"  Q{question_texts[text]['id']}: {question_texts[text]['text']}\n"
                f"  Q{question['id']}: {question['text']}\n"
            )
        else:
            question_texts[text] = question

    # Check for duplicate options within the same question
    for question in questions:
        option_texts = {}
        for option in question["variants"]:
            text = option["text"].lower()
            if text in option_texts:
                results.append(
                    f"IDENTICAL OPTIONS WITHIN THE SAME QUESTION FOUND:\n"
                    f"In Question {question['id']} - Options {chr(96 + option_texts[text]['id'])} "
                    f"and {chr(96 + option['id'])} are 100% identical\n"
                    f"  Q{question['id']}: {question['text']}\n"
                    f"    {chr(96 + option_texts[text]['id'])}) {option_texts[text]['text']}\n"
                    f"    {chr(96 + option['id'])}) {option['text']}\n"
                )
            else:
                option_texts[text] = option

    if not results:
        return "No duplicate or similar content found."

    return "\n".join(results)
