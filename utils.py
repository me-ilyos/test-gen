import os
import sys


def print_usage():
    print("Usage: python main.py input_path output_folder output_name [options]")
    print("Options:")
    print("  -a, --all       Generate all formats (default)")
    print("  -s, --student   Generate only student formats (with and without variants)")
    print("  -h, --hemis     Generate only program format")
    print("  -w, --word      Generate only Word document format")
    print("  --help          Show this help message")


def parse_args():
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    input_path = sys.argv[1]
    output_folder = sys.argv[2]
    output_name = sys.argv[3]

    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist")
        sys.exit(1)

    # Default to all formats if no option specified
    formats = {"student": True, "program": True, "word": True}

    # Parse additional arguments if provided
    if len(sys.argv) > 4:
        arg = sys.argv[4].lower()

        if arg in ["--help"]:
            print_usage()
            sys.exit(0)
        elif arg in ["-a", "--all"]:
            pass  # Already set to all
        elif arg in ["-s", "--student"]:
            formats = {"student": True, "program": False, "word": False}
        elif arg in ["-h", "--hemis"]:
            formats = {"student": False, "program": True, "word": False}
        elif arg in ["-w", "--word"]:
            formats = {"student": False, "program": False, "word": True}
        else:
            print(f"Unknown option: {arg}")
            print_usage()
            sys.exit(1)

    return input_path, output_folder, output_name, formats


def get_output_paths(output_folder, output_name):
    name_without_ext = os.path.splitext(output_name)[0]
    return {
        "student": os.path.join(output_folder, f"{name_without_ext}TalabaVariant.txt"),
        "student_novariant": os.path.join(
            output_folder, f"{name_without_ext}TalabaNovariant.txt"
        ),
        "program": os.path.join(output_folder, f"{name_without_ext}Hemis.txt"),
        "word": os.path.join(output_folder, f"{name_without_ext}Yakuniy.docx"),
    }
