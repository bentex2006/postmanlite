# Configuration management for saved requests and settings

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console

console = Console()


class ConfigManager:
    
    def __init__(self):
        self.config_dir = Path.home() / '.postmanlite'
        self.collections_file = self.config_dir / 'collections.json'
        self.settings_file = self.config_dir / 'settings.json'
        
        self.config_dir.mkdir(exist_ok=True)
        self._init_files()
    
    def _init_files(self):
        if not self.collections_file.exists():
            self._save_json(self.collections_file, {})
        
        if not self.settings_file.exists():
            default_settings = {
                "default_timeout": 30,
                "verify_ssl": True,
                "follow_redirects": True,
                "max_history_entries": 100,
                "auto_format_json": True,
                "show_timing": True
            }
            self._save_json(self.settings_file, default_settings)
    
    def save_request(self, name: str, method: str, url: str, 
                    headers: Optional[Dict[str, str]] = None, 
                    data: Optional[str] = None) -> None:
        collections = self._load_json(self.collections_file)
        
        request_data = {
            "method": method,
            "url": url,
            "headers": headers or {},
            "data": data,
            "created_at": self._get_timestamp()
        }
        
        collections[name] = request_data
        self._save_json(self.collections_file, collections)
    
    def load_request(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Load a saved request by name
        
        Args:
            name: Name of the saved request
            
        Returns:
            Request data or None if not found
        """
        collections = self._load_json(self.collections_file)
        return collections.get(name)
    
    def list_requests(self) -> Dict[str, Dict[str, Any]]:
        """Get all saved requests"""
        return self._load_json(self.collections_file)
    
    def delete_request(self, name: str) -> bool:
        """
        Delete a saved request
        
        Args:
            name: Name of the request to delete
            
        Returns:
            True if deleted, False if not found
        """
        collections = self._load_json(self.collections_file)
        
        if name in collections:
            del collections[name]
            self._save_json(self.collections_file, collections)
            return True
        
        return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a configuration setting"""
        settings = self._load_json(self.settings_file)
        return settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a configuration setting"""
        settings = self._load_json(self.settings_file)
        settings[key] = value
        self._save_json(self.settings_file, settings)
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings"""
        return self._load_json(self.settings_file)
    
    def reset_settings(self) -> None:
        """Reset settings to defaults"""
        self.settings_file.unlink(missing_ok=True)
        self._init_files()
    
    def export_collections(self, file_path: str) -> None:
        """Export collections to a file"""
        collections = self._load_json(self.collections_file)
        
        export_data = {
            "postmanlite_version": "1.0.0",
            "exported_at": self._get_timestamp(),
            "collections": collections
        }
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def import_collections(self, file_path: str, merge: bool = True) -> None:
        """
        Import collections from a file
        
        Args:
            file_path: Path to the import file
            merge: If True, merge with existing collections. If False, replace.
        """
        try:
            with open(file_path, 'r') as f:
                import_data = json.load(f)
            
            imported_collections = import_data.get('collections', {})
            
            if merge:
                existing_collections = self._load_json(self.collections_file)
                existing_collections.update(imported_collections)
                self._save_json(self.collections_file, existing_collections)
            else:
                self._save_json(self.collections_file, imported_collections)
                
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to import collections: {e}")
    
    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Save JSON data to file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving to {file_path}: {e}[/red]")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as ISO string"""
        from datetime import datetime
        return datetime.now().isoformat()
