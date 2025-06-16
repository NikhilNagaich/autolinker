from fastapi import FastAPI, APIRouter, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uuid
import sys
import os

# Ensure the root directory is in sys.path so pipeline.py can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import run_autolinker_pipeline  # Import your real pipeline

app = FastAPI()

# CORS setup for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://autolinker-aasf64pda-nikhilnagaichs-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")

# In-memory job store (for demo; use a database for production)
jobs: Dict[str, Dict[str, Any]] = {}

# Request/response models
class CrawlRequest(BaseModel):
    url: str

class ExtractResponse(BaseModel):
    job_id: str

# Background task to simulate crawling and extraction
def crawl_and_extract(job_id: str, url: str):
    jobs[job_id]["status"] = "in_progress"
    try:
        # Call your real pipeline here
        results = run_autolinker_pipeline(url)
        jobs[job_id]["results"] = results
        jobs[job_id]["status"] = "completed"
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["results"] = {"error": str(e)}

@router.post("/extract", response_model=ExtractResponse)
async def extract(request: CrawlRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "results": None}
    background_tasks.add_task(crawl_and_extract, job_id, request.url)
    return {"job_id": job_id}

@router.get("/status/{job_id}")
async def status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"status": "not_found"}
    return {"status": job["status"]}

@router.get("/results/{job_id}")
async def results(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"error": "Job not found"}
    if job["status"] != "completed":
        return {"error": "Job not completed yet"}
    return job["results"]

app.include_router(router)