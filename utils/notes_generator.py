def build_notes_prompt(pdf_text):

    prompt = f"""
You are an expert MBA professor.

Read the following study material carefully and prepare high-quality revision notes.

Generate your response using the following headings:

# 📖 Chapter Summary

Write a simple summary.

# 📝 Important Definitions

List all important definitions.

# 📌 Key Concepts

Explain the important concepts in bullet points.

# 📊 Important Formulas

List every important formula.
If there are no formulas, write:
"No important formulas found."

# 🎯 Exam Tips

Suggest important topics that students should revise.

Study Material:

{pdf_text}

"""

    return prompt