import json
import os
import re
from openai import OpenAI
import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description='Process questions and optionally print prompts.')
parser.add_argument('-l', '--license', type=str, required=True, help='license class')
args = parser.parse_args()

base_dir = args.license + '/'

# Load the OpenAI API key from environment variable
api_key = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=api_key)

# Load questions from JSON file
with open(base_dir + 'questions.json', 'r') as f:
    questions_data = json.load(f)

# Function to get a better title from OpenAI API
def get_better_title(section):    
        
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1.5,
        messages=[
            {"role": "user", 
             "content": f"""come up with a short and interesting title 
             for the section that would explain concepts  required for the attached questions. 
             Do not use meaningless phrases like "key concepts", "a guide to", "essential", "insights", 
             "foundations", "fundamental", "decoding", "demystifying", "understanding", etc.              
             Just simple title. 
            The questions are : \n{section['questions']}"""}
        ]
    )
    return response.choices[0].message.content.replace("\"", "").replace("**", "").replace("#", "").strip().lstrip()


# Process each chapter and section
for chapter in questions_data:
    for section in chapter['sections']:
        # original_title = section['section_title']
        # Get a better title
        better_title = get_better_title(section)
        # Update the section title
        #section['section_title_original'] = original_title
        section['section_title'] = better_title


# Output the modified data to questions2.json
with open(base_dir + 'questions2.json', 'w') as f:
    json.dump(questions_data, f, indent=4)

print("questions3.json has been generated successfully.")