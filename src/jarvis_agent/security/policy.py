from __future__ import annotations
import shlex

class PolicyError(ValueError):
    pass

ALLOWED_LOCAL = {"pwd", "ls", "whoami", "uname", "df", "free", "uptime", "date", "git", "python", "python3", "pytest", "pip", "npm", "node"}
BLOCKED = {"rm", "rmdir", "mkfs", "shutdown", "reboot", "poweroff", "dd", "chmod", "chown"}

def validate_argv(argv: list[str]) -> list[str]:
    if not argv or not all(isinstance(x, str) and x for x in argv):
        raise PolicyError("argv must be a non-empty list of strings")
    if argv[0] in BLOCKED or argv[0] not in ALLOWED_LOCAL:
        raise PolicyError(f"local command '{argv[0]}' is not allowed")
    for arg in argv:
        if any(c in arg for c in [";", "&&", "||", "|", ">", "<", "`", "$("]):
            raise PolicyError("shell metacharacters are not allowed")
    return argv

def tokenize(command: str) -> list[str]:
    return validate_argv(shlex.split(command))
