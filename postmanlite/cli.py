# Command line interface

import sys
import json
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from .core import request
from .formatter import format_response
from .history import HistoryManager
from .config import ConfigManager

console = Console()

@click.command()
@click.argument('url', required=False)
@click.option('-X', '--method', default='GET', 
              type=click.Choice(['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'], case_sensitive=False),
              help='HTTP method to use')
@click.option('-d', '--data', help='Request body data (JSON string or @filename)')
@click.option('-H', '--header', 'headers', multiple=True, 
              help='Custom headers in format "Key: Value" (can be used multiple times)')
@click.option('-t', '--timeout', default=30, type=int, help='Request timeout in seconds')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output with request details')
@click.option('--json', 'force_json', is_flag=True, help='Force JSON content-type header')
@click.option('--save', help='Save request to collection with given name')
@click.option('--load', help='Load and execute saved request from collection')
@click.option('--history', is_flag=True, help='Show request history')
@click.option('--examples', is_flag=True, help='Show usage examples')
@click.option('--version', is_flag=True, help='Show version information')
@click.option('--no-verify', is_flag=True, help='Disable SSL certificate verification')
@click.option('--follow-redirects/--no-follow-redirects', default=True, 
              help='Follow HTTP redirects')
def main(url, method, data, headers, timeout, verbose, force_json, save, load, 
         history, examples, version, no_verify, follow_redirects):
    """PostmanLite - Terminal HTTP client with beautiful output
    
    A simple command-line tool for making HTTP requests.
    
    Examples:
      postmanlite https://api.github.com/users/octocat
      postmanlite -X POST https://httpbin.org/post -d '{"key": "value"}'
      postmanlite https://api.example.com -H "Authorization: Bearer token"
    """
    
    if version:
        show_version()
        return
    
    if examples:
        show_examples()
        return
    
    if history:
        show_history()
        return
    
    if load:
        load_and_execute_request(load)
        return
    
    if not url:
        console.print("[red]Error: URL is required[/red]")
        console.print("Use --help for usage information")
        sys.exit(1)
    
    # Parse headers
    parsed_headers = {}
    for header in headers:
        if ':' in header:
            key, value = header.split(':', 1)
            parsed_headers[key.strip()] = value.strip()
        else:
            console.print(f"[yellow]Warning: Invalid header format '{header}', skipping[/yellow]")
    
    # Handle JSON content type
    if force_json:
        parsed_headers['Content-Type'] = 'application/json'
    
    # Parse data
    request_data = None
    if data:
        if data.startswith('@'):
            # Read from file
            filename = data[1:]
            try:
                with open(filename, 'r') as f:
                    request_data = f.read()
            except FileNotFoundError:
                console.print(f"[red]Error: File '{filename}' not found[/red]")
                sys.exit(1)
            except Exception as e:
                console.print(f"[red]Error reading file '{filename}': {e}[/red]")
                sys.exit(1)
        else:
            request_data = data
    
    # Validate JSON if content-type is JSON
    if (request_data and 
        parsed_headers.get('Content-Type', '').startswith('application/json')):
        try:
            json.loads(request_data)
        except json.JSONDecodeError as e:
            console.print(f"[red]Error: Invalid JSON data: {e}[/red]")
            sys.exit(1)
    
    try:
        # Make the request
        response = request(
            method=method.upper(),
            url=url,
            data=request_data,
            headers=parsed_headers,
            timeout=timeout,
            verify=not no_verify,
            allow_redirects=follow_redirects
        )
        
        # Format and display response
        format_response(response, verbose=verbose)
        
        # Save to history
        history_manager = HistoryManager()
        history_manager.add_request(method.upper(), url, parsed_headers, request_data, response)
        
        # Save to collection if requested
        if save:
            config_manager = ConfigManager()
            config_manager.save_request(save, method.upper(), url, parsed_headers, request_data)
            console.print(f"[green]Request saved as '{save}'[/green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Request cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

def show_version():
    from . import __version__, __author__
    
    version_text = Text()
    version_text.append("PostmanLite ", style="bold blue")
    version_text.append(f"v{__version__}", style="bold green")
    version_text.append(f"\nBy {__author__}", style="dim")
    version_text.append("\n\nLightweight HTTP client for terminal", style="italic")
    
    panel = Panel(
        version_text,
        title="[bold blue]Version[/bold blue]",
        border_style="blue"
    )
    
    console.print(panel)

def show_examples():
    examples = [
        ("Simple GET request", "postmanlite https://api.github.com/users/octocat"),
        ("POST with JSON data", "postmanlite -X POST https://httpbin.org/post -d '{\"name\": \"John\", \"age\": 30}'"),
        ("GET with custom headers", "postmanlite https://api.example.com -H \"Authorization: Bearer your-token\""),
        ("POST with file data", "postmanlite -X POST https://httpbin.org/post -d @data.json"),
        ("PUT with multiple headers", "postmanlite -X PUT https://api.example.com/users/1 -H \"Content-Type: application/json\" -H \"X-API-Key: key123\" -d '{\"name\": \"Updated\"}'"),
        ("DELETE with verbose output", "postmanlite -X DELETE https://api.example.com/users/1 -v"),
        ("Save request to collection", "postmanlite https://api.github.com/users/octocat --save github-user"),
        ("Load saved request", "postmanlite --load github-user"),
        ("View request history", "postmanlite --history"),
    ]
    
    table = Table(title="PostmanLite Usage Examples", show_header=True, header_style="bold magenta")
    table.add_column("Description", style="cyan", width=25)
    table.add_column("Command", style="green")
    
    for description, command in examples:
        table.add_row(description, command)
    
    console.print(table)
    
    # Additional tips
    tips_text = Text()
    tips_text.append("Tips:\n", style="bold yellow")
    tips_text.append("• Use -v or --verbose for detailed request/response information\n", style="white")
    tips_text.append("• Save frequently used requests with --save <name>\n", style="white")
    tips_text.append("• Load saved requests with --load <name>\n", style="white")
    tips_text.append("• Use @ prefix to read data from files: -d @data.json\n", style="white")
    tips_text.append("• Multiple headers: -H \"Header1: Value1\" -H \"Header2: Value2\"\n", style="white")
    
    tips_panel = Panel(
        tips_text,
        title="[bold yellow]Usage Tips[/bold yellow]",
        border_style="yellow"
    )
    
    console.print("\n")
    console.print(tips_panel)

def show_history():
    """Show request history"""
    history_manager = HistoryManager()
    history = history_manager.get_history()
    
    if not history:
        console.print("[yellow]No requests in history[/yellow]")
        return
    
    table = Table(title="Request History", show_header=True, header_style="bold magenta")
    table.add_column("Time", style="cyan", width=20)
    table.add_column("Method", style="green", width=8)
    table.add_column("URL", style="blue")
    table.add_column("Status", style="yellow", width=8)
    
    for entry in history[-20:]:  # Show last 20 entries
        status_style = "green" if entry['status_code'] < 400 else "red"
        table.add_row(
            entry['timestamp'],
            entry['method'],
            entry['url'][:60] + "..." if len(entry['url']) > 60 else entry['url'],
            f"[{status_style}]{entry['status_code']}[/{status_style}]"
        )
    
    console.print(table)

def load_and_execute_request(name):
    """Load and execute a saved request"""
    config_manager = ConfigManager()
    saved_request = config_manager.load_request(name)
    
    if not saved_request:
        console.print(f"[red]No saved request found with name '{name}'[/red]")
        return
    
    console.print(f"[cyan]Loading saved request '{name}'...[/cyan]")
    
    try:
        response = request(
            method=saved_request['method'],
            url=saved_request['url'],
            data=saved_request.get('data'),
            headers=saved_request.get('headers', {}),
            timeout=30,
            verify=True,
            allow_redirects=True
        )
        
        format_response(response, verbose=False)
        
        # Save to history
        history_manager = HistoryManager()
        history_manager.add_request(
            saved_request['method'], 
            saved_request['url'], 
            saved_request.get('headers', {}), 
            saved_request.get('data'), 
            response
        )
        
    except Exception as e:
        console.print(f"[red]Error executing saved request: {e}[/red]")

if __name__ == '__main__':
    main()
