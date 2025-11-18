from app.llm_client import generate_text
from app.prompts import qa_prompt

def answer_question(vector_db, question, top_k=5, chunk_maxlen=3000):
    context_chunks, metas = vector_db.search(question, top_k=top_k)
    chunk_texts = []
    for chunk in context_chunks:
        if isinstance(chunk, list):
            chunk_texts.append(" ".join(str(x) for x in chunk)[:chunk_maxlen])
        else:
            chunk_texts.append(str(chunk)[:chunk_maxlen])
    context = "\n\n".join(chunk_texts)
    msg = [
        {"role": "system", "content": "Expert research Q&A assistant; only use provided text."},
        {"role": "user", "content": qa_prompt.format(sections=context, question=question)}
    ]
    # # 🧪 Debug: print what is being sent to the model
    # print("\n================ DEBUG LLM MESSAGE ================\n")
    # print(msg)
    # print("\n===================================================\n")
    answer = generate_text(msg)
    return answer if answer else "Q&A failed."
