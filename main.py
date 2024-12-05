"""
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
"""
import json
import sys
import os

def transform_to_text(json_data):
    output = []
    for question in json_data['questions']:
        output.append(question['text'])
        output.append("====")
        
        for variant in question['variants']:
            output.append(f"{'#' if variant['id'] == question['correct'] else ''}{variant['text']}")
            output.append("====")
        
        if question != json_data['questions'][-1]:
            output.append("++++")
    
    return "\n".join(output)

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py input_path output_folder output_name")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_folder = sys.argv[2]
    output_name = sys.argv[3]
    
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist")
        sys.exit(1)
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, output_name)
    
    try:
        with open(input_path, 'r') as file:
            json_data = json.load(file)
        
        formatted_text = transform_to_text(json_data)
        with open(output_path, 'w') as file:
            file.write(formatted_text)
            
    except json.JSONDecodeError:
        print("Error: Invalid JSON file")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()