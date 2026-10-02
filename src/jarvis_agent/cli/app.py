from __future__ import annotations
import asyncio
import typer
from rich.console import Console
from rich.panel import Panel
from ..configuration import load_config, setup_interactive

app = typer.Typer(no_args_is_help=False, add_completion=False)
console = Console()

def get_config():
    cfg = load_config()
    if not cfg or not cfg.configured: cfg = setup_interactive(cfg)
    return cfg

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand: return
    cfg = get_config()
    from ..agent.runtime import Runtime
    runtime = Runtime(cfg)
    console.print(Panel("[bold]JARVIS[/bold]\nTerminal-first AI agent\nTelegram is an optional remote channel."))
    while True:
        try: text = typer.prompt("JARVIS", prompt_suffix="> ", default="", show_default=False)
        except (EOFError, KeyboardInterrupt): break
        if text.strip().lower() in {"exit", "quit"}: break
        if not text.strip(): continue
        try: console.print(asyncio.run(runtime.handle("cli", text)))
        except Exception as exc: console.print(f"[red]Error:[/red] {exc}")

@app.command()
def setup(): setup_interactive(load_config())

@app.command()
def status():
    cfg = load_config()
    if not cfg:
        console.print("Not configured. Run: jarvis setup")
        return
    console.print({"provider": cfg.provider, "endpoint": cfg.base_url, "model": cfg.model, "telegram_configured": bool(cfg.telegram_bot_token), "api_key": "configured" if cfg.api_key else "missing"})

if __name__ == "__main__": app()
