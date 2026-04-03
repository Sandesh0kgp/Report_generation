import fitz  # PyMuPDF
from PIL import Image
import io
import os
from typing import List, Dict, Any

class PDFExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = fitz.open(file_path)

    def extract_pages_as_images_and_text(self, max_pages: int = 0):
        """Convert entire PDF pages to images and texts."""
        page_images = []
        text_content = []
        limit = len(self.doc) if max_pages <= 0 else min(len(self.doc), max_pages)
        for page_num in range(limit):
            page = self.doc[page_num]
            text_content.append(page.get_text())
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for better resolution
            image_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(image_bytes))
            page_images.append(image)
        return page_images, "\n".join(text_content)

    def close(self):
        self.doc.close()

def process_pdf_vlm(file_path: str, max_pages: int = 0) -> tuple[List[Image.Image], str]:
    """Helper to extract pages as images and text for VLM."""
    extractor = PDFExtractor(file_path)
    page_images, text_content = extractor.extract_pages_as_images_and_text(max_pages)
    extractor.close()
    return page_images, text_content
