import sys
import logging
from core.config import settings

print(f"Loaded GROQ Key: {settings.GROQ_API_KEY[:5]}...")

from utils.pdf_extractor import process_pdf_vlm
from ml.agentic_pipeline import LlangChainAgentPipeline

def run_test():
    try:
        inspection_images = process_pdf_vlm("test_data/sample_inspection.pdf")[:1]
        pipeline = LlangChainAgentPipeline()
        
        insp_text = pipeline.extract_from_pdf_images(inspection_images, "Inspection")
        print("SUCCESS VLM!")
        
        res = pipeline.summary_and_deduplicate(insp_text, "Dummy thermal data: cold spot found")
        print("SUCCESS REASONING!")
        print(res)
    except Exception as e:
        print("FAILURE:", e)
        
if __name__ == "__main__":
    run_test()
