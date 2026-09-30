from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from backend.database.database import get_db, init_db
from backend.database.models.schema import BenchmarkRun, TestResult
from backend.runner.executor import run_benchmark

app = FastAPI(title="AI Security Sandbox API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    init_db()

class TestCase(BaseModel):
    test_id: str
    name: Optional[str] = ""
    category: Optional[str] = ""
    prompt: str
    expected_behavior: Optional[str] = ""

class RunRequest(BaseModel):
    provider: str
    model_name: str
    test_cases: List[TestCase]
    mock: Optional[bool] = True

@app.get("/")
def health_check():
    return {"status": "online", "system": "AI Security Sandbox API"}

@app.post("/api/benchmark/run")
def start_benchmark(payload: RunRequest):
    tests = [tc.dict() for tc in payload.test_cases]
    result = run_benchmark(
        provider=payload.provider,
        model_name=payload.model_name,
        test_cases=tests,
        mock=payload.mock
    )
    return result

@app.get("/api/benchmark/runs")
def list_runs(db: Session = Depends(get_db)):
    runs = db.query(BenchmarkRun).order_by(BenchmarkRun.id.desc()).all()
    return [
        {
            "id": r.id,
            "provider": r.provider,
            "model_name": r.model_name,
            "created_at": r.created_at,
            "total_results": len(r.results)
        }
        for r in runs
    ]

@app.get("/api/benchmark/runs/{run_id}")
def get_run_details(run_id: int, db: Session = Depends(get_db)):
    run = db.query(BenchmarkRun).filter(BenchmarkRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run ID not found")
    
    return {
        "id": run.id,
        "provider": run.provider,
        "model_name": run.model_name,
        "created_at": run.created_at,
        "results": [
            {
                "id": res.id,
                "test_id": res.test_id,
                "test_name": res.test_name,
                "category": res.category,
                "prompt": res.prompt,
                "response_text": res.response_text,
                "is_jailbroken": res.is_jailbroken,
                "risk_score": res.risk_score,
                "executed_at": res.executed_at
            }
            for res in run.results
        ]
    }
