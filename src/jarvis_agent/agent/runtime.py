from __future__ import annotations
import json
from .planner import Planner
from ..providers.openai_compatible import OpenAICompatibleProvider, ProviderError
from ..security.audit import Audit
from ..tools.local import LocalTools
from ..tools.ssh import SSHTools
from ..storage.contacts import Contacts

class Runtime:
    def __init__(self, config):
        self.config = config
        self.provider = OpenAICompatibleProvider(config.base_url, config.api_key, config.model)
        self.planner = Planner(self.provider)
        self.local = LocalTools(config.dry_run, workspace=config.workspace)
        self.ssh = SSHTools(config.ssh_config, config.dry_run)
        self.audit = Audit()
        self.contacts = Contacts(str(__import__("pathlib").Path(config.workspace) / ".jarvis" / "contacts.db"))

    async def handle(self, user_id: str | int, text: str) -> str:
        try: plan = await self.planner.plan(text)
        except ProviderError: plan = self.planner.fallback(text)
        action, args = plan.get("action"), plan.get("args", {})
        self.audit.log(user_id=str(user_id), action=action)
        if action == "status": result = self.local.status()
        elif action == "doctor": result = self.local.doctor()
        elif action == "local_exec": result = self.local.exec(args["argv"])
        elif action == "ssh_exec": result = self.ssh.exec(args["host"], args["argv"])
        elif action == "contact_lookup":
            row = self.contacts.find(int(user_id), args["name"])
            result = {"name": row[0], "phone": row[1]} if row else {"found": False}
        elif action == "clarify": return "❓ " + args.get("question", "Please clarify the request.")
        else: return "⛔ Unsupported or unsafe action."
        return self.format_result(result)

    @staticmethod
    def format_result(result):
        if isinstance(result, str): return result
        return "```json\n" + json.dumps(result, indent=2, ensure_ascii=False) + "\n```"
