import os
import time
from utils.notes_generator import build_notes_prompt
import streamlit as st
from dotenv import load_dotenv
from google import genai
from prompts import PROMPTS
from utils.pdf_reader import extract_text_from_pdf

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =====================================================
# Streamlit Page Configuration
# =====================================================

st.set_page_config(
    page_title="MBA AI Tutor",
    page_icon="🎓",
    layout="wide"
)

# =====================================================
# Session State Initialization
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Store current study mode

if "study_mode" not in st.session_state:
    st.session_state.study_mode = "General AI"
    
if "generate_notes" not in st.session_state:
    st.session_state.generate_notes = False

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""  

# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.title("🎓 MBA AI Tutor")

    st.caption("Powered by Gemini 2.5 Flash")

    st.divider()

    st.subheader("📚 Study Mode")

    selected_mode = st.selectbox(
        "Choose your tutor",
        list(PROMPTS.keys()),
        index=list(PROMPTS.keys()).index(
            st.session_state.study_mode
        )
    )

    # Detect study mode change

    if selected_mode != st.session_state.study_mode:

        st.session_state.study_mode = selected_mode

        st.session_state.messages = []

        st.rerun()

    st.success(f"Current Mode:\n\n{selected_mode}")
    st.divider()

st.subheader("📄 Study Material")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if uploaded_file.name != st.session_state.pdf_name:

        with st.spinner("Reading PDF..."):

            pdf_text = extract_text_from_pdf(uploaded_file)

            st.session_state.pdf_text = pdf_text

            st.session_state.pdf_name = uploaded_file.name

    st.success("✅ PDF Loaded")

    st.write(f"**File:** {uploaded_file.name}")

    st.caption(
        f"Characters: {len(st.session_state.pdf_text)}"
    )
    # =====================================================
# Notes Generator
# =====================================================

st.divider()

if st.button("📝 Generate Notes", use_container_width=True):

    if st.session_state.pdf_text == "":

        st.warning("Please upload a PDF first.")

    else:

        st.session_state.generate_notes = True

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.markdown("### ✨ What this tutor can do")

    st.markdown("""
- 📖 Explain concepts

- 📝 Help with assignments

- 💡 Solve doubts

- 📊 Solve numericals

- 🎯 Prepare for exams

- ❓ Generate practice questions

- 📚 Teach topics step-by-step
""")

# =====================================================
# Main Page Heading
# =====================================================

titles = {
    "General AI": "🤖 General AI Assistant",
    "Financial Management": "📈 Financial Management Tutor",
    "Marketing Management": "📢 Marketing Management Tutor",
    "Human Resource Management": "👨‍💼 Human Resource Management Tutor",
    "Organisational Behaviour": "🧠 Organisational Behaviour Tutor",
    "Project Management": "📋 Project Management Tutor",
    "Research Methodology": "📑 Research Methodology Tutor"
}

st.title(titles[selected_mode])

st.caption(
    "Ask any question related to the selected subject. "
    "Your tutor will answer according to the chosen study mode."
)

st.divider()

# =====================================================
# Display Previous Chat Messages
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =====================================================
# User Input
# =====================================================

user_prompt = st.chat_input("Ask your tutor anything...")

if user_prompt:

    # ---------------------------------------------
    # Display User Message
    # ---------------------------------------------

    st.chat_message("user").markdown(user_prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # ---------------------------------------------
    # Get Prompt for Selected Study Mode
    # ---------------------------------------------

    system_prompt = PROMPTS[selected_mode]

    # ---------------------------------------------
    # Build Conversation
    # ---------------------------------------------

    conversation = system_prompt + "\n\n"

    # Add uploaded PDF (if available)

    if st.session_state.pdf_text != "":

        conversation += """
The user has uploaded study material.

Instructions:
- Use the uploaded study material as your primary source.
- Answer using the uploaded document whenever possible.
- If the answer is not available in the uploaded document, clearly mention that before using your own knowledge.
- If the user asks for summaries, notes, formulas, important questions, viva questions, MCQs or explanations, generate them from the uploaded study material first.

Study Material:

"""

        conversation += st.session_state.pdf_text + "\n\n"

    # Add previous chat history

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            conversation += f"User: {msg['content']}\n"

        else:

            conversation += f"Assistant: {msg['content']}\n"

    conversation += "Assistant:"

    # ---------------------------------------------
    # Generate AI Response
    # ---------------------------------------------

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        with st.spinner("Thinking..."):

            max_retries = 3

            for attempt in range(max_retries):

                try:

                    stream = client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=conversation
                    )

                    for chunk in stream:

                        if hasattr(chunk, "text") and chunk.text:

                            full_response += chunk.text

                            message_placeholder.markdown(
                                full_response + "▌"
                            )

                    message_placeholder.markdown(full_response)

                    break

                except Exception as e:

                    error_message = str(e)

                    if (
                        "503" in error_message
                        or "UNAVAILABLE" in error_message
                    ):

                        if attempt < max_retries - 1:

                            message_placeholder.info(
                                f"🔄 Server busy... Retrying ({attempt + 1}/{max_retries})"
                            )

                            time.sleep(2)

                            continue

                    full_response = (
                        "❌ Sorry, I couldn't generate a response.\n\n"
                        f"Error: {e}"
                    )

                    message_placeholder.markdown(full_response)

                    break

    # ---------------------------------------------
    # Save AI Response
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

# =====================================================
# Welcome Screen
# =====================================================

if len(st.session_state.messages) == 0:

    st.info(
        """
👋 **Welcome to MBA AI Tutor!**

Choose a subject from the sidebar and start learning.

### You can ask things like:

📈 Financial Management
- Explain NPV
- Solve IRR numericals
- What is Working Capital?

📢 Marketing Management
- Explain STP
- What is the Marketing Mix?
- Explain Consumer Behaviour

👨‍💼 Human Resource Management
- What is Recruitment?
- Explain Performance Appraisal

🧠 Organisational Behaviour
- Explain Motivation
- Leadership Styles
- Organizational Culture

📋 Project Management
- Explain PERT
- Solve CPM Numericals

📑 Research Methodology
- What is Hypothesis?
- Explain Sampling Methods

🤖 General AI
- Ask anything you'd like.
"""
    )
# =====================================================
# Automatic Notes
# =====================================================

if st.session_state.generate_notes:

    st.header("📝 Automatic Notes")

    with st.spinner("Generating notes..."):

        notes_prompt = build_notes_prompt(
            st.session_state.pdf_text
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=notes_prompt
        )

        notes = response.text

    st.markdown(notes)

    st.download_button(
        "⬇ Download Notes",
        notes,
        file_name="MBA_Notes.txt",
        mime="text/plain"
    )

    st.session_state.generate_notes = False

# =====================================================
# Footer
# =====================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.caption(f"📚 Current Tutor: **{selected_mode}**")

with col2:

    st.caption("🚀 Built using Streamlit + Gemini 2.5 Flash")