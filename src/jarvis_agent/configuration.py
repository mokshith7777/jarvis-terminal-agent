from __future__ import annotations
import json, os, stat
from dataclasses import dataclass, asdict
from getpass import getpass
from pathlib import Path

CONFIG_DIR = Path(os.getenv("JARVIS_CONFIG_DIR", Path.home() / ".config" / "jarvis"))
CONFIG_FILE = CONFIG_DIR / "config.json"

PROVIDERS = {
    "openrouter": {"name": "OpenRouter", "base_url": "https://openrouter.ai/api/v1", "model": "openai/gpt-oss-120b"},
    "openai": {"name": "OpenAI", "base_url": "https://api.openai.com/v1", "model": "gpt-5.6"},
    "groq": {"name": "Groq", "base_url": "https://api.groq.com/openai/v1", "model": "openai/gpt-oss-120b"},
}

@dataclass
class Config:
    provider: str
    base_url: str
    api_key: str
    model: str
    telegram_bot_token: str = ""
    allowed_user_ids: list[int] | None = None
    dry_run: bool = False
    workspace: str = ""
    ssh_config: str = ""

    def __post_init__(self):
        if self.allowed_user_ids is None:
            self.allowed_user_ids = []
        if not self.workspace:
            self.workspace = str(Path.cwd())
        if not self.ssh_config:
            self.ssh_config = str(CONFIG_DIR / "ssh.json")

    @property
    def configured(self):
        return bool(self.base_url and self.api_key and self.model)

def _write_secure(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass

def load_config():
    if not CONFIG_FILE.exists():
        return None
    try:
        return Config(**json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError):
        return None

def save_config(config):
    _write_secure(CONFIG_FILE, asdict(config))

def setup_interactive(existing=None):
    print("\nJARVIS setup\n")
    choices = list(PROVIDERS)
    for i, key in enumerate(choices, 1):
        print(f"{i}. {PROVIDERS[key]['name']} - {PROVIDERS[key]['base_url']}")
    print("4. Custom OpenAI-compatible endpoint")
    raw = input("Provider [1-4]: ").strip() or "1"
    if raw in {"1", "2", "3"}:
        key = choices[int(raw) - 1]
        provider = key
        base_url = PROVIDERS[key]["base_url"]
        default_model = PROVIDERS[key]["model"]
    elif raw == "4":
        provider = "custom"
        base_url = input("Endpoint base URL: ").strip().rstrip("/")
        default_model = ""
    else:
        raise ValueError("Choose 1, 2, 3, or 4")
    api_key = getpass("API key (hidden): ").strip()
    if not api_key:
        raise ValueError("An API key is required.")
    model = input(f"Model [{default_model or 'required'}]: ").strip() or default_model
    if not model:
        raise ValueError("A model is required.")
    token = existing.telegram_bot_token if existing else input("Telegram bot token (optional): ").strip()
    ids = input("Authorized Telegram user IDs (comma-separated, optional): ").strip()
    allowed = existing.allowed_user_ids if existing else []
    if ids:
        allowed = [int(x.strip()) for x in ids.split(",") if x.strip()]
    cfg = Config(provider, base_url, api_key, model, token, allowed,
                 existing.dry_run if existing else False,
                 existing.workspace if existing else str(Path.cwd()),
                 existing.ssh_config if existing else str(CONFIG_DIR / "ssh.json"))
    save_config(cfg)
    print(f"Saved securely to {CONFIG_FILE}.")
    return cfg
