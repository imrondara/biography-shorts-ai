from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE = Path(__file__).parent
app = FastAPI(title="Biography Shorts AI Studio", version="0.1.0")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

JOBS = {}

class GenerateRequest(BaseModel):
    person: str = Field(min_length=2, max_length=100)
    category: str = "บุคคลทั่วไป"
    tone: str = "สารคดีเข้มข้น"
    duration_seconds: int = Field(default=60, ge=30, le=90)
    language: str = "ไทย"

@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")

@app.get("/api/health")
def health():
    return {"ok": True, "project": "BIOGRAPHY SHORTS AI STUDIO", "version": "0.1.0"}

@app.post("/api/generate")
def generate(req: GenerateRequest):
    # Stage 1 prototype: validate the request and prepare a production brief.
    # AI research, voice generation, footage retrieval and FFmpeg rendering
    # will be connected in later stages. Do not treat this as verified biography.
    job_id = str(uuid4())[:8]
    brief = {
        "job_id": job_id,
        "status": "brief_ready",
        "person": req.person,
        "category": req.category,
        "tone": req.tone,
        "duration_seconds": req.duration_seconds,
        "language": req.language,
        "notice": "ต้นแบบขั้นที่ 1: ยังไม่ได้ค้นคว้าข้อเท็จจริงหรือเรนเดอร์วิดีโอ"
    }
    JOBS[job_id] = brief
    return brief

@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="ไม่พบงานนี้")
    return JOBS[job_id]
