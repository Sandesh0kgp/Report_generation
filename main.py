from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import json

from core.logger import get_logger
from core.exceptions import DDRException
from services.report_generator import ReportGenerator
from output.markdown_builder import build_markdown_report

logger = get_logger(__name__)
app = FastAPI(title="Automated DDR API", description="Detailed Diagnostic Report API")

@app.exception_handler(DDRException)
async def ddr_exception_handler(request: Request, exc: DDRException):
    logger.error(f"DDR Custom Exception Intercepted: {exc.message}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message, "status": "error"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

report_generator = ReportGenerator()

# Temp directory to store uploads
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

class ProcessingResponse(BaseModel):
    status: str
    markdown_report: str
    raw_data: dict
    summary_text: str

@app.post("/process", response_model=ProcessingResponse)
async def process_reports(
    inspection_file: UploadFile = File(...),
    thermal_file: UploadFile = File(...),
    max_pages: int = Form(5),
    groq_api_key: str | None = Form(None),
    gemini_api_key: str | None = Form(None)
):
    try:
        # Save temp files
        insp_path = os.path.join(TEMP_DIR, f"insp_{inspection_file.filename}")
        therm_path = os.path.join(TEMP_DIR, f"therm_{thermal_file.filename}")
        
        with open(insp_path, "wb") as f1, open(therm_path, "wb") as f2:
            shutil.copyfileobj(inspection_file.file, f1)
            shutil.copyfileobj(thermal_file.file, f2)
            
        # Run Pipeline
        pipeline_result = report_generator.generate(insp_path, therm_path, max_pages, groq_api_key, gemini_api_key)
        ddr_data = pipeline_result['structured_ddr']
        
        # Get Groq Summary
        summary = report_generator.generate_summary(json.dumps(ddr_data), groq_api_key)
        
        # Build Markdown
        markdown_str = build_markdown_report(ddr_data, summary_text=summary)
        
        return ProcessingResponse(
            status="success",
            markdown_report=markdown_str,
            raw_data=ddr_data,
            summary_text=summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(insp_path):
            os.remove(insp_path)
        if os.path.exists(therm_path):
            os.remove(therm_path)

from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse("frontend/index.html")
