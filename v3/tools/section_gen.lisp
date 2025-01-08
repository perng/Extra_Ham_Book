 (objective "Generate a subsection for a book chapter in LaTeX format according the input JSON file."
    "do not generate anything other than the LaTeX code")

 (subsection_elements
    (element 'title 
        "subsection title should be taken from 'title' field in the input JSON file."        
    )
    (element 'label
        "subsection label should be taken from 'label' field in the input JSON file."
    )
    (element 'subsection_text
        "generate LaTeX text according to the 'prompts' field in the input JSON file. "
        "Assume the reader has read the previous sections and knows the context, know enough math to follow the calculation."
        "Assume the reader only knows very basic physics"        
        "All formulas should be numbered  and referenced by their number."
        "Assume the images and tables are already generated and can be referenced by their label"
        "Write with a more relaxed tone, like a conversation with the reader, with some appropriate humor."        
        "subsections should be numbered as '\subsection{...}"
        "subsubsections should be unnumbered as '\subsubsection*{...}"
    )
    (element 'table 
        "generate LaTeX tables according to the 'table_prompt' field in the input JSON file."
        "If the table is not verey informative, or the information is already in the section_text, don't generate the table."
        "If the information to be conveyed is not tabular, don't generate the table. Add it to the section_text instead."
    )
    (element 'figure
        "generate figures according to the 'image_prompts' field in the input JSON file. use a commented out 'includegraphics' command in the figure as a place-holder for the image. Also elaborate the image prompt to make it more specific, describe what objects/plots should be in the figure. Put the prompt as comments in the figure. "    )
    (element ')    
    (element 'question 
        "add a bold-font title 'Questions'"
        "generate the multiple choice questions in a shaded box using '\\begin{{tcolorbox}}[colback=gray!10!white,colframe=black!75!black,title={question_id}]'
            then the question text, then enumerate (with noitemsep) the choices. 
            Mark the correct answer with bold. End with '\\end{{tcolorbox}}'."  
            "enumerate options should be \begin{enumerate}[label=\Alph*),noitemsep]"
            "the correct answer should be bold")
    (element 'explanation        
        "Do not say 'The correct answer is' as the correct answer is already bold in the question."
        "If the question is related to FCC Part 97, quote the relevant part of the regulation."
        "After each question, provide a  explanation. If calculation is required, show the calculation step by step. Also, explain why other options are wrong."
        "if the question can be answered from the subsection_text, make the explanation short and concise. Otherwise, explain the question in detail."
        "again! do not say 'The correct answer is'."        
    )
    
 )
   
