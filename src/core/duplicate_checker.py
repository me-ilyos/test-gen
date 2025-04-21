"""
Duplicate question detector for test questions.

This file contains functions for identifying similar questions and answer variants
in a set of test questions. It uses sequence matching to calculate text similarity
and generates reports about potential duplicates.
"""

from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional


def find_similar_questions(json_data: Dict, threshold: float = 1.0) -> List[Tuple[int, int, float]]:
    """
    Find similar questions based on text similarity.
    
    Args:
        json_data: Dictionary containing questions data
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        List of tuples with (question1_index, question2_index, similarity_score)
    """
    similar_pairs = []
    questions = json_data["questions"]
    
    # Compare each question with every other question (without redundant comparisons)
    for i in range(len(questions)):
        for j in range(i + 1, len(questions)):
            similarity = _calculate_text_similarity(
                questions[i]["text"].lower(),
                questions[j]["text"].lower()
            )
            
            if similarity >= threshold:
                similar_pairs.append((i, j, similarity))
    
    return similar_pairs


def _calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity ratio between two text strings.
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        Similarity ratio (0.0 to 1.0)
    """
    return SequenceMatcher(None, text1, text2).ratio()


def find_similar_variants(json_data: Dict, threshold: float = 1.0) -> List[Tuple[int, int, int, int, float]]:
    """
    Find similar answer variants across questions.
    
    Note: We no longer use this function since we don't need to check for
    duplicate options across different questions.
    
    This is kept for compatibility but returns an empty list.
    """
    # Return empty list as we don't need to check this
    return []


def find_similar_options_within_question(json_data: Dict, threshold: float = 1.0) -> List[Tuple[int, int, int, float]]:
    """
    Find similar answer options within the same question.
    
    Args:
        json_data: Dictionary containing questions data
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        List of tuples with (question_index, option1_index, option2_index, similarity_score)
    """
    similar_options = []
    questions = json_data["questions"]
    
    # Check each question's options
    for q_idx, question in enumerate(questions):
        variants = question["variants"]
        
        # Compare each option with every other option in the same question
        for i in range(len(variants)):
            for j in range(i + 1, len(variants)):
                similarity = _calculate_text_similarity(
                    variants[i]["text"].lower(),
                    variants[j]["text"].lower()
                )
                
                if similarity >= threshold:
                    similar_options.append((q_idx, i, j, similarity))
    
    return similar_options


def generate_duplicate_report(
    json_data: Dict, 
    question_threshold: float = 1.0,  # Changed to 1.0 for exact matches only
    variant_threshold: float = 1.0    # Changed to 1.0 for exact matches only
) -> str:
    """
    Generate a report of duplicate questions and duplicate options within questions.
    
    Args:
        json_data: Dictionary containing questions data
        question_threshold: Similarity threshold for questions (now 1.0 for exact matches)
        variant_threshold: Similarity threshold for variants (now 1.0 for exact matches)
        
    Returns:
        A formatted report string
    """
    similar_questions = find_similar_questions(json_data, question_threshold)
    similar_options = find_similar_options_within_question(json_data, variant_threshold)
    
    report_sections = []
    
    # Generate report for similar questions
    if similar_questions:
        report_sections.append("IDENTICAL QUESTIONS FOUND:")
        for i, j, sim in similar_questions:
            question_report = _format_similar_questions_report(json_data, i, j, sim)
            report_sections.append(question_report)
    
    # Generate report for similar options within the same question
    if similar_options:
        report_sections.append("IDENTICAL OPTIONS WITHIN THE SAME QUESTION FOUND:")
        for q_idx, opt1_idx, opt2_idx, sim in similar_options:
            option_report = _format_similar_options_report(json_data, q_idx, opt1_idx, opt2_idx, sim)
            report_sections.append(option_report)
    
    # Add "no duplicates" message if nothing found
    if not similar_questions and not similar_options:
        report_sections.append("No duplicate or similar content found.")
    
    return "\n".join(report_sections)


def _format_similar_questions_report(json_data: Dict, q1_index: int, q2_index: int, similarity: float) -> str:
    """
    Format a report section for similar questions.
    
    Args:
        json_data: Dictionary containing questions data
        q1_index: Index of first question
        q2_index: Index of second question
        similarity: Similarity score between questions
        
    Returns:
        Formatted report section
    """
    q1 = json_data["questions"][q1_index]
    q2 = json_data["questions"][q2_index]
    
    report_lines = [
        f"Question {q1['id']} and Question {q2['id']} - 100% identical",
        f"  Q{q1['id']}: {q1['text']}",
        f"  Q{q2['id']}: {q2['text']}",
        ""
    ]
    
    return "\n".join(report_lines)


def _format_similar_variants_report(
    json_data: Dict, 
    q1_index: int, 
    v1_index: int, 
    q2_index: int, 
    v2_index: int, 
    similarity: float
) -> str:
    """
    Format a report section for similar answer variants.
    
    Args:
        json_data: Dictionary containing questions data
        q1_index: Index of first question
        v1_index: Index of variant in first question
        q2_index: Index of second question
        v2_index: Index of variant in second question
        similarity: Similarity score between variants
        
    Returns:
        Formatted report section
    """
    q1 = json_data["questions"][q1_index]
    q2 = json_data["questions"][q2_index]
    v1 = q1["variants"][v1_index]
    v2 = q2["variants"][v2_index]
    
    report_lines = [
        f"Q{q1['id']} option {chr(96 + v1['id'])} and Q{q2['id']} option {chr(96 + v2['id'])} - 100% identical",
        f"  Q{q1['id']}: {q1['text']}",
        f"    {chr(96 + v1['id'])}) {v1['text']}",
        f"  Q{q2['id']}: {q2['text']}",
        f"    {chr(96 + v2['id'])}) {v2['text']}",
        ""
    ]
    
    return "\n".join(report_lines)


def _format_similar_options_report(
    json_data: Dict,
    q_index: int,
    opt1_index: int,
    opt2_index: int,
    similarity: float
) -> str:
    """
    Format a report section for similar options within the same question.
    
    Args:
        json_data: Dictionary containing questions data
        q_index: Index of the question
        opt1_index: Index of first option
        opt2_index: Index of second option
        similarity: Similarity score between options
        
    Returns:
        Formatted report section
    """
    question = json_data["questions"][q_index]
    opt1 = question["variants"][opt1_index]
    opt2 = question["variants"][opt2_index]
    
    report_lines = [
        f"In Question {question['id']} - Options {chr(96 + opt1['id'])} and {chr(96 + opt2['id'])} are 100% identical",
        f"  Q{question['id']}: {question['text']}",
        f"    {chr(96 + opt1['id'])}) {opt1['text']}",
        f"    {chr(96 + opt2['id'])}) {opt2['text']}",
        ""
    ]
    
    return "\n".join(report_lines)