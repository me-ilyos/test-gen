import json
import os
import tempfile
import pytest
from parser import parse_json_file, parse_text_file, parse_input_file


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


def test_parse_text_file(sample_text_file):
    """Test parsing a text file with questions and answers."""
    result = parse_text_file(sample_text_file)
    
    assert "questions" in result
    assert len(result["questions"]) == 2
    
    # Test first question
    q1 = result["questions"][0]
    assert q1["id"] == 1
    assert q1["text"] == "What is Python?"
    assert len(q1["variants"]) == 4
    assert q1["correct"] == 2
    
    # Test second question
    q2 = result["questions"][1]
    assert q2["id"] == 2
    assert q2["text"] == "What does CPU stand for?"
    assert len(q2["variants"]) == 4
    assert q2["correct"] == 1


def test_parse_json_file(sample_json_file):
    """Test parsing a JSON file with questions and answers."""
    result = parse_json_file(sample_json_file)
    
    assert "questions" in result
    assert len(result["questions"]) == 2
    
    # Test first question
    q1 = result["questions"][0]
    assert q1["id"] == 1
    assert q1["text"] == "What is Python?"
    assert len(q1["variants"]) == 4
    assert q1["correct"] == 2
    
    # Test second question
    q2 = result["questions"][1]
    assert q2["id"] == 2
    assert q2["text"] == "What does CPU stand for?"
    assert len(q2["variants"]) == 4
    assert q2["correct"] == 1


def test_parse_input_file(sample_text_file, sample_json_file):
    """Test the function that detects file type and parses accordingly."""
    # Test with text file
    text_result = parse_input_file(sample_text_file)
    assert "questions" in text_result
    assert len(text_result["questions"]) == 2
    
    # Test with json file
    json_result = parse_input_file(sample_json_file)
    assert "questions" in json_result
    assert len(json_result["questions"]) == 2