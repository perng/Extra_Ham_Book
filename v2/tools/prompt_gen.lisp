(objective
  "Transform the attached JSON file into a reorganized JSON structure for a book chapter. The reorganization should focus on conceptual themes, with no content generation required at this stage. Do not generate anything except the JSON structure."
)

(requirements
  (chapter-organization
    "The chapter should have a unique label with prefix "chapter:"
    "Break the chapter into smaller sections based on conceptual themes."
    "Each section should cover no more than 8 questions."
    "Sections do not need to mirror the original structure but should be logically organized."
    "The order of the sections should be coherent and logical, it should not depend on the concepts not being covered in the previous sections."
    "The chapter should be organized into sections, each with a unique label."
  )

  (section-fields
    (field "title"
      "A title for the section."
    )
    (field "section_label"
      "A unique label for the section to be used in LaTeX."
    )
    (field "questions"
      "A list of question ID from the input JSON relevant to the section."
    )
    (field "concepts" "a list of concepts to be explained in the section.")
    (field "prompts"
      "A detailed list of prompts for the LLM chatbot to generate section content."
      "Prompts should be elaborated and specific."
      "For each new term, add a reference label for the glossary."
    )
    (field "image_prompts"
      "A list of prompts for generating visual content (plots, diagrams, etc.)."
      (image-prompt-fields
        (field "prompt" "Prompt for generating the image that would be helpful for the section, or search phrase for web image.")
        (field "software" "Specify the appropriate software/tool for generating the image (e.g., SVG, gnuplot, Matplotlib, Graphviz, KiCad, Python). or 'web' if the image is better sourced from the web.")
        (field "caption" "Caption for the image, for LaTeX use.")
        (field "label" "Label for the image, for LaTeX use.")        
      )
    )
    (field "table_prompt"
      "A list of prompts for generating LaTeX tables."
      (table-prompt-fields
        (field "prompt" "Prompt for generating the table that would be helpful for the section")
        (field "caption" "Caption for the table, for LaTeX use.")
        (field "label" "Label for the table, for LaTeX use.")
      )
    )
  )
  (section-size
    "Each section must cover a focused topic and include no more than 8 questions."
  )
)

(deliverable
  "A JSON file with the reorganized chapter structure, adhering to the above requirements."
)