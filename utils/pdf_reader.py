import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file):

    """
    Reads an uploaded PDF and returns all text as a single string.
    """

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""

    for page in pdf:

        text += page.get_text()

    pdf.close()

    return text