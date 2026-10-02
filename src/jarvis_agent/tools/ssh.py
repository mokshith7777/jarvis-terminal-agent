from __future__ import annotations
import json
import shlex
from pathlib import Path
import paramiko
from ..security.policy import validate_argv

class SSHTools:
    def __init__(self, config_file: str, dry_run: bool):
        self.config = json.loads(Path(config_file).read_text()) if Path(config_file).exists() else {}
        self.dry_run = dry_run

    def exec(self, host: str, argv: list[str]):
        cfg = self.config.get(host)
        if not cfg:
            raise ValueError(f"SSH host '{host}' is not configured")
        argv = validate_argv(argv)
        if argv[0] not in cfg.get("allowed_commands", []):
            raise ValueError(f"SSH command '{argv[0]}' is not allowed for {host}")
        if self.dry_run:
            return {"dry_run": True, "host": host, "argv": argv}
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(cfg["hostname"], username=cfg["username"], key_filename=str(Path(cfg["key_filename"]).expanduser()), timeout=10)
        _, stdout, stderr = client.exec_command(" ".join(shlex.quote(x) for x in argv), timeout=60)
        result = {"stdout": stdout.read().decode(errors="replace")[-6000:], "stderr": stderr.read().decode(errors="replace")[-3000:]}
        client.close()
        return result
