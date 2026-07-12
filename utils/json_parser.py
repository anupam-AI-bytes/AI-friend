import json
import re


def parse_gemini_json(text):
    """
    Extracts the JSON array from Gemini's response
    and converts it into Python objects.
    """

    # Remove markdown code fences
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    # Find the first JSON array
    match = re.search(r"\[.*\]", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON array found in Gemini response.")

    json_text = match.group(0)

    return json.loads(json_text)