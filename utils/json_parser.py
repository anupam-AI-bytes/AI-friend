import json


def parse_gemini_json(text):
    """
    Cleans Gemini's response and converts it into Python objects.
    """

    # Remove markdown code fences if present

    cleaned = text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "", 1)

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```", "", 1)

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    return json.loads(cleaned)