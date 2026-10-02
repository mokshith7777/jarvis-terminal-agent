from __future__ import annotations
import re
from pathlib import Path
from ..providers.openai_compatible import OpenAICompatibleProvider
from ..security.policy import tokenize

class Planner:
    def __init__(self, provider: OpenAICompatibleProvider):
        self.provider = provider
        self.prompt = Path(__file__).resolve().parents[3].joinpath("config", "system_prompt.txt").read_text(encoding="utf-8")

    async def plan(self, text: str) -> dict:
        return await self.provider.complete(self.prompt, text)

    def fallback(self, text: str) -> dict:
        s = text.strip().lower()
        if s in {"status", "/status"}: return {"action": "status", "args": {}}
        if s in {"doctor", "/doctor"}: return {"action": "doctor", "args": {}}
        if "disk" in s: return {"action": "local_exec", "args": {"argv": ["df", "-h"]}}
        if s.startswith("run "): return {"action": "local_exec", "args": {"argv": tokenize(s[4:])}}
        m = re.match(r"ssh\s+([\w.-]+)\s*:\s*(.+)$", s)
        if m: return {"action": "ssh_exec", "args": {"host": m.group(1), "argv": tokenize(m.group(2))}}
        m = re.match(r"(?:show|find|lookup)\s+contact\s+(.+)$", s)
        if m: return {"action": "contact_lookup", "args": {"name": m.group(1).strip()}}
        return {"action": "clarify", "args": {"question": "I could not create a safe structured plan for that request."}}
