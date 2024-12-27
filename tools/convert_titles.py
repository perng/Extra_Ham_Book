import json
import os
import re
from openai import OpenAI

# Load the OpenAI API key from environment variable
api_key = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=api_key)

# Load questions from JSON file
with open('questions.json', 'r') as f:
    questions_data = json.load(f)

# Function to get a better title from OpenAI API
def get_better_title(original_title):
    # remove patterns "[A-Z][0-9]+"
    original_title = re.sub(r"[A-Z][0-9]+", "", original_title)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Please provide a more interesting title that is more like a movie quote for the following section: '{original_title}'."}
        ]
    )
    return response.choices[0].message.content.replace("\"", "").strip()

def get_better_question_title(original_question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Please provide a cheerful short title for the following question: '{original_question}'."}
        ]
    )
    return response.choices[0].message.content.replace("\"", "").strip()


# Process each chapter and section
for chapter in questions_data:
    for section in chapter['sections']:
        original_title = section['section_title']
        # Get a better title
        better_title = get_better_title(original_title)
        # Update the section title
        section['section_title_original'] = original_title
        section['section_title'] = better_title
        for question in section['questions']:
            original_question = question['question']
            # Get a better question title
            better_question_title = get_better_question_title(original_question)
            # Update the question with the new title
            question['question_title'] = better_question_title


# Output the modified data to questions2.json
with open('questions2.json', 'w') as f:
    json.dump(questions_data, f, indent=4)

print("questions2.json has been generated successfully.")