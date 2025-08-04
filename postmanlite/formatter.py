# Response formatting and display utilities

import json
import xml.dom.minidom
from typing import Any, Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich.tree import Tree

from .core import Response

console = Console()


def format_response(response: Response, verbose: bool = False) -> None:
    
    if verbose:
        show_request_summary(response)
    
    show_response_status(response)
    
    if verbose or not response.ok:
        show_response_headers(response)
    
    show_response_body(response)
    show_timing_info(response)


def show_request_summary(response: Response) -> None:
    request_info = Text()
    request_info.append("→ ", style="bold blue")
    request_info.append(f"Request sent to: ", style="white")
    request_info.append(response.url, style="cyan")
    
    console.print(request_info)
    console.print()


def show_response_status(response: Response) -> None:
    status_color = get_status_color(response.status_code)
    
    status_text = Text()
    status_text.append("HTTP Status: ", style="bold white")
    status_text.append(f"{response.status_code}", style=f"bold {status_color}")
    
    status_descriptions = {
        200: "OK",
        201: "Created",
        202: "Accepted",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        422: "Unprocessable Entity",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout"
    }
    
    if response.status_code in status_descriptions:
        status_text.append(f" ({status_descriptions[response.status_code]})", style=f"{status_color}")
    
    panel = Panel(
        status_text,
        title="[bold white]Response Status[/bold white]",
        border_style=status_color,
        padding=(0, 1)
    )
    
    console.print(panel)


def show_response_headers(response: Response) -> None:
    if not response.headers:
        return
    
    table = Table(title="Response Headers", show_header=True, header_style="bold magenta")
    table.add_column("Header", style="cyan", width=25)
    table.add_column("Value", style="white")
    
    sorted_headers = sorted(response.headers.items())
    
    for header, value in sorted_headers:
        display_value = value[:100] + "..." if len(value) > 100 else value
        table.add_row(header, display_value)
    
    console.print(table)
    console.print()


def show_response_body(response: Response) -> None:
    """Show formatted response body based on content type"""
    if not response.text.strip():
        console.print("[dim]Empty response body[/dim]")
        return
    
    content_type = response.get_content_type().lower()
    
    if response.is_json():
        show_json_response(response)
    elif response.is_xml():
        show_xml_response(response)
    elif response.is_html():
        show_html_response(response)
    else:
        show_text_response(response)


def show_json_response(response: Response) -> None:
    """Format and display JSON response"""
    try:
        json_data = response.json()
        formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)
        
        syntax = Syntax(
            formatted_json,
            "json",
            theme="monokai",
            line_numbers=True,
            word_wrap=True
        )
        
        panel = Panel(
            syntax,
            title="[bold green]JSON Response[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        
        console.print(panel)
        
        # Show JSON statistics
        show_json_stats(json_data)
        
    except ValueError as e:
        # Fallback to plain text if JSON parsing fails
        console.print(f"[yellow]Warning: Failed to parse JSON: {e}[/yellow]")
        show_text_response(response)


def show_xml_response(response: Response) -> None:
    """Format and display XML response"""
    try:
        # Pretty print XML
        dom = xml.dom.minidom.parseString(response.text)
        formatted_xml = dom.toprettyxml(indent="  ")
        
        # Remove empty lines
        lines = [line for line in formatted_xml.split('\n') if line.strip()]
        formatted_xml = '\n'.join(lines)
        
        syntax = Syntax(
            formatted_xml,
            "xml",
            theme="monokai",
            line_numbers=True,
            word_wrap=True
        )
        
        panel = Panel(
            syntax,
            title="[bold blue]XML Response[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        
        console.print(panel)
        
    except Exception:
        # Fallback to plain text if XML parsing fails
        show_text_response(response)


def show_html_response(response: Response) -> None:
    """Format and display HTML response"""
    # For HTML, show a preview and basic stats
    lines = response.text.split('\n')
    preview_lines = lines[:10]  # Show first 10 lines
    
    preview_text = '\n'.join(preview_lines)
    if len(lines) > 10:
        preview_text += f"\n... ({len(lines) - 10} more lines)"
    
    syntax = Syntax(
        preview_text,
        "html",
        theme="monokai",
        line_numbers=True,
        word_wrap=True
    )
    
    panel = Panel(
        syntax,
        title=f"[bold magenta]HTML Response Preview[/bold magenta] ({len(lines)} lines, {len(response.text)} chars)",
        border_style="magenta",
        padding=(1, 2)
    )
    
    console.print(panel)


def show_text_response(response: Response) -> None:
    """Show plain text response"""
    content = response.text
    
    # Detect if content might be code and apply syntax highlighting
    content_type = response.get_content_type().lower()
    lexer = None
    
    if 'javascript' in content_type or content_type.endswith('js'):
        lexer = "javascript"
    elif 'css' in content_type:
        lexer = "css"
    elif 'yaml' in content_type or 'yml' in content_type:
        lexer = "yaml"
    elif content_type.endswith('csv'):
        lexer = "csv"
    
    if lexer and len(content) < 5000:  # Only highlight smaller files
        try:
            syntax = Syntax(
                content,
                lexer,
                theme="monokai",
                line_numbers=True,
                word_wrap=True
            )
            
            panel = Panel(
                syntax,
                title=f"[bold cyan]Response Body ({content_type})[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            )
            
            console.print(panel)
            return
        except Exception:
            pass  # Fallback to plain text
    
    # Plain text display
    # Truncate very long responses
    if len(content) > 10000:
        content = content[:10000] + "\n... (response truncated)"
    
    panel = Panel(
        content,
        title=f"[bold white]Response Body ({content_type})[/bold white]",
        border_style="white",
        padding=(1, 2)
    )
    
    console.print(panel)


def show_json_stats(json_data: Any) -> None:
    """Show statistics about JSON response"""
    stats = Text()
    
    if isinstance(json_data, dict):
        stats.append(f"📊 Object with {len(json_data)} keys", style="dim cyan")
        if json_data:
            stats.append(f" (keys: {', '.join(list(json_data.keys())[:5])}", style="dim")
            if len(json_data) > 5:
                stats.append(f", +{len(json_data) - 5} more", style="dim")
            stats.append(")", style="dim")
    elif isinstance(json_data, list):
        stats.append(f"📋 Array with {len(json_data)} items", style="dim cyan")
    else:
        stats.append(f"📄 {type(json_data).__name__} value", style="dim cyan")
    
    console.print(stats)
    console.print()


def show_timing_info(response: Response) -> None:
    """Show request timing information"""
    timing_text = Text()
    timing_text.append("⏱️ ", style="yellow")
    timing_text.append("Response time: ", style="white")
    
    elapsed_ms = response.elapsed_ms
    if elapsed_ms < 100:
        timing_text.append(f"{elapsed_ms:.1f}ms", style="green")
    elif elapsed_ms < 1000:
        timing_text.append(f"{elapsed_ms:.1f}ms", style="yellow")
    else:
        timing_text.append(f"{elapsed_ms:.1f}ms", style="red")
    
    timing_text.append(" | ", style="dim")
    timing_text.append("Size: ", style="white")
    timing_text.append(format_bytes(len(response.content)), style="cyan")
    
    console.print(timing_text)
    console.print()


def get_status_color(status_code: int) -> str:
    """Get color for HTTP status code"""
    if status_code < 300:
        return "green"
    elif status_code < 400:
        return "yellow"
    elif status_code < 500:
        return "red"
    else:
        return "bright_red"


def format_bytes(size: int) -> str:
    """Format byte size in human readable format"""
    float_size = float(size)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if float_size < 1024.0:
            return f"{float_size:.1f}{unit}"
        float_size /= 1024.0
    return f"{float_size:.1f}TB"
