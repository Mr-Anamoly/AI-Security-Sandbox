import os
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
        provider = config.provider.lower()
        api_key = config.api_key or os.getenv(f"{provider.upper()}_API_KEY")

        # Fallback for local testing without real API keys
        if not api_key or api_key.startswith("dummy"):
            return f"[{config.provider}/{config.model_name}] Response for: {prompt}"

        # 1. OpenAI Integration
        if provider == "openai":
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=api_key)
                response = await client.chat.completions.create(
                    model=config.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=config.temperature,
                    max_tokens=config.max_tokens
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"OpenAI Error: {str(e)}"

        # 2. Anthropic (Claude) Integration
        elif provider == "anthropic":
            try:
                from anthropic import AsyncAnthropic
                client = AsyncAnthropic(api_key=api_key)
                response = await client.messages.create(
                    model=config.model_name,
                    max_tokens=config.max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                return f"Anthropic Error: {str(e)}"

        # 3. Google Gemini Integration
        elif provider in ["google", "gemini"]:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model=config.model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                return f"Gemini Error: {str(e)}"

        else:
            return f"[{config.provider}/{config.model_name}] Response for: {prompt}"
