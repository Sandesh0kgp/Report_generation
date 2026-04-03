from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import json
from models.schemas import DDRResponse
from core.config import settings
from utils.image_handler import process_and_encode_image
from core.logger import get_logger
from core.exceptions import LLMProcessingError

logger = get_logger(__name__)

class LlangChainAgentPipeline:
    def __init__(self):
        # Initializing Groq Llama 4 Scout as the VLM Extractor
        self.vlm_extractor = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            api_key=settings.GROQ_API_KEY,
            temperature=0.1
        )
        
        # Initializing Groq Llama 3.3 70B Versatile for the Logic/Summary Agent
        self.reasoning_agent = ChatGroq(
            model="llama-3.3-70b-versatile",
            model_name="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY,
            temperature=0.2
        )

    def extract_from_pdf_images(self, page_images, report_type="Inspection", pdf_text_context: str = "", groq_api_key=None, gemini_api_key=None):
        """Feed pages natively as images and raw text context to VLM for extraction"""
        prompt = f"""
        Extract all observations, locations (Area), and Photo IDs from this {report_type} report.
        If any data is missing or images lack IDs, write 'Not Available'.
        Ensure you do not invent facts.
        """
        
        if pdf_text_context and pdf_text_context.strip():
            prompt += f"\n\nADDITIONAL RAW TEXT CONTEXT FROM PDF:\n{pdf_text_context}"
        
        try:
            logger.info("Triggering Native Groq Scout VLM for Image Extraction.")
            from groq import Groq
            import os
            client = Groq(api_key=groq_api_key or os.environ.get("GROQ_API_KEY", settings.GROQ_API_KEY))
            # Llama 4 natively enforces a strict 5-image boundary limit per payload string
            chunk_size = 5
            all_text_results = []
            
            for i in range(0, len(page_images), chunk_size):
                chunk = page_images[i:i + chunk_size]
                
                message_content = [{"type": "text", "text": prompt}]
                for img in chunk:
                    b64_img = process_and_encode_image(img)
                    message_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}})
                    
                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[{"role": "user", "content": message_content}],
                    temperature=0.1
                )
                all_text_results.append(response.choices[0].message.content)
                
            return "\n".join(all_text_results)
        except Exception as e:
            error_str = str(e).lower()
            if "rate limit" in error_str or "tokens" in error_str or "429" in error_str:
                logger.warning("Groq Vision API limit reached! Falling back securely to Gemini 1.5 Flash.")
                import google.generativeai as genai
                import os
                genai.configure(api_key=gemini_api_key or os.environ.get("GEMINI_API_KEY", settings.GEMINI_API_KEY))
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                
                # Gemini natively accepts PIL objects and text in an array
                gemini_input = [prompt]
                for img in page_images:
                    gemini_input.append(img)
                    
                gem_resp = model.generate_content(gemini_input)
                return gem_resp.text
            else:
                logger.error(f"VLM Extraction Error: {str(e)}")
                raise LLMProcessingError(f"Vision Layer failed to process images: {str(e)}")

    def summary_and_deduplicate(self, insp_data: str, therm_data: str, groq_api_key=None) -> dict:
        """Reasoning Agent pattern: Deduplicate, resolve conflicts, and infer"""
        
        schema_str = json.dumps(DDRResponse.model_json_schema(), indent=2)
        sys_prompt = f"""
        You are a Summary & Logic Agent.
        INSTRUCTIONS:
        1. Compare findings from the Inspection Report and Thermal Report.
        2. Merging (Deduplication): If both reports mention the same issue (e.g. Dampness), merge them into one point under the area.
        3. Conflict Resolution: If inspection says no leak but thermal shows a coldspot, explicitly flag the conflict.
        4. Infer Probable Root Cause based on synthesized data.
        5. For missing data fields, strictly output 'Not Available'. Do not invent facts.
        
        Output MUST strictly be JSON matching this exact DDRResponse schema structure.
        SCHEMA:
        {schema_str}
        """
        
        user_prompt = f"""
        INSPECTION DATA:
        {insp_data}
        
        THERMAL DATA:
        {therm_data}
        
        Return the final structured JSON only.
        """
        
        try:
            logger.info("Triggering Native Llama 3.3 Versatile Agent for Deduplication.")
            from groq import Groq
            import os
            client = Groq(api_key=groq_api_key or os.environ.get("GROQ_API_KEY", settings.GROQ_API_KEY))
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            content_txt = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
            return json.loads(content_txt)
        except json.JSONDecodeError as e:
            logger.error(f"JSON Parse Error from Agent: {str(e)}")
            raise LLMProcessingError("Reasoning Agent failed to output valid JSON.")
        except Exception as e:
            logger.error(f"Reasoning Agent Error: {str(e)}")
            raise LLMProcessingError(f"Reasoning process failed: {str(e)}")

def validate_ddr(ddr_dict: dict) -> DDRResponse:
    """Validate logic checking for 'Not Available' patterns as required."""
    try:
        obj = DDRResponse(**ddr_dict)
    except Exception as e:
        logger.error(f"Pydantic Validation Error: {e}")
        obj = DDRResponse()  # Completely empty fallback to bypass fatal 500s
        
    # Custom post-validation mapping
    if not obj.probable_root_cause or obj.probable_root_cause == "":
        obj.probable_root_cause = "Not Available"
        
    return obj
