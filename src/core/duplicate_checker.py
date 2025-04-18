"""
Duplicate question detector for test questions.

This file contains functions for identifying similar questions and answer variants
in a set of test questions. It uses sequence matching to calculate text similarity
and generates reports about potential duplicates.
"""

from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional


def find_similar_questions(json_data: Dict, threshold: float = 0.8) -> List[Tuple[int, int, float]]:
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


def find_similar_variants(json_data: Dict, threshold: float = 0.8) -> List[Tuple[int, int, int, int, float]]:
    """
    Find similar answer variants across questions.
    
    Args:
        json_data: Dictionary containing questions data
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        List of tuples with (question1_index, variant1_index, question2_index, variant2_index, similarity_score)
    """
    similar_variants = []
    questions = json_data["questions"]
    
    # Compare variants across different questions
    for i in range(len(questions)):
        for j in range(i, len(questions)):
            variant_pairs = _find_similar_variant_pairs(
                questions[i], questions[j], i, j, threshold
            )
            similar_variants.extend(variant_pairs)
    
    return similar_variants


def _find_similar_variant_pairs(
    question1: Dict, 
    question2: Dict, 
    q1_index: int, 
    q2_index: int, 
    threshold: float
) -> List[Tuple[int, int, int, int, float]]:
    """
    Find similar variant pairs between two questions.
    
    Args:
        question1: First question data
        question2: Second question data
        q1_index: Index of first question in the dataset
        q2_index: Index of second question in the dataset
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        List of tuples with (q1_index, variant1_index, q2_index, variant2_index, similarity)
    """
    similar_pairs = []
    
    for vi, variant1 in enumerate(question1["variants"]):
        for vj, variant2 in enumerate(question2["variants"]):
            # Skip comparing a variant with itself
            if q1_index == q2_index and vi == vj:
                continue
            
            similarity = _calculate_text_similarity(
                variant1["text"].lower(),
                variant2["text"].lower()
            )
            
            if similarity >= threshold:
                similar_pairs.append((q1_index, vi, q2_index, vj, similarity))
    
    return similar_pairs


def generate_duplicate_report(
    json_data: Dict, 
    question_threshold: float = 0.8, 
    variant_threshold: float = 0.9
) -> str:
    """
    Generate a report of duplicate questions and variants.
    
    Args:
        json_data: Dictionary containing questions data
        question_threshold: Similarity threshold for questions
        variant_threshold: Similarity threshold for variants
        
    Returns:
        A formatted report string
    """
    similar_questions = find_similar_questions(json_data, question_threshold)
    similar_variants = find_similar_variants(json_data, variant_threshold)
    
    report_sections = []
    
    # Generate report for similar questions
    if similar_questions:
        report_sections.append("SIMILAR QUESTIONS FOUND:")
        for i, j, sim in similar_questions:
            question_report = _format_similar_questions_report(json_data, i, j, sim)
            report_sections.append(question_report)
    
    # Generate report for similar variants
    if similar_variants:
        report_sections.append("SIMILAR ANSWER VARIANTS FOUND:")
        for i, vi, j, vj, sim in similar_variants:
            variant_report = _format_similar_variants_report(json_data, i, vi, j, vj, sim)
            report_sections.append(variant_report)
    
    # Add "no duplicates" message if nothing found
    if not similar_questions and not similar_variants:
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
        f"Question {q1['id']} and Question {q2['id']} - {similarity:.2f} similarity",
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
        f"Q{q1['id']} option {chr(96 + v1['id'])} and Q{q2['id']} option {chr(96 + v2['id'])} - {similarity:.2f} similarity",
        f"  Q{q1['id']}: {q1['text']}",
        f"    {chr(96 + v1['id'])}) {v1['text']}",
        f"  Q{q2['id']}: {q2['text']}",
        f"    {chr(96 + v2['id'])}) {v2['text']}",
        ""
    ]
    
    return "\n".join(report_lines)