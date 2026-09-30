from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.database.database import Base

class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    results = relationship("TestResult", back_populates="run", cascade="all, delete-orphan")

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("benchmark_runs.id"), nullable=False)
    
    test_id = Column(String(50), nullable=False)
    test_name = Column(String(150), nullable=True)
    category = Column(String(100), nullable=True)
    
    prompt = Column(Text, nullable=False)
    expected_behavior = Column(Text, nullable=True)
    
    response_text = Column(Text, nullable=True)
    is_jailbroken = Column(Boolean, default=False)
    risk_score = Column(Float, default=0.0)
    
    executed_at = Column(DateTime, default=datetime.utcnow)

    run = relationship("BenchmarkRun", back_populates="results")
