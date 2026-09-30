from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ModelConfig(BaseModel):
    provider: str
    model_name: str
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, gt=0)
    api_key: Optional[str] = None
    extra_params: Dict[str, Any] = {}
