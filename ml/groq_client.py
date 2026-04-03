from groq import Groq
from core.config import settings
from ml.prompts import SUMMARY_PROMPT

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model_name = "llama-3.3-70b-versatile"
        
    def generate_executive_summary(self, ddr_json_str: str, api_key: str | None = None) -> str:
        """
        Uses Groq for fast inference of an executive summary.
        """
        client = Groq(api_key=api_key) if api_key else self.client
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SUMMARY_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following DDR report:\n{ddr_json_str}"
                }
            ],
            model=self.model_name,
            temperature=0.3,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
