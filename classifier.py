from transformers import pipeline

O1A_CRITERIA = [
    "Awards",
    "Membership",
    "Press",
    "Judging",
    "Original Contribution",
    "Scholarly Articles",
    "Critical Employment",
    "High Remuneration"
]
classifier_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_text(text: str) -> dict:
    """
    Classify the provided text into O-1A criteria.
    
    Returns a dictionary with keys 'labels' and 'scores'.
    """
    result = classifier_pipeline(text, candidate_labels=O1A_CRITERIA, multi_label=True)
    return result

def get_overall_rating(result: dict) -> str:
    """
    Generate an overall rating (Low, Medium, High) based on the average score.
    This is a heuristic: average score > 0.75 => High, > 0.5 => Medium, else Low.
    """
    scores = result.get("scores", [])
    if not scores:
        return "Low"
    avg_score = sum(scores) / len(scores)
    if avg_score > 0.75:
        return "High"
    elif avg_score > 0.25:
        return "Medium"
    else:
        return "Low"
