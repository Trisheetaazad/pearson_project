import json
import os

FEEDBACK_FILE = "data/human_edits.jsonl"

def save_feedback(original_summary, edited_summary, case_id):
    feedback_data = {
        "case_id": case_id,
        "original": original_summary,
        "edited": edited_summary,
        "timestamp": datetime.now().isoformat()
    }
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
    with open(FEEDBACK_FILE, "a") as f:
        f.write(json.dumps(feedback_data) + "\n")

def get_learning_examples(limit=3):
    if not os.path.exists(FEEDBACK_FILE):
        return "No previous examples available."
    
    examples = []
    try:
        with open(FEEDBACK_FILE, "r") as f:
            lines = f.readlines()
            # Get the most recent edits
            for line in lines[-limit:]:
                data = json.loads(line)
                examples.append(f"AI Draft: {data['original']}\nHuman Corrected Style: {data['edited']}")
    except Exception:
        return "Error loading examples."
        
    return "\n\n---\n\n".join(examples)