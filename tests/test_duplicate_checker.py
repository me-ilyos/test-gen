import os
import sys
import tempfile
import pytest
from utils import parse_args, get_output_paths

@pytest.fixture
def mock_argv(monkeypatch):
    """Setup mock command line arguments."""
    def _mock_argv(args):
        monkeypatch.setattr(sys, 'argv', args)
    return _mock_argv


def test_get_output_paths():
    """Test generating output file paths."""
    paths = get_output_paths("/tmp", "test")
    assert paths["student"] == os.path.join("/tmp", "testTalabaVariant.txt")
    assert paths["student_novariant"] == os.path.join("/tmp", "testTalabaNovariant.txt")
    assert paths["program"] == os.path.join("/tmp", "testHemis.txt")
    assert paths["word"] == os.path.join("/tmp", "testYakuniy.docx")
    
    paths = get_output_paths("/tmp", "test.json")
    assert paths["student"] == os.path.join("/tmp", "testTalabaVariant.txt")
    assert paths["student_novariant"] == os.path.join("/tmp", "testTalabaNovariant.txt")
    assert paths["program"] == os.path.join("/tmp", "testHemis.txt")
    assert paths["word"] == os.path.join("/tmp", "testYakuniy.docx")


def test_parse_args_all_formats(mock_argv, monkeypatch):
    """Test parsing command line arguments for all formats."""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
        input_path = temp.name
    
    try:
        monkeypatch.setattr(os.path, 'exists', lambda path: True)
        
        mock_argv(['main.py', input_path, '/tmp', 'test'])
        input_file, output_folder, output_name, formats = parse_args()
        
        assert input_file == input_path
        assert output_folder == '/tmp'
        assert output_name == 'test'
        assert formats["student"] is True
        assert formats["program"] is True
        assert formats["word"] is True
        
        mock_argv(['main.py', input_path, '/tmp', 'test', '--all'])
        _, _, _, formats = parse_args()
        assert formats["student"] is True
        assert formats["program"] is True
        assert formats["word"] is True
    finally:
        os.unlink(input_path)


def test_parse_args_specific_formats(mock_argv, monkeypatch):
    """Test parsing command line arguments for specific formats."""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
        input_path = temp.name
    
    try:
        monkeypatch.setattr(os.path, 'exists', lambda path: True)
        
        mock_argv(['main.py', input_path, '/tmp', 'test', '--student'])
        _, _, _, formats = parse_args()
        assert formats["student"] is True
        assert formats["program"] is False
        assert formats["word"] is False
        
        mock_argv(['main.py', input_path, '/tmp', 'test', '--hemis'])
        _, _, _, formats = parse_args()
        assert formats["student"] is False
        assert formats["program"] is True
        assert formats["word"] is False
        
        mock_argv(['main.py', input_path, '/tmp', 'test', '--word'])
        _, _, _, formats = parse_args()
        assert formats["student"] is False
        assert formats["program"] is False
        assert formats["word"] is True
    finally:
        os.unlink(input_path)


def test_parse_args_invalid_input(mock_argv, monkeypatch):
    """Test parsing command line arguments with invalid input."""
    monkeypatch.setattr(os.path, 'exists', lambda path: False)
    
    mock_argv(['main.py', '/nonexistent/file.txt', '/tmp', 'test'])
    
    with pytest.raises(SystemExit) as e:
        parse_args()
    assert e.value.code == 1