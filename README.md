# Report_generation

A state-of-the-art vision-language-model (VLM) pipeline designed to ingest, process, and automatically formulate Detailed Diagnostic Reports (DDR) from raw Inspection and Thermal PDF documents.

## Features
- **Hybrid VLM Extraction**: Simultaneously ingests PyMuPDF scaled visual renders and deterministic raw text vectors to process anomaly reports with extreme accuracy.
- **Agentic Deduplication**: Analyzes issues found across thermal and standard inspections, naturally deduplicating occurrences and flagging contradictory data.
- **Automated Fallbacks**: Automatically shifts from Groq Llama 4 Scout down to Gemini 1.5 Flash upon rate-limits or quota exhaustion.
- **Dynamic SPA Frontend**: Features a beautiful glassmorphic frontend utilizing Single Page Application (SPA) functionality, entirely decoupled from hard browser reloads.
- **Premium Security**: Protected via an aesthetically constrained, micro-animated login gateway.
- **Dynamic UI Overrides**: Out of API quota? Safely inject fallback API keys straight into the system right from the user interface sidebar.

## Quick Start
1. Create a Python Virtual Environment (`uv`, `venv`, etc.) and activate it:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   ```
2. Install the core requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Boot the FastAPI Server:
   ```bash
   uvicorn main:app --port 8005 --reload
   # Or use the provided batch script: start_server.bat
   ```
4. Access the web dashboard at `http://localhost:8005/`.

## Authentication
By default, the gateway strictly restricts access to the dashboard. 
- **Username:** `admin`
- **Password:** `admin`

## Architecture Overview
- `frontend/index.html`: The HTML/Vanilla CSS logic storing the SPA router, authentication card, and dynamic API endpoints.
- `main.py`: The FastAPI controller handling POST multipart requests and routing fallback API keys correctly.
- `ml/agentic_pipeline.py`: The brain of the operation. Ingests logic constraints, manages prompts, triggers API switches to Gemini/Groq natively, and ensures strict pydantic JSON typing over raw text.
- `utils/pdf_extractor.py`: Extracts raw text alongside physical image frames synchronously to be ingested structurally by the Vision Models.

## Deploying to Production (Render)
This backend natively intercepts API calls dynamically (`fetch('/process')`), making it 100% compliant with standard Render.com Web Services deployments. Set your host loop to `0.0.0.0` and launch perfectly. Ensure your `.env` variables (`GROQ_API_KEY` & `GEMINI_API_KEY`) are inputted manually within your deployment environment configurations.
