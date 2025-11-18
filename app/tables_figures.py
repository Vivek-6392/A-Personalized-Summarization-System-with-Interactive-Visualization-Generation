import fitz
import easyocr

def extract_tables_figures(pdf_file):
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    reader = easyocr.Reader(['en'])
    
    results = []

    for pg_num, page in enumerate(doc):
        images = page.get_images(full=True)
        text_blocks = page.get_text("blocks")

        for img_index, img in enumerate(images):
            xref = img[0]

            # Extract image bytes
            pix = fitz.Pixmap(doc, xref)
            img_bytes = pix.tobytes("png")

            # OCR text
            ocr_result = reader.readtext(img_bytes)
            ocr_text = "\n".join([line[1] for line in ocr_result]) if ocr_result else ""

            # Detect nearest caption (below image area)
            bbox = page.get_image_bbox(img)
            possible_caption = ""
            for block in text_blocks:
                block_rect = fitz.Rect(block[:4])
                
                # Caption heuristic: text directly below the image, and short
                if block_rect.y0 > bbox.y1 and block_rect.y0 - bbox.y1 < 120:  
                    block_text = block[4].strip()
                    if 5 < len(block_text) < 200:
                        possible_caption = block_text
                        break

            # Heuristic type detection based on keywords
            ttype = "Figure"
            cleaned = (possible_caption + " " + ocr_text).lower()
            if any(word in cleaned for word in ["table", "dataset", "values", "rows", "columns"]):
                ttype = "Table"

            results.append({
                "type": ttype,
                "page": pg_num + 1,
                "coords": tuple(bbox),
                "ocr_text": ocr_text if ocr_text else "(No readable OCR text)",
                "title_guess": possible_caption or "",
                "img_bytes": img_bytes
            })

    return results
