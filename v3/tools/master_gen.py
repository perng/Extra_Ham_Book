import json
import os


import argparse


# Set up argument parsing
parser = argparse.ArgumentParser(description='Process questions and optionally print prompts.')
parser.add_argument('-l', '--license', type=str, required=True, help='license class')
args = parser.parse_args()
titles = {'tech':'Beyond Memorization: Ham Technician Class', 
          'general':'Beyond Memorization: Ham General Class', 
          'extra':'Beyond Memorization: Ham Amateur Extra Class'}
sub_titles = {'tech':'Building a Strong Foundation for New Amateur Operators', 
               'general':'Elevating Your Radio Skills and Expanding Horizons', 
               'extra':'Reaching the Pinnacle of Amateur Radio Expertise'}

assert args.license in ['tech', 'general', 'extra']



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
\usetikzlibrary{arrows.meta,positioning,shapes}
\usepackage{float}
\usepackage{wrapfig}
\usepackage{svg}
\usepackage{draftwatermark}
\usepackage{circuitikz}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{enumitem}
\setlist[itemize]{noitemsep}

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

% Part titles - typically very large, centered, with plenty of space
\titleformat{\part}[display]{\Huge\bfseries\centering}{PART \thepart}{20pt}{}[\vspace{2ex}]

% Chapter titles - large, can be either centered or left-aligned
\titleformat{\chapter}[display]{\huge\bfseries}{CHAPTER \thechapter}{20pt}{}[\vspace{1ex}]

% Section titles - moderately large, left-aligned
\titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}

% Subsection titles - slightly larger than body text
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}

% Subsubsection titles - normal size, unnumbered
\titleformat{\subsubsection}{\normalsize\bfseries}{}{0em}{}

% Ensure subsubsections are unnumbered in TOC as well
\setcounter{secnumdepth}{2}  % Only number down to subsection level

%\setcounter{tocdepth}{1}
\begin{document}

\begin{titlepage}
    \centering
    \vspace*{2cm}    
    {\Huge\bfseries <book_title>\par}
    \vspace{2cm}    
    {\Large <book_subtitle>\par}
    
    \vspace{3cm}
    
    {\large\today\par}
    
    \vfill
    
    {\large Prepared by AK6KP\par}
\end{titlepage}

\cleardoublepage

\tableofcontents
\newpage
"""

latex_content = latex_content.replace('<book_title>', titles[args.license])
latex_content = latex_content.replace('<book_subtitle>', sub_titles[args.license])


base_dir = args.license + '/'

with open(base_dir + 'toc.json', 'r') as f:
    toc = json.load(f)

for part in toc['parts']:
    part_id = part['label'].split(':')[1]
    print(part_id)
    latex_content += f"\\part{{{part['part_title']}}}\n"
    for chapter in part['chapters']:
        latex_content += f"\\chapter{{{chapter['chapter_title']}}}\n"
        chapter_id = chapter['label'].split(':')[1]
        first_section = True  # Add flag to track first section
        for section in chapter['sections']:
            section_id = section['label'].split(':')[1]
            latex_content += f"\\section{{{section['section_title']}}}\n"
            for subsection in section['subsections']:
                subsection_id = subsection['label'].split(':')[1]
                latex_file = f'{args.license}/contents/{part_id}/{chapter_id}/{section_id}/{subsection_id}'
                latex_file_path = latex_file + '.tex'
                # print(latex_file_path)
                if os.path.exists(latex_file_path):
                    latex_content += f"\\input{{{latex_file}}}\n"
                else:
                    print(f"Subsection {subsection_id} not found in {latex_file_path}")

latex_content += r"\end{document}"

# Write the LaTeX content to master.tex
with open(base_dir + f'{args.license}.tex', 'w') as f:
    f.write(latex_content)

print(f"{args.license}.tex has been generated successfully.")