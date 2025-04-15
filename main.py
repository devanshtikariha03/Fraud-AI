import os
import asyncio
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from fraud_detection import analyze_with_groq
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render the homepage containing the form.
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=JSONResponse)
async def analyze(request: Request, message: Optional[str] = Form(None), url: Optional[str] = Form(None)):
    # Check if at least one field is provided
    if not message and not url:
        return JSONResponse(
            status_code=400,
            content={"error": "At least one of message or URL must be provided"}
        )
    
    # Run the fraud detection pipeline using GROQ
    result = await analyze_with_groq(message, url)
    return result

if __name__ == "__main__":
    # Run the FastAPI app on a different port to avoid conflicts
    uvicorn.run(app, host="0.0.0.0", port=8001) 