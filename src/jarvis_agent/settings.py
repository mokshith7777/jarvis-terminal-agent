import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
def _ids(value): return {int(x.strip()) for x in value.split(',') if x.strip()}
@dataclass(frozen=True)
class Settings:
    telegram_bot_token:str; allowed_user_ids:set[int]; dry_run:bool; db_path:str; audit_log:str; llm_base_url:str|None; llm_api_key:str|None; llm_model:str|None; ssh_config:str
    @classmethod
    def from_env(cls):
        token=os.getenv('TELEGRAM_BOT_TOKEN','')
        if not token: raise RuntimeError('TELEGRAM_BOT_TOKEN is required')
        return cls(token,_ids(os.getenv('TELEGRAM_ALLOWED_USER_IDS','')),os.getenv('JARVIS_DRY_RUN','true').lower()=='true',os.getenv('JARVIS_DB_PATH','data/jarvis.db'),os.getenv('JARVIS_AUDIT_LOG','data/audit.jsonl'),os.getenv('JARVIS_LLM_BASE_URL') or None,os.getenv('JARVIS_LLM_API_KEY') or None,os.getenv('JARVIS_LLM_MODEL') or None,os.getenv('JARVIS_SSH_CONFIG','config/ssh.json'))
