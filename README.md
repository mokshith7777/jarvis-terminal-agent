# JARVIS Terminal Agent

Terminal-first AI agent with Telegram as a thin remote channel.

JARVIS converts natural-language intent into structured actions, validates them against explicit security policy, and executes approved local or SSH tools.

## Features
- Terminal-first local control
- Telegram polling gateway with per-user allowlist
- OpenAI-compatible AI providers
- Deterministic fallback planner
- Safe subprocess execution with shell=False
- SSH host and command allowlists
- Telegram contact storage and lookup
- Audit logging and dry-run mode
- Docker support
- GitHub Actions CI
- GitHub Pages site

## Install

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    jarvis setup
    jarvis

## Telegram

Configure the bot token and numeric Telegram user allowlist locally, then run jarvis-telegram.

## Security

Telegram is treated as an untrusted transport. Local commands use shell=False, shell metacharacters are rejected, destructive commands are blocked, and SSH hosts and commands must be explicitly configured. Never commit API keys, Telegram tokens, private keys, or config/ssh.json.

## Development

    python -m pytest

## GitHub Pages

The docs directory is deployed by .github/workflows/pages.yml.

## License

MIT.
