import json

# Load questions from questions2.json
with open('questions2.json', 'r') as f:
    questions_data = json.load(f)

# Initialize a collection for wrong choices
W = set()

# Collect all wrong choices into W
for chapter in questions_data:
    for section in chapter['sections']:
        for question in section['questions']:
            for choice in question['choices'].values():
                if choice != question['choices'][question['answer']]:  # If it's not the right choice
                    W.update(choice.lower().split())  # Add words to the collection W in lowercase

# Function to find unique words from the right choice that do not appear in W
def find_unique_words(question):
    right_choice = question['choices'][question['answer']]
    words = right_choice.split()
    
    # Collect unique words that are not in W (case insensitive)
    unique_words = set(word for word in words if word.lower() not in W)  # Convert to lowercase for comparison
    
    return unique_words

# Prepare the results
results = []

# Process each question to find unique words
for chapter in questions_data:
    for section in chapter['sections']:
        for question in section['questions']:
            unique_words = find_unique_words(question)
            if unique_words:
                results.append({
                    "question_id": question['question_id'],
                    "unique_words": list(unique_words)  # Convert set to list for output
                })
                print(results[-1])
            else:
                print(f"No unique words found for question {question['question_id']}")

# Output the results
with open('unique_words.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Unique words have been collected and saved to unique_words.json.")