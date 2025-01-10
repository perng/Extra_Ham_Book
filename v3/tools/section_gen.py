import json
import sys, os
from openai import OpenAI
import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description='Process questions and optionally print prompts.')
parser.add_argument('-l', '--license', type=str, required=True, help='license class')
parser.add_argument('-c', '--chapter', type=int, required=False, help='chapter')

parser.add_argument('-p', action='store_true', help='Print the prompt without calling the API')
parser.add_argument('-r', action='store_true', help='Replace the existing file')


parser.add_argument('sections', type=str, nargs='*', default=[], help='Section label prefixes to filter')
args = parser.parse_args()

assert args.license in ['extra', 'general', 'tech']

base_dir = args.license + '/'

# api_key = os.getenv("OPEN_AI_API_KEY")
api_key = os.getenv("DEEPSEEK_API_KEY")
print(api_key) 
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


# Load questions from JSON file
with open(F'../v2/{args.license}/questions2.json', 'r') as f:
    questions_data = json.load(f)

questions = {}
for chapter in questions_data:
    for section in chapter['sections']:
        for question in section['questions']:
            questions[question['question_id']] = json.dumps(question)

print("number of questions:", len(questions))
# Ensure the output directory exists

# read "tools/section_gen.lisp" as a prompt
with open("tools/section_gen.lisp", "r") as f:
    prompt_template = f.read()


# read toc.json
with open(base_dir + 'toc.json', 'r') as f:
    toc = json.load(f)


# Loop over each section and its questions

output_dir = base_dir 
os.makedirs(output_dir, exist_ok=True)

prompt_path = base_dir + f'/prompts/'

# Loop over toc.json

for part in toc['parts']:
    part_id = part['label'].split(':')[1]
    for chapter in part['chapters']:
        chapter_id = chapter['label'].split(':')[1]
        print(chapter['chapter_title'])
        first_section = True  # Add flag to track first section
        for section in chapter['sections']:
            # if first_section:  # Skip first section
            #     first_section = False
            #     continue
            section_id = section['label'].split(':')[1]
            print(f"Part: {part_id}, Chapter: {chapter_id}, Section: {section_id}")
            prompt_file = base_dir + f'prompts/{part_id}/{chapter_id}/{section_id}.json'
            if not os.path.exists(prompt_file):
                continue
            with open(prompt_file, 'r') as f:
                prompt_json = json.load(f)
            
            for subsec in prompt_json['subsections']:                              
                print(subsec['label'])
                print('qid', [qid for qid in subsec['questions']])
                if type(subsec['questions']) == dict:
                    subsec['questions'] = subsec['questions'].values()
                elif type(subsec['questions']) == list and len(subsec['questions']) >0 and type(subsec['questions'][0]) == str:
                    print('questions type', type(subsec['questions']))
                    print('questions', subsec['questions'])
                    subsec['questions'] = [questions[qid] for qid in subsec['questions']]
                subsec_id = subsec['label'].split(':')[1]
                        
                output_dir = base_dir + f'contents/{part_id}/{chapter_id}/{section_id}/'
                os.makedirs(output_dir, exist_ok=True)
                output_file = output_dir + f'{subsec_id}.tex'
                if not args.r and os.path.exists(output_file):
                    print(f"Skipping {output_file} because it already exists")            
                    continue
            
                # Prepare the prompt for OpenAI API
                prompt = prompt_template + f"\nHere is the input JSON: {json.dumps(subsec)}"

            
                if args.p:
                    print(prompt)
                    print('skipping because -p is set')
                    os.exit(0)
    
        
                response = client.chat.completions.create(
                    # model="gpt-4o-mini",
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": "You are an knowledgeable radio technology expert, you are able to generate LaTeX content for a book on radio technology."},
                    {"role": "user", "content": prompt}]
                )

                latex_content = response.choices[0].message.content
                
                # remove everything before the '\section'
                latex_content = '\\subsection' + latex_content.split('\\subsection')[1]
                # remove everything after "```"
                latex_content = latex_content.split("```")[0]
                with open(output_file, 'w') as tex_file:
                    tex_file.write(latex_content)
    
                # sys.exit(0)
