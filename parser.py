import json
import re


def parse_text_file(input_path):
    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    questions = []
    current_question = None
    question_pattern = r"(\d+)\.\s+(.*)"
    variant_pattern = r"([a-z])\)\s+(\*?)(.+)"

    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue

        question_match = re.match(question_pattern, line)
        if question_match:
            if current_question:
                questions.append(current_question)

            question_number = int(question_match.group(1))
            question_text = question_match.group(2).strip()
            current_question = {
                "id": question_number,
                "text": question_text,
                "variants": [],
                "correct": None,
            }
            continue

        variant_match = re.match(variant_pattern, line)
        if variant_match and current_question is not None:
            variant_letter = variant_match.group(1)
            is_correct = bool(variant_match.group(2))
            variant_text = variant_match.group(3).strip()

            variant_id = ord(variant_letter) - ord("a") + 1
            current_question["variants"].append(
                {"id": variant_id, "text": variant_text}
            )

            if is_correct:
                current_question["correct"] = variant_id

    if current_question:
        questions.append(current_question)

    return {"questions": questions}


def parse_json_file(input_path):
    with open(input_path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_input_file(input_path):
    import os

    _, file_extension = os.path.splitext(input_path)

    if file_extension.lower() == ".json":
        return parse_json_file(input_path)
    else:
        return parse_text_file(input_path)
