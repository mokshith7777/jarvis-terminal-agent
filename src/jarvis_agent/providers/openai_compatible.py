from __future__ import annotations
import json
import re
import httpx

class ProviderError(RuntimeError):
    pass

class OpenAICompatibleProvider:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    async def complete(self, system_prompt: str, user_text: str) -> dict:
        payload = {"model": self.model, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}], "temperature": 0, "response_format": {"type": "json_object"}}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"AI endpoint returned HTTP {exc.response.status_code}.") from exc
        except (httpx.HTTPError, KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Could not complete the AI request. Check endpoint, key, and model.") from exc
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", str(content).strip())
        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ProviderError("The configured model did not return valid JSON.") from exc
        if not isinstance(data, dict):
            raise ProviderError("The AI provider returned an invalid plan.")
        return data
