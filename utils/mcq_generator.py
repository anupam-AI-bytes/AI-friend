def build_mcq_prompt(pdf_text):

    prompt = f"""
You are an MBA professor.

The student has uploaded study material.

Generate 10 multiple choice questions ONLY from the uploaded PDF.

Rules:

- Each question must have 4 options.
- Mention the correct answer.
- After all questions, provide a short explanation for every answer.
- Do not use outside knowledge.
- Use only the uploaded study material.

Study Material:

{pdf_text}
"""

    return prompt