import os
import asyncio
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fraud_detection import analyze_with_groq
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="FraudGuard AI",
    description="Advanced fraud detection system powered by AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
@limiter.limit("30/minute")
async def home(request: Request):
    # Render the homepage containing the form.
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/healthz")
@limiter.limit("10/minute")
async def health_check(request: Request):
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "FraudGuard AI"}

@app.post("/analyze", response_class=JSONResponse)
@limiter.limit("5/minute")
async def analyze(request: Request, message: Optional[str] = Form(None), url: Optional[str] = Form(None)):
    # Check if at least one field is provided
    if not message and not url:
        return JSONResponse(
            status_code=400,
            content={"error": "At least one of message or URL must be provided"}
        )
    
    try:
        result = await analyze_with_groq(message, url)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Analysis failed: {str(e)}"}
        )

if __name__ == "__main__":
    # Run the FastAPI app on a different port to avoid conflicts
    uvicorn.run(app, host="0.0.0.0", port=8001) 