 (objective "Generate a section for a book chapter in LaTeX format according the input JSON file.")

 (section_elements
    (element 'title 
        "section title should be taken from 'title' field in the input JSON file."        
    )
    (element 'label
        "section label should be taken from 'section_label' field in the input JSON file."
    )
    (element 'section_text
        "generate LaTeX text according to the 'prompts' field in the input JSON file. "
        "Assume the reader has read the previous sections and knows the context, know enough math to follow the calculation."
        "Assume the reader only knows very basic physics"        
        "All formulas should be numbered and referenced by their number."
        "Assume the images and tables are already generated and can be referenced by their label"        
        "subsection should be unnumbered"
    )
    (element 'table 
        "generate LaTeX tables according to the 'table_prompt' field in the input JSON file.")
    (element 'figure
        "generate figures according to the 'image_prompts' field in the input JSON file. use a commented out 'includegraphics' command in the figure as a place-holder for the image. Also elaborate the image prompt to make it more specific, describe what objects/plots should be in the figure. Put the prompt as comments in the figure. "    )
    (element 'question 
        "subsetion title is 'Questions'"
        "generate the multiple choice questions in a shaded box using '\\begin{{tcolorbox}}[colback=gray!10!white,colframe=black!75!black,title={question_id}]'
            then the question text, then enumerate (with noitemsep) the choices. 
            Mark the correct answer with bold. End with '\\end{{tcolorbox}}'."  
            "enumerate options should be \begin{enumerate}[label=\Alph*,noitemsep]"
            "the correct answer should be bold")
    (element 'explanation        
        "Do not say 'The correct answer is' as the correct answer is already bold in the question."
        "If the question is about FCC Part 97, quote the relevant part of the regulation."
        "After each question, provide a  explanation. If calculation is required, show the calculation step by step. Also, explain why other options are wrong."
        "if the question can be answered from the section_text, make the explanation short and concise. Otherwise, explain the question in detail."
        "At the end of the explanation, add a comment line '%memory_tric <question_id>'".
    )

    (element 'summary
        "generate a summary subsection titled 'Summary'"
        "List and explain the terms listed in the 'concepts' field in the input JSON file."
        "A few sentences that summarize the section. but don't say 'In Summary'"     
    )
 )
   
