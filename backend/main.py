from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from backend.models.model_config import ModelConfig
from backend.models.model_manager import ModelManager
from backend.runner.executor import BenchmarkExecutor
from backend.database.repositories.database import get_run_results

app = FastAPI(title="AI Security Sandbox API")

manager = ModelManager()
executor = BenchmarkExecutor(manager)

class RunBenchmarkRequest(BaseModel):
    alias: str
    test_cases: List[Dict[str, Any]]

@app.get("/")
def read_root():
    return {"status": "online", "system": "AI-Security-Sandbox API"}

@app.post("/models/register")
def register_model(alias: str, config: ModelConfig):
    manager.register_model(alias, config)
    return {"message": f"Model '{alias}' registered successfully."}

@app.post("/benchmark/run")
async def run_benchmark(request: RunBenchmarkRequest):
    try:
        summary = await executor.run_suite(request.alias, request.test_cases)
        return summary
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
