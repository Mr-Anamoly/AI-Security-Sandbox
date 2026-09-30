from typing import List
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, init_db
from backend.database.models.schema import BenchmarkRun, TestResult

def create_benchmark_run(provider: str, model_name: str) -> int:
    init_db()
    session: Session = SessionLocal()
    try:
        run = BenchmarkRun(provider=provider, model_name=model_name)
        session.add(run)
        session.commit()
        session.refresh(run)
        return run.id
    finally:
        session.close()

def save_test_result(
    run_id: int,
    test_case: dict,
    response_text: str,
    is_jailbroken: bool = False,
    risk_score: float = 0.0
) -> TestResult:
    session: Session = SessionLocal()
    try:
        result = TestResult(
            run_id=run_id,
            test_id=test_case.get("test_id", "UNKNOWN"),
            test_name=test_case.get("name", ""),
            category=test_case.get("category", ""),
            prompt=test_case.get("prompt", ""),
            expected_behavior=test_case.get("expected_behavior", ""),
            response_text=response_text,
            is_jailbroken=is_jailbroken,
            risk_score=risk_score
        )
        session.add(result)
        session.commit()
        session.refresh(result)
        return result
    finally:
        session.close()

def get_run_results(run_id: int) -> List[TestResult]:
    session: Session = SessionLocal()
    try:
        return session.query(TestResult).filter(TestResult.run_id == run_id).all()
    finally:
        session.close()
