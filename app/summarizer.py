from app.llm_client import generate_text

def summarize_one_section_mistral(heading, section_text, max_chunk_len=12000):
    """
    Summarizes a section using the local LM Studio model.
    """
    content = section_text[:max_chunk_len]

    prompt = (
        "Write a clear scientific summary of the following section. "
        "Keep it concise, structured, and avoid repeating text.\n\n"
        f"### Section Title:\n{heading}\n\n"
        f"### Original Text:\n{content}\n\n"
        "### Summary:"
    )

    messages = [
        {"role": "system", "content": "You are an expert academic summarizer."},
        {"role": "user", "content": prompt}
    ]

    summary = generate_text(messages)
    return summary if summary else "Summarization failed."


def summarize_figure_or_table(ocr_text, title=None, max_len=2048):
    """
    Summarizes an extracted figure/table/image using OCR text and optional caption.
    """
    ocr_text = ocr_text.strip()[:max_len]

    prompt = (
        "Summarize the content of this research figure/table. "
        "Explain what it represents, key findings, and relevance to the study.\n\n"
    )

    if title:
        prompt += f"**Title:** {title}\n\n"

    prompt += f"**Content Extracted via OCR:**\n{ocr_text}\n\nSummary:"

    messages = [
        {"role": "system", "content": "You summarize scientific figures and tables accurately."},
        {"role": "user", "content": prompt}
    ]

    summary = generate_text(messages)
    return summary if summary else "Summary failed."
