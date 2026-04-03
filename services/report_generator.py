from utils.pdf_extractor import process_pdf_vlm
from ml.agentic_pipeline import LlangChainAgentPipeline, validate_ddr
from ml.groq_client import GroqClient
import json

class ReportGenerator:
    def __init__(self):
        self.lc_pipeline = LlangChainAgentPipeline()
        self.groq_client = GroqClient()

    def generate(self, inspection_pdf_path: str, thermal_pdf_path: str, max_pages: int = 5, groq_api_key: str | None = None, gemini_api_key: str | None = None) -> dict:
        """
        Main pipeline using LlamaIndex/LangChain Reasoning Agent pattern:
        1. VLM extracts unstructured text directly from images (Gemini 1.5 Flash).
        2. Summary Agent (Gemini 1.5 Pro) deduplicates and logically infers DDR payload.
        3. Validates output for 'Not Available' fallback explicitly.
        """
        
        # 1. Process PDFs natively as images and raw text
        inspection_images, inspection_text = process_pdf_vlm(inspection_pdf_path, max_pages)
        thermal_images, thermal_text = process_pdf_vlm(thermal_pdf_path, max_pages)
        
        # 2. Logic Layer 1: VLM Extraction
        insp_text = self.lc_pipeline.extract_from_pdf_images(inspection_images, "Inspection", pdf_text_context=inspection_text, groq_api_key=groq_api_key, gemini_api_key=gemini_api_key)
        therm_text = self.lc_pipeline.extract_from_pdf_images(thermal_images, "Thermal", pdf_text_context=thermal_text, groq_api_key=groq_api_key, gemini_api_key=gemini_api_key)
        
        # 3. Logic Layer 2: Summary Agent
        ddr_dict = self.lc_pipeline.summary_and_deduplicate(insp_text, therm_text, groq_api_key=groq_api_key)
        
        # 4. Validation
        ddr_validated = validate_ddr(ddr_dict)
        
        return {
            "structured_ddr": ddr_validated.model_dump(),
            "extracted_images": []  # Let VLM handle image mapping natively in the payload text
        }
    
    def generate_summary(self, ddr_json_str: str, groq_api_key: str | None = None) -> str:
        """Get a quick executive summary using Groq."""
        return self.groq_client.generate_executive_summary(ddr_json_str, api_key=groq_api_key)

