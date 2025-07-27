@echo off
echo Starting Agricultural Multi-Agent API Server...
echo.
echo Make sure you have activated your virtual environment first:
echo   .venv\Scripts\activate
echo.
echo Installing/Updating dependencies...
pip install -r requirements_api.txt
echo.
echo Starting server on http://localhost:8000
echo API docs will be available at http://localhost:8000/docs
echo.
python api_server.py
