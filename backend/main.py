import json
import os
from fastapi import FastAPI, HTTPException
from backend.models.model_config import ModelConfig
from backend.models.model_manager import ModelManager
from backend.runner.executor import BenchmarkExecutor
from backend.database.connection import init_db
from backend.database.repository import get_run_results
from pydantic import BaseModel
from typing import List

init_db()

app = FastAPI(title="AI Security Sandbox API", version="0.1.0")
manager = ModelManager()
executor = BenchmarkExecutor(manager)

class TestPayload(BaseModel):
    test_id: str
    category: str
    prompt: str

class RunBenchmarkRequest(BaseModel):
    alias: str
    test_cases: List[TestPayload]

@app.get("/")
def read_root():
    return {"message": "AI Security Sandbox API is running."}

@app.post("/models/register")
def register_model(alias: str, config: ModelConfig):
    manager.register_model(alias, config)
    return {"message": f"Model '{alias}' registered successfully."}

@app.post("/benchmark/run")
async def run_benchmark(request: RunBenchmarkRequest):
    try:
        results = await executor.run_suite(request.alias, request.test_cases)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/benchmark/run-preset/{alias}")
async def run_preset_benchmark(alias: str):
    suite_path = "backend/data/benchmark_suite.json"
    if not os.path.exists(suite_path):
        raise HTTPException(status_code=404, detail="Benchmark suite file not found.")
    
    with open(suite_path, "r") as f:
        test_cases = json.load(f)
    
    try:
        results = await executor.run_suite(alias, test_cases)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/benchmark/results/{run_id}")
def get_results(run_id: int):
    results = get_run_results(run_id)
    if not results:
        raise HTTPException(status_code=404, detail="Run ID not found or has no results.")
    return [
        {
            "id": r.id,
            "test_id": r.test_id,
            "category": r.category,
            "prompt": r.prompt,
            "response_text": r.response_text,
            "is_jailbroken": r.is_jailbroken,
            "risk_score": r.risk_score,
            "executed_at": r.executed_at
        }
        for r in results
    ]
