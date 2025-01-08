import json

# Load TOC data
with open('tech/toc.json', 'r') as f:
    toc_data = json.load(f)

# Load questions data
with open('../v2/tech/questions2.json', 'r') as f:
    questions_data = json.load(f)

# Get all question IDs from questions2.json
question_ids = set()
for chapter in questions_data:
    for section in chapter['sections']:
        for question in section['questions']:
            question_ids.add(question['question_id'])

# Get all question IDs from TOC and track duplicates
toc_questions = set()
duplicate_questions = set()

def process_chapters(chapters):
    for chapter in chapters:
        for section in chapter.get('sections', []):
            for subsection in section.get('subsections', []):
                for qid in subsection.get('questions', []):
                    if qid in toc_questions:
                        duplicate_questions.add(qid)
                    else:
                        toc_questions.add(qid)

# Process all parts and their chapters
for part in toc_data['parts']:
    process_chapters(part['chapters'])

# Find missing questions (in questions2.json but not in toc.json)
missing_questions = question_ids - toc_questions

# Print results
print("Duplicate questions in toc.json:")
for qid in sorted(duplicate_questions):
    print(f"  {qid}")

print("\nQuestions in questions2.json but missing from toc.json:")
for qid in sorted(missing_questions):
    print(f"  {qid}")

print(f"\nSummary:")
print(f"Total questions in questions2.json: {len(question_ids)}")
print(f"Total questions in toc.json: {len(toc_questions)}")
print(f"Number of duplicate questions: {len(duplicate_questions)}")
print(f"Number of missing questions: {len(missing_questions)}")