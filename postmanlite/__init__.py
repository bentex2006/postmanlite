"""
PostmanLite - Lightweight HTTP client for the command line
"""

__version__ = "1.0.0"
__author__ = "BenTex2006"
__email__ = "hello.b3xtopia@gmail.com"
__description__ = "Educational lightweight HTTP client with beautiful terminal output"

from .core import request, Response, get, post, put, delete, patch, head, options
from .cli import main

__all__ = ['request', 'Response', 'get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'main']
