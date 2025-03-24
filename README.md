# Question Format Converter

A simple Python tool that converts test questions from text or JSON into various output formats useful for students, HEMIS, and Word documents.

## What it does

This app takes test questions with answer variants and converts them into different formats:
- Student format (with or without answer variants)
- Hemis-compatible format marked with special separators
- Word document format with questions in tables

You can specify which format(s) to generate through command-line arguments.

## Input file formatting

The app accepts two types of input files:

### Text file format

```
1. What is Python?
a) A snake
b) *A programming language
c) An operating system
d) A database

2. What does CPU stand for?
a) Central Processing Unit
b) *Computer Processing Unit
c) Central Program Utility
d) Computer Program Utility
```

Mark the correct answer with an asterisk (*).

### JSON file format

```json
{
  "questions": [{
    "id": 1,
    "text": "What is Python?",
    "variants": [
      {"id": 1, "text": "A snake"},
      {"id": 2, "text": "A programming language"}
    ],
    "correct": 2
  }]
}
```

## Output formats

### Student format
```
1. What is Python?
a) A snake
b) A programming language

2. What does CPU stand for?
a) Central Processing Unit
b) Computer Processing Unit
c) Central Program Utility
d) Computer Program Utility
```

### HEMIS format
```
What is Python?
====
A snake
====
#A programming language
====
++++
What does CPU stand for?
====
Central Processing Unit
====
#Computer Processing Unit
====
Central Program Utility
====
Computer Program Utility
====
```

The correct answer is marked with a # symbol.

### Word Document
The app creates a Word document with tables for each question. The first row contains the question, the second row contains the correct answer, and remaining rows contain incorrect answers.

## Installation

1. Make sure you have Python 3.6 or newer installed
2. Install required packages:
   ```
   pip install python-docx
   ```
3. Download all the files or clone the repository

## Usage

Basic usage:
```
python main.py input_file output_folder output_name [options]
```

Examples:
```
# Generate all formats
python main.py questions.txt output test_quiz

# Generate only student formats
python main.py questions.txt output test_quiz -s

# Generate only program format
python main.py questions.txt output test_quiz -h

# Generate only Word document
python main.py questions.txt output test_quiz -w
```

### Command line options

- `-a, --all`: Generate all formats (default)
- `-s, --student`: Generate only student formats (with and without variants)
- `-h, --hemis`: Generate only program format
- `-w, --word`: Generate only Word document format
- `--help`: Show help message

## Output files

The app generates the following files in the output folder:
- `[output_name]_student.txt`: Student format with variants
- `[output_name]_student_novariant.txt`: Student format without variants
- `[output_name]_program.txt`: Program format
- `[output_name].docx`: Word document with tables

## Troubleshooting

- Make sure your input file follows the correct format
- Check that the python-docx package is installed
- Ensure you have write permissions in the output folder
