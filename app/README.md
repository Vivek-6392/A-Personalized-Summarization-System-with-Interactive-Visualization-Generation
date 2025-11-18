# Research Summarizer (Python, LM Studio, Streamlit)

## Features
- Upload scientific PDFs
- Section-based and full-paper AI summarization
- Figures/tables extraction with OCR
- Retrieval-Augmented Generation (RAG) Q&A
- All processing uses local openchat-3.6-8b via LM Studio

## Usage
1. Install requirements: `pip install -r requirements.txt`
2. Run LM Studio and load the openchat-3.6-8b model
3. Create `.env` file with LMSTUDIO_URL and OPENCHAT_MODEL
4. Start app: `streamlit run app/main.py`
