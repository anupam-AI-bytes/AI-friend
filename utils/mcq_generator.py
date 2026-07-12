def build_mcq_prompt(pdf_text):

    prompt = f"""
You are an MBA professor.

Generate EXACTLY 10 multiple choice questions from the study material.

Return ONLY valid JSON.

The JSON format must be:

[
  {{
    "question": "...",
    "options": [
      "...",
      "...",
      "...",
      "..."
    ],
    "answer": 0,
    "explanation": "..."
  }}
]

Rules:

- No markdown.
- No code blocks.
- No extra text.
- Only JSON.
- Each question must have exactly 4 options.
- "answer" must be the index (0-3) of the correct option.
- Use ONLY the uploaded study material.

Study Material:

{pdf_text}
"""

    return prompt