# HTTP request handling

import requests
import json
from typing import Optional, Dict, Any, Union
from urllib.parse import urlparse


class Response:
    # Wrapper around requests.Response with extra features
    
    def __init__(self, requests_response: requests.Response):
        self._response = requests_response
    
    @property
    def status_code(self) -> int:
        return self._response.status_code
    
    @property
    def headers(self) -> Dict[str, str]:
        return dict(self._response.headers)
    
    @property
    def text(self) -> str:
        return self._response.text
    
    @property
    def content(self) -> bytes:
        return self._response.content
    
    @property
    def url(self) -> str:
        return self._response.url
    
    @property
    def encoding(self) -> Optional[str]:
        return self._response.encoding
    
    @property
    def elapsed_ms(self) -> float:
        return self._response.elapsed.total_seconds() * 1000
    
    @property
    def ok(self) -> bool:
        return self._response.ok
    
    def json(self) -> Any:
        try:
            return self._response.json()
        except json.JSONDecodeError as e:
            raise ValueError(f"Response is not valid JSON: {e}")
    
    def is_json(self) -> bool:
        content_type = self.headers.get('content-type', '').lower()
        return 'application/json' in content_type or content_type.startswith('application/') and content_type.endswith('+json')
    
    def is_html(self) -> bool:
        content_type = self.headers.get('content-type', '').lower()
        return 'text/html' in content_type
    
    def is_xml(self) -> bool:
        content_type = self.headers.get('content-type', '').lower()
        return 'xml' in content_type
    
    def get_content_type(self) -> str:
        return self.headers.get('content-type', 'unknown').split(';')[0].strip()


def request(
    method: str,
    url: str,
    data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    verify: bool = True,
    allow_redirects: bool = True,
    **kwargs
) -> Response:
    
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    if method.upper() not in valid_methods:
        raise ValueError(f"Invalid HTTP method '{method}'. Must be one of: {', '.join(valid_methods)}")
    
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError(f"Invalid URL '{url}'. URL must include scheme (http:// or https://)")
    
    request_headers = headers.copy() if headers else {}
    if 'User-Agent' not in request_headers:
        from . import __version__
        request_headers['User-Agent'] = f'PostmanLite/{__version__}'
    
    if data and isinstance(data, dict):
        request_headers.setdefault('Content-Type', 'application/json')
        data = json.dumps(data)
    
    request_params = {
        'method': method.upper(),
        'url': url,
        'headers': request_headers,
        'timeout': timeout,
        'verify': verify,
        'allow_redirects': allow_redirects,
        **kwargs
    }
    
    if data is not None:
        if request_headers.get('Content-Type', '').startswith('application/json'):
            try:
                if isinstance(data, str):
                    json.loads(data)
                request_params['data'] = data
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON data: {e}")
        else:
            request_params['data'] = data
    
    try:
        response = requests.request(**request_params)
        return Response(response)
        
    except requests.exceptions.Timeout as e:
        raise TimeoutError(f"Request to {url} timed out after {timeout} seconds")
    
    except requests.exceptions.SSLError as e:
        raise Exception(f"SSL error when connecting to {url}: {e}")
    
    except requests.exceptions.TooManyRedirects as e:
        raise Exception(f"Too many redirects when accessing {url}: {e}")
    
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(f"Failed to connect to {url}: {e}")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")


def get(url: str, **kwargs) -> Response:
    return request('GET', url, **kwargs)


def post(url: str, data=None, **kwargs) -> Response:
    return request('POST', url, data=data, **kwargs)


def put(url: str, data=None, **kwargs) -> Response:
    return request('PUT', url, data=data, **kwargs)


def delete(url: str, **kwargs) -> Response:
    return request('DELETE', url, **kwargs)


def patch(url: str, data=None, **kwargs) -> Response:
    return request('PATCH', url, data=data, **kwargs)


def head(url: str, **kwargs) -> Response:
    return request('HEAD', url, **kwargs)


def options(url: str, **kwargs) -> Response:
    """Convenience method for OPTIONS requests"""
    return request('OPTIONS', url, **kwargs)
