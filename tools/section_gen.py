import json
import os
from openai import OpenAI
import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description='Process questions and optionally print prompts.')
parser.add_argument('-l', '--license', type=str, required=True, help='license class')
parser.add_argument('-c', '--chapter', type=int, required=False, help='chapter')

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

questions = {}
for chapter in data:
    for section in chapter['sections']:
        for question in section['questions']:
            questions[question['question_id']] = json.dumps(question)

# Ensure the output directory exists

# read "tools/section_gen.lisp" as a prompt
with open("tools/section_gen.lisp", "r") as f:
    prompt_template = f.read()


# Loop over each section and its questions

output_dir = base_dir + f'/organized/'
os.makedirs(output_dir, exist_ok=True)

prompt_path = base_dir + f'/organized/prompts/'

# Loop over each prompt files


chapter_index = 1
while True:

    ch = 'chapter_' + str(chapter_index)
    prompt_file = prompt_path + ch + '.json'
    if not os.path.exists(prompt_file):
        break

    if args.chapter and int(args.chapter) != chapter_index:
        chapter_index += 1
        continue
    chapter_index += 1

    output_chapter_path = output_dir + ch +'/'
    os.makedirs(output_chapter_path, exist_ok=True)

    print('prompt file:', prompt_file)
    with open(prompt_file, 'r') as f:
        chapter = json.load(f)

    for section in chapter['sections']:
        print('section title:', section['title'])

        qids = section['questions']
        section['questions'] = [questions[qid] for qid in qids]

        output_file = output_chapter_path + f'{section["section_label"].split(":")[1]}.tex'
    
        if not args.r and os.path.exists(output_file):
            print(f"Skipping {output_file} because it already exists")            
            continue

        # Prepare the prompt for OpenAI API
        prompt = prompt_template + f"\nHere is the input JSON: {json.dumps(section)}"

        
        if args.p:
                print(prompt)
                print('skipping because -p is set')
                break
        
        response = client.chat.completions.create(
                # model="gpt-4o-mini",
                model="deepseek-chat",
                messages=[{"role": "system", "content": "You are an knowledgeable radio technology expert, you are able to generate LaTeX content for a book on radio technology."},
                {"role": "user", "content": prompt}]
            )

        latex_content = response.choices[0].message.content
        # remove everything before the '\section'
        latex_content = '\\section' + latex_content.split('\\section')[1]
        # remove everything after "```"
        latex_content = latex_content.split("```")[0]
        with open(output_file, 'w') as tex_file:
              tex_file.write(latex_content)
    

# ... existing code ...
