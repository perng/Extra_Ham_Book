import json
import os


import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description='Process questions and optionally print prompts.')
parser.add_argument('-l', '--license', type=str, required=True, help='license class')
args = parser.parse_args()
titles = {'tech':'Technical Ham', 'general':'General Ham', 'extra':'Extra HAM!'}
assert args.license in ['tech', 'general', 'extra']

base_dir = args.license + '/organized/'


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
\usepackage{draftwatermark}
\SetWatermarkText{Draft}
\SetWatermarkScale{4}
\SetWatermarkLightness{0.9}


\pgfplotsset{compat=1.18} % Important for log10

% Page layout
\geometry{a4paper, margin=1in}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{<book_title>}
\fancyhead[R]{}
\fancyfoot[C]{\thepage}

\titleformat{\chapter}[hang]{\huge\bfseries}{Chapter \thechapter}{1em}{}
\titleformat{\section}[hang]{\Large\bfseries}{\thesection}{0.5em}{}
\titleformat{\subsection}[hang]{\large\bfseries}{\thesubsection}{1em}{}

\begin{document}

\tableofcontents
\newpage
"""

latex_content = latex_content.replace('<book_title>', titles[args.license])

input_dir = base_dir + f'/prompts/'


# Iterate through chapters and sections

chapter_index = 0
while True:
    chapter_index += 1
    ch = 'chapter_' + str(chapter_index) + '.json'
    if not os.path.exists(input_dir + ch):
        print(f"Chapter {input_dir + ch} not found in {input_dir}. Exiting.")
        break

    with open(input_dir + ch, 'r') as f:
        chapter_data = json.load(f)

    chapter_title = chapter_data['chapter_label'].split(':')[1].replace('_',' ').upper()
    latex_content += f"\\chapter{{{chapter_title}}}\n"
    latex_content += f"\\label{{{chapter_data['chapter_label']}}}\n"
    
    for section in chapter_data['sections']:
        section_label = section['section_label'].split(':')[1]
        section_path = base_dir + f'chapter_{chapter_index}/{section_label}'
        print(section_path)
        if os.path.exists(section_path+'.tex'):
            latex_content += f"\\input{{{section_path}}}\n"
        else:
            print(f"Section {section_label} not found in {section_path}.tex")
            

# End the document
latex_content += r"""
\end{document}
"""

# Write the LaTeX content to master.tex
with open(base_dir + args.license +'.tex', 'w') as f:
    f.write(latex_content)

print("master.tex has been generated successfully.")