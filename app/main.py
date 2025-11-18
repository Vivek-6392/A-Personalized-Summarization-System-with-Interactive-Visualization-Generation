# import streamlit as st
# from pdf_parser import extract_sections_from_pdf
# from tables_figures import extract_tables_figures
# from vector_db import VectorDB
# from summarizer import summarize_one_section_mistral, summarize_figure_or_table
# from chunker import split_by_sections_and_subsections
# from qa import answer_question

# import pdf2image
# import io
# from PIL import Image

# st.set_page_config(page_title="Research Summarizer", layout="wide")
# st.title("Research Summarizer")

# file = st.file_uploader("Upload a scientific PDF", type=["pdf"])
# vector_db = VectorDB()
# sections_dict, tables_figures = None, []
# pdf_pages = None

# if file:
#     file_bytes = file.read()

#     # ---- FIXED INDENTATION HERE ----
#     try:
#         pdf_pages = pdf2image.convert_from_bytes(
#             file_bytes,
#             poppler_path=r"C:\Users\vivek\Downloads\Release-25.11.0-0\poppler-25.11.0\Library\bin"
#         )
#     except Exception as e:
#         st.warning(f"PDF Preview failed: {str(e)}")

#     file_stream_1 = io.BytesIO(file_bytes)
#     file_stream_2 = io.BytesIO(file_bytes)

#     try:
#         extracted = extract_sections_from_pdf(file_stream_1)

#         if isinstance(extracted, dict):
#             full_text = "\n".join(str(v) for v in extracted.values())
#         else:
#             full_text = str(extracted)

#         sections_dict = split_by_sections_and_subsections(full_text)
#         vector_db.add_chunks({sec: str(chunk) for sec, chunk in sections_dict.items()})
#         tables_figures = extract_tables_figures(file_stream_2)

#     except Exception as e:
#         st.error(f"Document analysis error: {str(e)}")
#         sections_dict, tables_figures = None, []

#     # ---- PDF PREVIEW UI ----
#     if pdf_pages:
#         st.header("PDF Preview")
#         for idx, page in enumerate(pdf_pages):
#             resized_page = page.resize((500, int(500 * page.height / page.width)))
#             st.image(resized_page, caption=f"Page {idx+1}", use_container_width=True)

#     # ---- SECTION VIEW + SUMMARIZATION ----
#     if sections_dict:
#         st.header("Detected Sections & Subsections")
#         st.write(list(sections_dict.keys()))

#         if st.button("Summarize Sections"):
#             progress = st.progress(0)

#             for idx, (heading, chunk) in enumerate(sections_dict.items()):
#                 with st.expander(heading):
#                     st.write(chunk[:500] + ("..." if len(chunk) > 500 else ""))
#                     with st.spinner("Summarizing..."):
#                         summary = summarize_one_section_mistral(heading, chunk)
#                         st.write("**Summary:**")
#                         st.write(summary)

#                 progress.progress((idx + 1) / len(sections_dict))

#     # ---- FIGURES + TABLES ----
#     if tables_figures:
#         st.header("Figures & Tables")
#         for tf in tables_figures:
#             col_img, col_info = st.columns([1,2])
#             with col_img:
#                 if tf.get("img_bytes"):
#                     img = Image.open(io.BytesIO(tf["img_bytes"]))
#                     if img.width > 300:
#                         img = img.resize((300, int(300 * img.height / img.width)))
#                     st.image(img, caption=f"{tf['type']} — Page {tf['page']}")
#             with col_info:
#                 st.write(f"**Title:** {tf.get('title_guess', '')}")
#                 st.write(f"**OCR Text:** {tf.get('ocr_text', '(no text detected)')}")
#                 if tf.get("ocr_text", "").strip():
#                     with st.spinner("Summarizing..."):
#                         st.write(summarize_figure_or_table(tf['ocr_text'], tf['title_guess']))
#             st.markdown("---")

#     # ---- Q&A MODULE ----
#     st.header("Ask a Question")
#     question = st.text_input("Ask about the paper")
#     if st.button("Get Answer") and sections_dict:
#         st.write(answer_question(vector_db, question))

# else:
#     st.info("Upload a PDF research paper to begin.")



# import streamlit as st
# import io
# from PIL import Image
# import pdf2image

# from pdf_parser import extract_sections_from_pdf
# from tables_figures import extract_tables_figures
# from vector_db import VectorDB
# from summarizer import summarize_one_section_mistral, summarize_figure_or_table
# from chunker import split_by_sections_and_subsections
# from qa import answer_question


# # -------------------------
# # Streamlit UI Setup
# # -------------------------
# st.set_page_config(page_title="Research Summarizer", layout="wide")
# st.title("📄 Research Paper Analyzer")

# file = st.file_uploader("Upload a scientific PDF", type=["pdf"])
# vector_db = VectorDB()
# sections_dict, tables_figures = None, []
# pdf_pages = None


# # -------------------------
# # MAIN EXECUTION
# # -------------------------
# if file:
#     file_bytes = file.read()

#     # ---- PAGE PREVIEW ----
#     try:
#         pdf_pages = pdf2image.convert_from_bytes(
#             file_bytes,
#             poppler_path=r"C:\Users\vivek\Downloads\Release-25.11.0-0\poppler-25.11.0\Library\bin"
#         )
#     except Exception as e:
#         st.warning(f"⚠ PDF Preview failed: {str(e)}")

#     file_stream_1 = io.BytesIO(file_bytes)
#     file_stream_2 = io.BytesIO(file_bytes)

#     try:
#         # ---- Extract text for AI use & fallback ----
#         extracted = extract_sections_from_pdf(file_stream_1)

#         if isinstance(extracted, dict):
#             full_text = "\n".join(str(v) for v in extracted.values())
#         else:
#             full_text = str(extracted)

#         # ---- CHUNK USING PDF STRUCTURE ----
#         sections_dict = split_by_sections_and_subsections(file_bytes)

#         # ---- Fallback if no headings detected ----
#         if not sections_dict or len(sections_dict) <= 1:
#             sections_dict = {"Document": full_text}

#         # ---- Add chunks to vector DB ----
#         vector_db.add_chunks({sec: str(chunk) for sec, chunk in sections_dict.items()})

#         # ---- Extract Figures/Tables ----
#         tables_figures = extract_tables_figures(file_stream_2)

#     except Exception as e:
#         st.error(f"❌ Document analysis error: {str(e)}")
#         sections_dict, tables_figures = None, []


#     # -------------------------
#     # PDF Preview Display
#     # -------------------------
#     if pdf_pages:
#         st.header("📑 PDF Preview")
#         for idx, page in enumerate(pdf_pages):
#             resized = page.resize((500, int(500 * page.height / page.width)))
#             st.image(resized, caption=f"Page {idx + 1}", use_container_width=True)


#     # -------------------------
#     # SECTION VIEW + SUMMARIZER
#     # -------------------------
#     if sections_dict:
#         st.header("📌 Detected Sections & Subsections")
#         st.write(list(sections_dict.keys()))

#         if st.button("✨ Summarize Sections"):
#             progress = st.progress(0)

#             for idx, (heading, chunk) in enumerate(sections_dict.items()):
#                 with st.expander(heading):
#                     st.write(chunk[:800] + ("..." if len(chunk) > 800 else ""))
#                     with st.spinner("Generating summary..."):
#                         summary = summarize_one_section_mistral(heading, chunk)
#                         st.write("🧠 **Summary:**")
#                         st.write(summary)

#                 progress.progress((idx + 1) / len(sections_dict))


#     # -------------------------
#     # FIGURES + TABLES
#     # -------------------------
#     if tables_figures:
#         st.header("🖼 Figures & Tables")
#         for tf in tables_figures:
#             col_img, col_info = st.columns([1, 2])

#             with col_img:
#                 if tf.get("img_bytes"):
#                     img = Image.open(io.BytesIO(tf["img_bytes"]))
#                     if img.width > 300:
#                         img = img.resize((300, int(300 * img.height / img.width)))
#                     st.image(img, caption=f"{tf['type']} — Page {tf['page']}")

#             with col_info:
#                 st.write(f"**Title Guess:** {tf.get('title_guess', '')}")
#                 st.write(f"**OCR Text:** {tf.get('ocr_text', '(None)')}")

#                 if tf.get("ocr_text", "").strip():
#                     with st.spinner("Summarizing..."):
#                         st.write(summarize_figure_or_table(tf['ocr_text'], tf['title_guess']))

#             st.markdown("---")


#     # -------------------------
#     # Q&A MODULE
#     # -------------------------
#     st.header("💬 Ask a Question")
#     question = st.text_input("Ask anything about the paper:")

#     if st.button("🔍 Get Answer") and sections_dict:
#         st.write(answer_question(vector_db, question))


# else:
#     st.info("📥 Upload a PDF research paper to begin.")


import streamlit as st
import io
from PIL import Image
import pdf2image

from pdf_parser import extract_sections_from_pdf
from tables_figures import extract_tables_figures
from vector_db import VectorDB
from summarizer import summarize_one_section_mistral, summarize_figure_or_table
from chunker import split_by_sections_and_subsections
from qa import answer_question


# -------------------------
# UI CONFIG
# -------------------------
st.set_page_config(page_title="Research Summarizer", layout="wide")
st.title("📄 Research Paper Analyzer")


# -------------------------
# FILE INPUT
# -------------------------
file = st.file_uploader("Upload a scientific PDF", type=["pdf"])
vector_db = VectorDB()
sections_dict, tables_figures = None, []
pdf_pages = None


# -------------------------
# WHEN PDF IS UPLOADED
# -------------------------
if file:
    file_bytes = file.read()

    # ---- PDF preview (optional) ----
    try:
        pdf_pages = pdf2image.convert_from_bytes(
            file_bytes,
            poppler_path=r"C:\Users\vivek\Downloads\Release-25.11.0-0\poppler-25.11.0\Library\bin"
        )
    except Exception as e:
        st.warning(f"⚠ PDF preview unavailable: {str(e)}")

    file_stream_1 = io.BytesIO(file_bytes)
    file_stream_2 = io.BytesIO(file_bytes)

    try:
        # ---- Extract raw cleaned text (backup + summary use) ----
        extracted = extract_sections_from_pdf(file_stream_1)

        if isinstance(extracted, dict):
            full_text = "\n".join(str(v) for v in extracted.values())
        else:
            full_text = str(extracted)

        # ---- USE NEW CHUNKER (layout-aware) ----
        sections_dict = split_by_sections_and_subsections(file_bytes)

        # ---- Fallback if no headings detected ----
        if not sections_dict or len(sections_dict) <= 1:
            sections_dict = {"Document": full_text}

        # ---- Add chunks to vector DB (searchable AI memory) ----
        vector_db.add_chunks({sec: str(chunk) for sec, chunk in sections_dict.items()})

        # ---- Extract tables + figures ----
        tables_figures = extract_tables_figures(file_stream_2)

    except Exception as e:
        st.error(f"❌ Document analysis failed: {str(e)}")
        sections_dict, tables_figures = None, []


    # -------------------------
    # PDF PAGE THUMBNAILS
    # -------------------------
    if pdf_pages:
        st.header("📑 PDF Preview")
        for idx, page in enumerate(pdf_pages):
            resized = page.resize((500, int(500 * page.height / page.width)))
            st.image(resized, caption=f"Page {idx + 1}", use_container_width=True)


    # -------------------------
    # SECTIONS + SUMMARIZATION UI
    # -------------------------
    if sections_dict:
        st.header("📌 Detected Sections")
        st.write(list(sections_dict.keys()))

        if st.button("✨ Summarize All Sections"):
            progress = st.progress(0)

            for idx, (heading, chunk) in enumerate(sections_dict.items()):
                with st.expander(heading):
                    st.write(chunk[:1000] + ("..." if len(chunk) > 1000 else ""))
                    with st.spinner("Generating summary..."):
                        summary = summarize_one_section_mistral(heading, chunk)
                        st.write("🧠 **Summary:**")
                        st.write(summary)

                progress.progress((idx + 1) / len(sections_dict))


    # -------------------------
    # TABLES + FIGURES PROCESSING
    # -------------------------
    if tables_figures:
        st.header("🖼 Extracted Figures & Tables")

        for tf in tables_figures:
            col_img, col_info = st.columns([1, 2])

            with col_img:
                if tf.get("img_bytes"):
                    img = Image.open(io.BytesIO(tf["img_bytes"]))
                    if img.width > 350:
                        img = img.resize((350, int(350 * img.height / img.width)))
                    st.image(img, caption=f"{tf['type']} — Page {tf['page']}")

            with col_info:
                st.write(f"**Title Guess:** {tf.get('title_guess', '')}")
                st.write(f"**OCR Text:** {tf.get('ocr_text', '(None extracted)')}")

                if tf.get("ocr_text", "").strip():
                    with st.spinner("Summarizing..."):
                        st.write(summarize_figure_or_table(tf['ocr_text'], tf['title_guess']))

            st.markdown("---")


    # -------------------------
    # QUESTION-ANSWERING MODULE
    # -------------------------
    st.header("💬 Ask Questions About the Paper")
    question = st.text_input("Enter a question:")

    if st.button("🔍 Get Answer") and sections_dict:
        st.write(answer_question(vector_db, question))


else:
    st.info("📥 Upload a PDF to begin.")
