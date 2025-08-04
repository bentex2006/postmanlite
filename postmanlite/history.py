# Request history management

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console

from .core import Response

console = Console()


class HistoryManager:
    
    def __init__(self):
        self.config_dir = Path.home() / '.postmanlite'
        self.history_file = self.config_dir / 'history.json'
        self.max_entries = 100
        
        self.config_dir.mkdir(exist_ok=True)
        
        if not self.history_file.exists():
            self._save_history([])
    
    def add_request(self, method: str, url: str, headers: Dict[str, str], 
                   data: Optional[str], response: Response) -> None:
        history = self.get_history()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "url": url,
            "headers": headers,
            "data": data,
            "status_code": response.status_code,
            "response_time_ms": response.elapsed_ms,
            "response_size": len(response.content),
            "content_type": response.get_content_type()
        }
        
        # Add to beginning of history
        history.insert(0, entry)
        
        # Limit history size
        if len(history) > self.max_entries:
            history = history[:self.max_entries]
        
        # Save updated history
        self._save_history(history)
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get request history
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of history entries
        """
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
            
            if limit:
                history = history[:limit]
            
            return history
            
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def clear_history(self) -> None:
        """Clear all history"""
        self._save_history([])
    
    def delete_entry(self, index: int) -> bool:
        """
        Delete a specific history entry
        
        Args:
            index: Index of the entry to delete
            
        Returns:
            True if deleted, False if index out of range
        """
        history = self.get_history()
        
        if 0 <= index < len(history):
            del history[index]
            self._save_history(history)
            return True
        
        return False
    
    def search_history(self, query: str) -> List[Dict[str, Any]]:
        """
        Search history by URL, method, or status code
        
        Args:
            query: Search query
            
        Returns:
            List of matching history entries
        """
        history = self.get_history()
        query_lower = query.lower()
        
        matches = []
        for entry in history:
            if (query_lower in entry['url'].lower() or
                query_lower in entry['method'].lower() or
                query == str(entry['status_code'])):
                matches.append(entry)
        
        return matches
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about request history"""
        history = self.get_history()
        
        if not history:
            return {
                "total_requests": 0,
                "success_rate": 0,
                "avg_response_time": 0,
                "methods": {},
                "status_codes": {}
            }
        
        total_requests = len(history)
        successful_requests = sum(1 for entry in history if entry['status_code'] < 400)
        success_rate = (successful_requests / total_requests) * 100
        
        total_response_time = sum(entry['response_time_ms'] for entry in history)
        avg_response_time = total_response_time / total_requests
        
        # Count methods
        methods = {}
        for entry in history:
            method = entry['method']
            methods[method] = methods.get(method, 0) + 1
        
        # Count status codes
        status_codes = {}
        for entry in history:
            status = str(entry['status_code'])
            status_codes[status] = status_codes.get(status, 0) + 1
        
        return {
            "total_requests": total_requests,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "methods": methods,
            "status_codes": status_codes
        }
    
    def export_history(self, file_path: str, format: str = 'json') -> None:
        """
        Export history to a file
        
        Args:
            file_path: Output file path
            format: Export format ('json' or 'csv')
        """
        history = self.get_history()
        
        if format.lower() == 'json':
            export_data = {
                "postmanlite_version": "1.0.0",
                "exported_at": datetime.now().isoformat(),
                "history": history
            }
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
                
        elif format.lower() == 'csv':
            import csv
            
            with open(file_path, 'w', newline='') as f:
                if history:
                    writer = csv.DictWriter(f, fieldnames=history[0].keys())
                    writer.writeheader()
                    writer.writerows(history)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """Save history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving history: {e}[/red]")
