"""
Formatters for converting questions to different output formats.

This module contains functions to transform question data into various
output formats including student format, HEMIS format, and Word documents.
"""

from docx import Document
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


def transform_to_student_format(json_data: Dict, include_variants: bool = True) -> str:
    """
    Convert questions to student format with or without answer variants.

    Args:
        json_data: Dictionary containing questions data
        include_variants: Whether to include answer variants in output

    Returns:
        Formatted text for student use
    """
    output = []

    for question in json_data["questions"]:
        output.append(f"{question['id']}. {question['text']}")

        if include_variants:
            output.extend(
                [
                    f"{chr(96 + variant['id'])}) {variant['text']}"
                    for variant in question["variants"]
                ]
            )

        output.append("")

    return "\n".join(output)


def transform_to_program_format(json_data: Dict) -> str:
    """
    Convert questions to HEMIS format with markers for correct answers.

    Args:
        json_data: Dictionary containing questions data

    Returns:
        Formatted text in HEMIS format
    """
    output = []
    questions = json_data["questions"]

    for i, question in enumerate(questions):
        output.append(question["text"])
        output.append("====")

        for variant in question["variants"]:
            is_correct = variant["id"] == question["correct"]
            marker = "#" if is_correct else ""
            output.append(f"{marker}{variant['text']}")
            output.append("====")

        if i < len(questions) - 1:
            output.append("++++")

    return "\n".join(output)


def create_word_document(json_data: Dict, output_path: str) -> None:
    """
    Create a Word document with questions in tables.

    Args:
        json_data: Dictionary containing questions data
        output_path: Path to save the Word document
    """
    doc = Document()

    for question in json_data["questions"]:
        num_variants = len(question["variants"])
        table = doc.add_table(rows=num_variants + 1, cols=1)
        table.style = "Table Grid"

        # Add question to first row
        question_cell = table.cell(0, 0)
        question_cell.text = question["text"]

        # Get correct answer safely
        correct_variants = [
            v for v in question["variants"] if v["id"] == question["correct"]
        ]

        if correct_variants:
            # Use the first matching correct variant
            correct_variant = correct_variants[0]

            # Add correct answer to second row
            table.cell(1, 0).text = correct_variant["text"]

            # Add incorrect answers to remaining rows
            row = 2
            incorrect_variants = [
                v for v in question["variants"] if v["id"] != question["correct"]
            ]
            for variant in incorrect_variants:
                table.cell(row, 0).text = variant["text"]
                row += 1
        else:
            # Handle case where no correct answer is found
            # Just add all variants in order
            logger.warning(f"No correct answer found for question: {question['id']}")

            for i, variant in enumerate(question["variants"]):
                table.cell(i + 1, 0).text = variant["text"]

        doc.add_paragraph()

    doc.save(output_path)


def create_student_format_word(
    json_data: Dict, output_path: str, include_variants: bool = True
) -> None:
    """
    Create a Word document with questions in student format.

    Args:
        json_data: Dictionary containing questions data
        output_path: Path to save the Word document
        include_variants: Whether to include answer variants
    """
    doc = Document()

    for question in json_data["questions"]:
        # Add question
        doc.add_paragraph(f"{question['id']}. {question['text']}")

        # Add variants if requested
        if include_variants:
            for variant in question["variants"]:
                doc.add_paragraph(f"{chr(96 + variant['id'])}) {variant['text']}")

        # Add empty paragraph between questions
        doc.add_paragraph()

    doc.save(output_path)


def create_program_format_word(json_data: Dict, output_path: str) -> None:
    """
    Create a Word document with questions in HEMIS format.

    Args:
        json_data: Dictionary containing questions data
        output_path: Path to save the Word document
    """
    doc = Document()
    questions = json_data["questions"]

    for i, question in enumerate(questions):
        # Add question
        doc.add_paragraph(question["text"])
        doc.add_paragraph("====")

        # Add variants
        for variant in question["variants"]:
            is_correct = variant["id"] == question["correct"]
            marker = "#" if is_correct else ""
            doc.add_paragraph(f"{marker}{variant['text']}")
            doc.add_paragraph("====")

        # Add separator between questions
        if i < len(questions) - 1:
            doc.add_paragraph("++++")

    doc.save(output_path)


def create_duplicate_report_word(report_text: str, output_path: str) -> None:
    """
    Create a Word document with duplicate report.

    Args:
        report_text: Text of the duplicate report
        output_path: Path to save the Word document
    """
    doc = Document()

    # Add title
    doc.add_heading("Takrorlanishlar hisoboti", level=1)

    # Add report content, split by lines
    for line in report_text.split("\n"):
        if line.startswith("SIMILAR QUESTIONS FOUND") or line.startswith(
            "SIMILAR ANSWER VARIANTS FOUND"
        ):
            # Make these section headings
            doc.add_heading(line, level=2)
        elif line.strip() == "":
            # Add empty paragraph for spacing
            doc.add_paragraph()
        else:
            # Regular paragraph for content
            doc.add_paragraph(line)

    doc.save(output_path)
