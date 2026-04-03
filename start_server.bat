@echo off
echo =======================================================
echo     Automated DDR Generation - Server Boot Script
echo =======================================================

echo.
echo [1] Terminating any old servers blocking port 8005...
FOR /F "tokens=5" %%T IN ('netstat -a -n -o ^| findstr "8005"') DO (
    TaskKill.exe /PID %%T /F 2>NUL
)

echo.
echo [2] Activating strict UV Virtual Environment...
call .\.venv\Scripts\activate.bat

echo.
echo [3] Launching FastAPI Server with Groq Llama 4 Scout Engine...
python -m uvicorn main:app --port 8005 --reload

pause
