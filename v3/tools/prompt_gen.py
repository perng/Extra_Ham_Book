import json
import os
import sys
from openai import OpenAI
import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description='Process questions and optionally print prompts.')
parser.add_argument('-l', '--license', type=str, required=True, help='license class')
parser.add_argument('-p', action='store_true', help='Print the prompt without calling the API')
parser.add_argument('-r', action='store_true', help='Replace the existing file')

# parser.add_argument('sections', type=str, nargs='+', default=[], help='Section label prefixes to filter')
args = parser.parse_args()

assert args.license in ['extra', 'general', 'tech']

base_dir =  args.license + '/'

# api_key = os.getenv("OPEN_AI_API_KEY")
api_key = os.getenv("DEEPSEEK_API_KEY")
print(api_key)
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


questions = {}
with open(f'../v2/{args.license}/questions2.json', 'r') as f:
    data = json.load(f)
    for chapter in data:
        for section in chapter['sections']:
            for question in section['questions']:
                questions[question['question_id']] = json.dumps(question)


# Load questions from JSON file
with open(base_dir + 'toc.json', 'r') as f:
    data = json.load(f)

# Ensure the output directory exists

# read "tools/section_gen.lisp" as a prompt
with open("tools/prompt_gen.lisp", "r") as f:
    prompt_template = f.read()


# Loop over each section and its questions

output_dir = base_dir + f'/prompts/'
os.makedirs(output_dir, exist_ok=True)

chapter_index = 1

concepts=[]

for part in data['parts']:
    part_id = part['label'].split(':')[1]
    for chapter in part['chapters']:
        chapter_id = chapter['label'].split(':')[1]
        print(chapter['chapter_title'])
        first_section = True  # Add flag to track first section
        for section in chapter['sections']:
            if first_section:  # Skip first section
                first_section = False
                continue
            section_id = section['label'].split(':')[1]
            print(f"Part: {part_id}, Chapter: {chapter_id}, Section: {section_id}")
            output_dir = base_dir + f'prompts/{part_id}/{chapter_id}/'
            print('creating', output_dir)
            os.makedirs(output_dir, exist_ok=True)
            output_file = f'{output_dir}{section_id}.json'
            print('output_file', output_file)
            if not args.r and os.path.exists(output_file):
                print(f"Skipping {output_file} because it already exists")
                with open(output_file, 'r') as f:
                        section_data = json.load(f)
                        for subsection in section['subsections']:
                            if 'concepts' in subsection:
                                concepts.extend(subsection['concepts'])
                continue
                 
            prompt = prompt_template + f"\nHere is the input section-data JSON: {json.dumps(section)}" + f"\nHere is the previously defined-concepts: {str(concepts)}\n"
            prompt += "The questions are:\n"
            for subsection in section['subsections']:
                for qid in subsection['questions']:
                    prompt += f"{str(questions[qid])},\n"

            # print(prompt)
            if args.p:
                continue
            
                
            # Call OpenAI API to generate LaTeX content
            response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": "You are an knowledgeable radio technology expert, you are about to generate content for a book on radio technology."},
                    {"role": "user", "content": prompt}]
                )

            # Save the generated LaTeX to a file
            content = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
            with open(output_file, 'w') as tex_file:
                    tex_file.write(content)
            # load the content as json
            content = json.loads(content)
            for subsection in content['subsections']:
                concepts.extend(subsection['concepts'])
        # sys.exit(0)
            