#!/usr/bin/env python3
"""
Post-install welcome message script
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def show_welcome_message():
    """Display the PostmanLite welcome message"""
    console = Console()
    
    welcome_text = Text()
    welcome_text.append("🚀 ", style="bold green")
    welcome_text.append("PostmanLite installed successfully!", style="bold blue")
    welcome_text.append("\n\n")
    welcome_text.append("📖 Quick Start:\n", style="bold yellow")
    welcome_text.append("  postmanlite https://api.github.com/users/octocat\n", style="cyan")
    welcome_text.append("  postmanlite -X POST https://httpbin.org/post -d '{\"key\": \"value\"}'\n", style="cyan")
    welcome_text.append("\n")
    welcome_text.append("📚 Documentation:\n", style="bold yellow")
    welcome_text.append("  postmanlite --help\n", style="cyan")
    welcome_text.append("  postmanlite --examples\n", style="cyan")
    welcome_text.append("\n")
    welcome_text.append("⭐ Support us:\n", style="bold yellow")
    welcome_text.append("  Star us on GitHub: https://github.com/postmanlite/postmanlite\n", style="green")
    welcome_text.append("  Buy us a coffee: https://ko-fi.com/postmanlite\n", style="magenta")
    
    panel = Panel(
        welcome_text,
        title="[bold green]Welcome to PostmanLite[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(panel)

if __name__ == "__main__":
    show_welcome_message()