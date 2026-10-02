from __future__ import annotations
import platform
import subprocess
from pathlib import Path
from ..security.policy import validate_argv

class LocalTools:
    def __init__(self, dry_run: bool, workspace: str):
        self.dry_run = dry_run
        self.workspace = Path(workspace).expanduser().resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def status(self):
        return {"platform": platform.platform(), "python": platform.python_version(), "workspace": str(self.workspace), "dry_run": self.dry_run}

    def doctor(self):
        checks = {}
        for command in ["git", "python3", "ssh"]:
            try:
                subprocess.run([command, "--version"], capture_output=True, timeout=5, check=False)
                checks[command] = True
            except (OSError, subprocess.SubprocessError):
                checks[command] = False
        return {"ok": all(checks.values()), "checks": checks}

    def exec(self, argv):
        argv = validate_argv(argv)
        if self.dry_run:
            return {"dry_run": True, "argv": argv}
        p = subprocess.run(argv, cwd=self.workspace, capture_output=True, text=True, timeout=60, shell=False, check=False)
        return {"returncode": p.returncode, "stdout": p.stdout[-6000:], "stderr": p.stderr[-3000:]}
