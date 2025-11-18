
import fitz
import io
import re

SECTION_KEYWORDS = [
    "abstract","introduction","background","method","model","architecture",
    "training","results","evaluation","conclusion","attention","encoding",
    "regularization","optimizer","dataset","analysis","experiments","framework",
    "machine","translation","positional","decoder","encoder","visualization"
]


def extract_pdf_blocks(pdf_stream):
    doc = fitz.open(stream=pdf_stream.read(), filetype="pdf")
    blocks = []

    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            text = ""
            sizes = []
            fonts = set()

            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text += " " + span["text"].strip()
                    sizes.append(span["size"])
                    fonts.add(span["font"])

            text = text.strip()
            if not text:
                continue

            avg_size = sum(sizes) / len(sizes)
            blocks.append({"text": text, "size": avg_size, "font": list(fonts)[0]})

    return blocks


def is_sentence(text):
    """Detect body text sentences."""
    if text[0].islower():
        return True

    # Contains punctuation normally not in headers
    if re.search(r"[,:()\"']", text):
        return True

    # Reject if contains stopwords indicating grammar
    if len(re.findall(r"\b(is|are|was|were|have|has|allow|generate|improve|learn|prevent|use)\b", text.lower())):
        return True

    # Reject long strings and numeric patterns
    if len(text.split()) > 7:
        return True

    return False


def detect_headings(blocks):
    sizes = sorted([b["size"] for b in blocks])
    body_size = sizes[len(sizes)//2]
    detected = {}

    for i, block in enumerate(blocks):
        text, size = block["text"], block["size"]

        if is_sentence(text):
            continue

        # Title case heuristic
        words = text.split()
        title_case_ratio = sum(w[0].isupper() for w in words) / len(words)

        score = 0

        if title_case_ratio >= 0.7:
            score += 1

        # Font priority
        if size > body_size * 1.12:
            score += 2

        # Contains known keywords
        if any(k in text.lower() for k in SECTION_KEYWORDS):
            score += 2

        # Numbered heading pattern
        if re.match(r"^\d+(\.\d+){0,2}", text):
            score += 2

        if score >= 3:
            detected[i] = text

    return detected


def build_sections(blocks, headings):
    sections = {}
    current = None

    for idx, block in enumerate(blocks):
        if idx in headings:
            current = headings[idx]
            sections[current] = ""
        elif current:
            sections[current] += " " + block["text"]

    return {k: v.strip() for k, v in sections.items() if len(v.split()) > 20}


def split_by_sections_and_subsections(pdf_data):
    if isinstance(pdf_data, (bytes, bytearray)):
        pdf_data = io.BytesIO(pdf_data)

    if isinstance(pdf_data, str):
        return {"Document": pdf_data}

    blocks = extract_pdf_blocks(pdf_data)
    headings = detect_headings(blocks)
    return build_sections(blocks, headings)


