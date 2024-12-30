import json
import re

def parse_questions(file_path):
    data = []
    current_chapter = None
    current_section = None

    # Read all lines into a list and filter out blank lines and separators
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and "~~" not in line]

    index = 0  # Initialize an index to track the current line
    while index < len(lines):
        line = lines[index]
        if line.startswith("SUBELEMENT"):
            print('subelement', line)
            # New chapter
            if current_section is not None:
                current_chapter["sections"].append(current_section)
            current_section = None

            if current_chapter is not None:
                data.append(current_chapter)

            current_chapter = {
                "chapter_title": line,
                "sections": []
            }
        elif re.match(r"^E\d\w ", line):
            print('section', line)
            # New section
            if current_section is not None:
                current_chapter["sections"].append(current_section)
            current_section = {
                "section_title": line,
                "questions": []
            }
        elif line and current_section is not None:
            # Process question
            question_id = line.split()[0]  # Get the question ID (e.g., E1A01)
            answer = line.split()[-1][1]  # Get the answer (e.g., (D))
            index += 1  # Move to the next line for the question text
            question_text = lines[index]  # Get the question text
            choices = {}
            for _ in range(4):
                index += 1  # Move to the next line for each choice
                option_line = lines[index]
                assert option_line[0] in "ABCD"
                choices[option_line[0]] = option_line[3:]  # Get choice letter and text

            question = {
                "question_id": question_id,
                "question": question_text,
                "answer": answer,
                "choices": choices
            }
            current_section["questions"].append(question)

        index += 1  # Move to the next line
        # if index > 1520:
        #     break

    # Append the last section and chapter
    if current_section is not None:
        current_chapter["sections"].append(current_section)
    if current_chapter is not None:
        data.append(current_chapter)

    return data

def main():
    file_path = 'questions.txt'
    questions = parse_questions(file_path)

    # Convert to JSON format
    json_output = json.dumps(questions, indent=4)

    # Save to a JSON file
    with open('questions.json', 'w') as json_file:
        json_file.write(json_output)

if __name__ == "__main__":
    main()