from typing import Dict
from backend.models.model_config import ModelConfig

class ModelManager:
    def __init__(self):
        self.configs: Dict[str, ModelConfig] = {}

    def register_model(self, alias: str, config: ModelConfig):
        self.configs[alias] = config

    async def generate_response(self, alias: str, prompt: str) -> str:
        if alias not in self.configs:
            raise ValueError(f"Model alias '{alias}' is not registered.")
        
        config = self.configs[alias]
        return f"[{config.provider}/{config.model_name}] Response for: {prompt[:40]}..."
