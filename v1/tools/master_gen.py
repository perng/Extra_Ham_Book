import json
import os


import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description='Process questions and optionally print prompts.')
parser.add_argument('-l', '--license', type=str, required=True, help='license class')
args = parser.parse_args()
titles = {'tech':'Technical Ham', 'general':'General Ham', 'extra':'Extra HAM!'}
assert args.license in ['tech', 'general', 'extra']

base_dir = args.license + '/'

# Load questions from JSON file
with open(base_dir + 'questions2.json', 'r') as f:
    questions_data = json.load(f)

# Start creating the LaTeX content
latex_content = r"""\documentclass[12pt]{book}

\usepackage{geometry} % Page layout
\usepackage{titlesec} % Formatting headings
\usepackage{fancyhdr} % Header/Footer
\usepackage{hyperref} % Hyperlinks
\usepackage{graphicx} % For images
\usepackage{amsmath} % For math
\usepackage{amssymb} % For math symbols
\usepackage{enumitem} % Custom lists
\usepackage[most]{tcolorbox}
\usepackage{epstopdf} % For converting EPS to PDF
\usepackage{pgfplots}
\usepackage{tikz}
\usepackage{svg}
\usetikzlibrary{circuits.ee.IEC} % Include this if using electrical components
\usepackage{circuitikz}
\pgfplotsset{compat=1.18} % Important for log10

% Page layout
\geometry{a4paper, margin=1in}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Extra HAM!}
\fancyhead[R]{}
\fancyfoot[C]{\thepage}

\titleformat{\chapter}[hang]{\huge\bfseries}{Chapter \thechapter}{1em}{}
\titleformat{\section}[hang]{\Large\bfseries}{\thesection}{0.5em}{}
\titleformat{\subsection}[hang]{\large\bfseries}{\thesubsection}{1em}{}

\begin{document}

\tableofcontents
\newpage
"""

# Iterate through chapters and sections
for chapter in questions_data:
    chapter_title = chapter['chapter_title']
    latex_content += f"\\chapter{{{chapter_title}}}\n"
    
    for section in chapter['sections']:
        section_title = section['section_title']
        latex_content += f"\\section{{{section_title}}}\n"
        
        for question in section['questions']:
            question_id = question['question_id']

            # extra sections
            # if question_id == "E6A01":
            #     latex_content += "\\include{questions/transistors}\n"

            section_path =  f"{base_dir}questions/{question_id[:3]}/{question_id}"
            output_file = section_path + ".tex"
            # if the file does not exist, skip
            if os.path.exists(output_file):               
                latex_content += f"\\input{{{section_path}}}\n"

# End the document
latex_content += r"""
\end{document}
"""

# Write the LaTeX content to master.tex
with open(base_dir + args.license +'.tex', 'w') as f:
    f.write(latex_content)

print("master.tex has been generated successfully.")