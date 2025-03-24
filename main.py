import os
import sys
import json
from parser import parse_input_file
from formatters import (
    transform_to_student_format,
    transform_to_program_format,
    create_word_document,
)
from utils import parse_args, get_output_paths, print_usage


def main():
    if "--help" in sys.argv:
        print_usage()
        sys.exit(0)

    input_path, output_folder, output_name, formats = parse_args()

    os.makedirs(output_folder, exist_ok=True)

    file_paths = get_output_paths(output_folder, output_name)

    try:
        json_data = parse_input_file(input_path)

        if formats["student"]:
            student_text = transform_to_student_format(json_data, include_variants=True)
            with open(file_paths["student"], "w", encoding="utf-8") as file:
                file.write(student_text)

            student_text_novariants = transform_to_student_format(
                json_data, include_variants=False
            )
            with open(file_paths["student_novariant"], "w", encoding="utf-8") as file:
                file.write(student_text_novariants)
            print(f"Generated student formats in {output_folder}")

        if formats["program"]:
            program_text = transform_to_program_format(json_data)
            with open(file_paths["program"], "w", encoding="utf-8") as file:
                file.write(program_text)
            print(f"Generated program format in {output_folder}")

        if formats["word"]:
            create_word_document(json_data, file_paths["word"])
            print(f"Generated Word document in {output_folder}")

    except json.JSONDecodeError:
        print("Error: Invalid JSON file")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
