import os
import tempfile
import json
import pytest
from parser import parse_input_file
from formatters import (
    transform_to_student_format,
    transform_to_program_format,
    create_word_document
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_text_file():
    """Create a temporary text file with sample questions."""
    content = """1. What is Python?
        a) A snake
        b) *A programming language
        c) An operating system
        d) A database

        2. What does CPU stand for?
        a) *Central Processing Unit
        b) Computer Processing Unit
        c) Central Program Utility
        d) Computer Program Utility
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp:
        temp.write(content)
        temp_name = temp.name
    
    yield temp_name
    os.unlink(temp_name)


@pytest.fixture
def sample_json_file():
    """Create a temporary JSON file with sample questions."""
    content = {
        "questions": [
            {
                "id": 1,
                "text": "What is Python?",
                "variants": [
                    {"id": 1, "text": "A snake"},
                    {"id": 2, "text": "A programming language"},
                    {"id": 3, "text": "An operating system"},
                    {"id": 4, "text": "A database"}
                ],
                "correct": 2
            },
            {
                "id": 2,
                "text": "What does CPU stand for?",
                "variants": [
                    {"id": 1, "text": "Central Processing Unit"},
                    {"id": 2, "text": "Computer Processing Unit"},
                    {"id": 3, "text": "Central Program Utility"},
                    {"id": 4, "text": "Computer Program Utility"}
                ],
                "correct": 1
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp:
        json.dump(content, temp)
        temp_name = temp.name
    
    yield temp_name
    os.unlink(temp_name)


def test_text_file_to_all_formats(sample_text_file, temp_dir):
    """Test full workflow from text file to all output formats."""
    json_data = parse_input_file(sample_text_file)
    
    assert "questions" in json_data
    assert len(json_data["questions"]) == 2
    
    student_format = transform_to_student_format(json_data, include_variants=True)
    student_path = os.path.join(temp_dir, "student_format.txt")
    with open(student_path, "w", encoding="utf-8") as f:
        f.write(student_format)
    
    assert os.path.exists(student_path)
    with open(student_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "1. What is Python?" in content
        assert "a) A snake" in content
        assert "2. What does CPU stand for?" in content
    
    student_no_variants = transform_to_student_format(json_data, include_variants=False)
    student_no_variants_path = os.path.join(temp_dir, "student_no_variants.txt")
    with open(student_no_variants_path, "w", encoding="utf-8") as f:
        f.write(student_no_variants)
    
    assert os.path.exists(student_no_variants_path)
    with open(student_no_variants_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "1. What is Python?" in content
        assert "a) A snake" not in content
    
    program_format = transform_to_program_format(json_data)
    program_path = os.path.join(temp_dir, "program_format.txt")
    with open(program_path, "w", encoding="utf-8") as f:
        f.write(program_format)
    
    assert os.path.exists(program_path)
    with open(program_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "What is Python?" in content
        assert "#A programming language" in content
        assert "====" in content
    
    word_path = os.path.join(temp_dir, "questions.docx")
    create_word_document(json_data, word_path)
    
    assert os.path.exists(word_path)


def test_json_file_to_all_formats(sample_json_file, temp_dir):
    """Test full workflow from JSON file to all output formats."""
    json_data = parse_input_file(sample_json_file)
    
    assert "questions" in json_data
    assert len(json_data["questions"]) == 2
    
    student_format = transform_to_student_format(json_data, include_variants=True)
    student_path = os.path.join(temp_dir, "student_format.txt")
    with open(student_path, "w", encoding="utf-8") as f:
        f.write(student_format)
    
    assert os.path.exists(student_path)
    
    student_no_variants = transform_to_student_format(json_data, include_variants=False)
    student_no_variants_path = os.path.join(temp_dir, "student_no_variants.txt")
    with open(student_no_variants_path, "w", encoding="utf-8") as f:
        f.write(student_no_variants)
    
    assert os.path.exists(student_no_variants_path)
    
    program_format = transform_to_program_format(json_data)
    program_path = os.path.join(temp_dir, "program_format.txt")
    with open(program_path, "w", encoding="utf-8") as f:
        f.write(program_format)
    
    assert os.path.exists(program_path)
    
    word_path = os.path.join(temp_dir, "questions.docx")
    create_word_document(json_data, word_path)
    
    assert os.path.exists(word_path)


def test_format_content_verification(sample_text_file, temp_dir):
    """Test detailed content verification of different output formats."""
    json_data = parse_input_file(sample_text_file)
    
    student_format = transform_to_student_format(json_data, include_variants=True)
    lines = student_format.strip().split("\n")
    
    assert lines[0] == "1. What is Python?"
    assert lines[1] == "a) A snake"
    assert lines[2] == "b) A programming language"
    assert lines[3] == "c) An operating system"
    assert lines[4] == "d) A database"
    
    program_format = transform_to_program_format(json_data)
    lines = program_format.strip().split("\n")
    
    assert lines[0] == "What is Python?"
    assert lines[1] == "===="
    assert "A snake" in program_format
    assert "#A programming language" in program_format
    assert "+++++" in program_format or "++++" in program_format