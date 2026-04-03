class DDRException(Exception):
    """Base API Exception for Automated DDR Generation System"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class PDFExtractionError(DDRException):
    """Raised when PyMuPDF fails or VLM extraction formatting fails"""
    def __init__(self, message: str = "Failed to extract target data from PDF."):
        super().__init__(message, status_code=400)

class LLMProcessingError(DDRException):
    """Raised when Gemini or Groq fail their internal network generation steps"""
    def __init__(self, message: str = "LLM Engine Generation Failed."):
        super().__init__(message, status_code=502)
