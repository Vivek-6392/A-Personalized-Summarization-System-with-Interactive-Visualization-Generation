# 📄 Research Paper Analyzer & Visualization Assistant

An end-to-end AI-powered tool built using **Python**, **Streamlit**, and **local LLM inference** to automate the understanding, summarization, visualization, and analysis of scientific research papers and datasets.

---

## 🚀 Features

### 🔍 PDF Understanding & Extraction
- Extracts structured text, headings, and layout sections using **PyMuPDF**
- Detects and processes **tables and figures** using **OCR (EasyOCR)**
- Automatically identifies research sections (Abstract, Introduction, Methodology, Results, Conclusion)

### 🧠 LLM-Powered Summarization & Q&A
- Uses **local LLMs (Mistral/OpenChat via LM Studio)** for:
  - Section-wise summarization  
  - Q&A based on extracted content  
  - Figure/table interpretation  
- Implements **RAG (Retrieval-Augmented Generation)** using:
  - `SentenceTransformers` for embeddings  
  - **ChromaDB** for semantic storage and search  

### 📊 Interactive Data Visualization Assistant
- Upload CSV files and automatically:
  - Generate insights and metadata summaries  
  - Recommend visualization types  
  - Auto-generate charts (matplotlib / seaborn / plotly)  
  - Export usable Python visualization code  
- Powered by **LIDA framework** for automated reasoning and chart planning.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| UI | Streamlit |
| NLP / LLM | LM Studio, OpenChat, Mistral |
| OCR | EasyOCR |
| PDF Parsing | PyMuPDF (fitz) |
| Vector Indexing | ChromaDB + SentenceTransformers |
| Visualization | matplotlib, seaborn, plotly, LIDA |
| Utilities | Python, pandas, regex, dotenv |

---
