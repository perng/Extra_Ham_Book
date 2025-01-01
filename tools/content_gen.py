import json
import os
from openai import OpenAI
import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description='Process questions and optionally print prompts.')
parser.add_argument('-l', '--license', type=str, required=True, help='license class')
parser.add_argument('-p', action='store_true', help='Print the prompt without calling the API')
parser.add_argument('-r', action='store_true', help='Replace the existing file')

parser.add_argument('prefixes', type=str, nargs='+', default=[], help='Question ID prefixes to filter questions')
args = parser.parse_args()

assert args.license in ['extra', 'general', 'tech']

base_dir = args.license + '/'

# api_key = os.getenv("OPEN_AI_API_KEY")
api_key = os.getenv("DEEPSEEK_API_KEY")
print(api_key)
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


# Load questions from JSON file
with open(base_dir + 'questions.json', 'r') as f:
    data = json.load(f)

# Ensure the output directory exists

# Loop over each section and its questions
for chapter in data:
    for section in chapter['sections']:

        for question in section['questions']:
            question_id = question['question_id']
            output_dir = base_dir + f'/questions/{question_id[:3]}'
            os.makedirs(output_dir, exist_ok=True)
            if args.prefixes and not any(question_id.startswith(prefix) for prefix in args.prefixes):
                continue  # skip if not in the list            

            # if the file already exists, skip
            if not args.r and os.path.exists(os.path.join(output_dir, f"{question_id}.tex")):
                continue

            question_text = question['question']
            choices = question['choices']

         # Prepare the prompt for OpenAI API
            prompt = f"""Generate a LaTeX subsection for the question in the end. 
            Assume the following packages are loaded: geometry,titlesec,fancyhdr,hyperref,graphicx,amsmath,amssymb,enumitem,tcolorbox,epstopdf        
            First, generate a short subsection (with section number) title based on the question, it should not be as long as the question, it should be the only numbered title.
            If there is other divisions, use subsubsection.
            then add a label to the subsection, it should be the question id.
            then generate the multiple choice questions in a shaded box using
            '\\begin{{tcolorbox}}[colback=gray!10!white,colframe=black!75!black,title={question_id}]'
            then the question text, then enumerate the choices. 
            Mark the correct answer with bold. End with '\\end{{tcolorbox}}'.
            The next subsubsection is "Intuitive Explanation" this would explain the question with humor as if the reader is a middle school student, 
            simplify the question and explain the concept in a way that is easy to understand.
            The next subsubsection is "Advanced Explanation" this would explain the related concepts and concepts required to answer the question in more detail and more mathematically.
            If calculation is required, show the calculation step by step. If math would not help much in explaining the question, don't show it.
            Then elaborate on the related concepts and concepts required to answer the question. 
            
            If diagrams are better for explanation, a prompt for generating the diagram as comment in the end of the output.

            Make sure the entire content is in LaTeX syntax, do not use Markdown or any other formatting. Do not use "**" for bold. 
            Make sure greek letters are in LaTeX syntax.
            Question:{question}"""

            print(prompt)

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
            latex_content = response.choices[0].message.content.replace("\"", "").replace("```latex", "").replace("```", "").strip()
            with open(os.path.join(output_dir, f"{question_id}.tex"), 'w') as tex_file:
                tex_file.write(latex_content)

# ... existing code ...
