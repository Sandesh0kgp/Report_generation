import google.generativeai as genai
from core.config import settings
from ml.prompts import SYSTEM_PROMPT
import json

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Using gemini-1.5-pro for complex multi-modal and reasoning tasks over large documents
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
    def generate_ddr(self, inspection_text: str, thermal_text: str, images_data: list, schema: dict) -> dict:
        """
        Generate DDR using Gemini's multimodal capabilities. 
        """
        
        prompt = f"""{SYSTEM_PROMPT}
        
INSPECTION REPORT DATA:
{inspection_text}

THERMAL REPORT DATA:
{thermal_text}

Analyze the provided inputs. Output MUST be a valid JSON matching this schema:
{json.dumps(schema, indent=2)}
"""
        
        # Prepare contents
        contents = [prompt]
        
        # In a real multimodal scenario, we'll append PIL images here.
        # Format the images for Gemini
        for img_obj in images_data:
             contents.append({
                 "mime_type": "image/jpeg",
                 "data": img_obj['base64_data']
             })
             
        # Call model
        response = self.model.generate_content(
            contents,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        
        try:
            return json.loads(response.text)
        except Exception as e:
            raise ValueError(f"Failed to parse Gemini response as JSON: {response.text}")
