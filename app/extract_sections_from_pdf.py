import fitz  # PyMuPDF

def extract_sections_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    all_text = ""
    for page in doc:
        all_text += page.get_text("text") + "\n"
    return all_text

