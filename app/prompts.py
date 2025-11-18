summary_prompt = """
Summarize the following scientific section. Identify key findings, methodology, and conclusions—avoid repetition and irrelevant details.

Section: {section}
Content: {content}

Summary (max 200 words):
"""

qa_prompt = """
Use ONLY the following text chunks from the paper to answer the user's question clearly and with references (quote sections where possible).

Text Chunks:
{sections}

Question: {question}
Give a detailed, referenced answer:
"""
