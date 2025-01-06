import json
import os
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

base_dir = args.license + '/'

# api_key = os.getenv("OPEN_AI_API_KEY")
api_key = os.getenv("DEEPSEEK_API_KEY")
print(api_key)
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


# Load questions from JSON file
with open(base_dir + 'questions2.json', 'r') as f:
    data = json.load(f)

# Ensure the output directory exists

# read "tools/section_gen.lisp" as a prompt
with open("tools/prompt_gen.lisp", "r") as f:
    prompt_template = f.read()


# Loop over each section and its questions

output_dir = base_dir + f'/organized/prompts/'
os.makedirs(output_dir, exist_ok=True)

chapter_index = 1

for chapter in data:
            print(chapter['chapter_title'])
            # if args.sections and not any(section.label.startswith(isection) for isection in args.sections):
                # continue  # skip if not in the list            

            # if the file already exists, skip
            output_file = output_dir + f'chapter_{chapter_index}.json'
            chapter_index += 1
            if not args.r and os.path.exists(output_file):
                print(f"Skipping {output_file} because it already exists")
                continue


         # Prepare the prompt for OpenAI API
            prompt = prompt_template + f"\nHere is the input JSON: {json.dumps(chapter)}"

            # print(prompt)

            if args.p:
                continue

            # Call OpenAI API to generate LaTeX content
            response = client.chat.completions.create(
                # model="gpt-4o-mini",
                model="deepseek-chat",
                messages=[{"role": "system", "content": "You are an knowledgeable radio technology expert, you are able to generate LaTeX content for a book on radio technology."},
                {"role": "user", "content": prompt}]
            )

            # Save the generated LaTeX to a file
            latex_content = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
            with open(output_file, 'w') as tex_file:
                tex_file.write(latex_content)
            

# ... existing code ...
