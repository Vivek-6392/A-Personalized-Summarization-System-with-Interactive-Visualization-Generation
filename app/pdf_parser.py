import fitz  # PyMuPDF

def extract_sections_from_pdf(pdf_file):
    if hasattr(pdf_file, "read"):
        raw_bytes = pdf_file.read()
    else:
        raw_bytes = pdf_file
    doc = fitz.open(stream=raw_bytes, filetype="pdf")

    all_text = ""
    sections = {}
    SECTION_KEYWORDS = [
        "abstract", "introduction", "background", "methods",
        "materials", "experiment", "results", "analysis",
        "discussion", "conclusion", "references", "acknowledgments"
    ]
    for page in doc:
        all_text += page.get_text("text") + "\n"

    current = "Title"
    buf = ""
    for line in all_text.splitlines():
        line_low = line.strip().lower()
        found_section = next((k for k in SECTION_KEYWORDS if k in line_low), None)
        if found_section and len(line.strip()) < 40:
            if buf.strip():
                sections[current] = buf.strip()
            current = found_section.capitalize()
            buf = ""
        else:
            buf += line + "\n"
    if buf.strip():
        sections[current] = buf.strip()
    return sections
