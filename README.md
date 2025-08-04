# PostmanLite

A lightweight CLI HTTP client built for educational purposes - bringing Postman-like functionality to your terminal. Perfect for learning API testing, exploring REST services, and quick HTTP requests without the overhead of a full desktop application.

[![PyPI version](https://badge.fury.io/py/postmanlite.svg)](https://badge.fury.io/py/postmanlite)
[![Python Support](https://img.shields.io/pypi/pyversions/postmanlite.svg)](https://pypi.org/project/postmanlite/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Beautiful Terminal Output**: Rich formatting with syntax highlighting for JSON, XML, and HTML responses
- **Educational Focus**: Learn HTTP methods, headers, and API interactions through hands-on CLI experience
- **Postman-Inspired Design**: Familiar concepts like collections and request history in a lightweight package
- **Library and CLI**: Use as a command-line tool or import into Python scripts for programmatic HTTP requests
- **Request Collections**: Save frequently used API calls and organize your testing workflow
- **Automatic History**: Track all requests with response times and status codes for learning and debugging
- **Multiple Output Modes**: Verbose mode for detailed request/response inspection
- **Cross-Platform**: Works on Windows, macOS, and Linux with Python 3.7+

## Installation

```bash
pip install postmanlite
```

## Quick Start

### CLI Usage

```bash
# Simple GET request
postmanlite https://api.github.com/users/octocat

# POST with JSON data
postmanlite -X POST https://httpbin.org/post -d '{"name": "John", "age": 30}' --json

# GET with custom headers
postmanlite https://api.example.com -H "Authorization: Bearer your-token"

# Verbose output with request details
postmanlite https://httpbin.org/get -v

# Save request to collection
postmanlite https://api.github.com/users/octocat --save github-user

# Load and execute saved request
postmanlite --load github-user

# View request history
postmanlite --history

# Show examples
postmanlite --examples
```

### Library Usage

```python
from postmanlite import request

# Simple GET request
response = request('GET', 'https://api.github.com/users/octocat')
print(f"Status: {response.status_code}")
print(f"JSON: {response.json()}")

# POST with data
response = request('POST', 'https://httpbin.org/post', 
                  data='{"key": "value"}',
                  headers={'Content-Type': 'application/json'})
print(f"Response time: {response.elapsed_ms}ms")

# Convenience methods
from postmanlite import get, post, put, delete

response = get('https://httpbin.org/get')
response = post('https://httpbin.org/post', data={'key': 'value'})
```

## Educational Focus

PostmanLite is designed as a learning tool for understanding HTTP protocols and API testing. Unlike the full Postman desktop application, this lightweight version focuses on:

- **HTTP Fundamentals**: Learn request methods, headers, status codes, and response formats
- **API Testing Basics**: Practice with real APIs using a simple command-line interface  
- **REST API Concepts**: Understand GET, POST, PUT, DELETE operations through hands-on experience
- **Request/Response Cycle**: See detailed request and response information to understand HTTP communication
- **Collection Management**: Learn to organize and reuse API calls like in professional testing workflows

Perfect for students, developers learning APIs, or anyone who wants Postman-like functionality without the complexity.

## Command Line Options

```
Usage: postmanlite [OPTIONS] [URL]

Options:
  -X, --method [GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS]
                                  HTTP method to use
  -d, --data TEXT                 Request body data (JSON string or @filename)
  -H, --header TEXT               Custom headers in format "Key: Value"
  -t, --timeout INTEGER           Request timeout in seconds
  -v, --verbose                   Verbose output with request details
  --json                          Force JSON content-type header
  --save TEXT                     Save request to collection with given name
  --load TEXT                     Load and execute saved request from collection
  --history                       Show request history
  --examples                      Show usage examples
  --version                       Show version information
  --no-verify                     Disable SSL certificate verification
  --follow-redirects / --no-follow-redirects
                                  Follow HTTP redirects
  --help                          Show this message and exit.
```

## 🎯 Advanced Examples

### Working with Files

```bash
# Send data from file
postmanlite -X POST https://httpbin.org/post -d @data.json

# Multiple headers
postmanlite https://api.example.com \
  -H "Authorization: Bearer token123" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: secret123"
```

### Request Collections

```bash
# Save frequently used requests
postmanlite https://api.github.com/user --save github-profile
postmanlite -X POST https://api.example.com/login -d @login.json --save login-request

# Execute saved requests
postmanlite --load github-profile
postmanlite --load login-request
```

### History and Statistics

```bash
# View request history
postmanlite --history

# All requests are automatically saved to history with:
# - Timestamp
# - Method and URL
# - Status code
# - Response time
# - Response size
```

## 🐍 Python Library

### Basic Usage

```python
from postmanlite import request, get, post, put, delete

# Make requests
response = get('https://httpbin.org/get')
response = post('https://httpbin.org/post', data={'key': 'value'})
response = put('https://httpbin.org/put', data='{"updated": true}')
response = delete('https://httpbin.org/delete')

# Access response properties
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.text}")
print(f"JSON: {response.json()}")
print(f"Response time: {response.elapsed_ms}ms")
print(f"Content type: {response.get_content_type()}")
```

### Advanced Usage

```python
from postmanlite import request

# Custom timeout and headers
response = request(
    method='GET',
    url='https://api.example.com/data',
    headers={
        'Authorization': 'Bearer token123',
        'User-Agent': 'MyApp/1.0'
    },
    timeout=10,
    verify=True
)

# Handle different content types
if response.is_json():
    data = response.json()
elif response.is_xml():
    xml_content = response.text
elif response.is_html():
    html_content = response.text
else:
    raw_content = response.content
```

## 🎨 Rich Output Features

PostmanLite provides beautiful terminal output with:

- **Syntax highlighting** for JSON, XML, HTML, CSS, JavaScript
- **Color-coded status codes** (green for success, red for errors)
- **Formatted headers** in easy-to-read tables
- **Response timing** and size information
- **JSON statistics** showing object keys and array lengths
- **Smart content detection** and appropriate formatting

## 📁 File Structure

Your requests and settings are stored in `~/.postmanlite/`:

```
~/.postmanlite/
├── collections.json    # Saved request collections
├── history.json       # Request history
└── settings.json      # User settings and preferences
```

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/postmanlite/postmanlite.git
cd postmanlite
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
pytest --cov=postmanlite  # With coverage
```

### Code Quality

```bash
black postmanlite/        # Format code
flake8 postmanlite/       # Lint code
mypy postmanlite/         # Type checking
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## ⭐ Support

If you find PostmanLite helpful, please consider:

- ⭐ **Starring** the repository on GitHub
- 🐛 **Reporting** bugs or requesting features
- 💬 **Sharing** it with your colleagues and friends
- ☕ **Buying us a coffee** at [ko-fi.com/postmanlite](https://ko-fi.com/postmanlite)

## 📊 Why PostmanLite?

| Feature | PostmanLite | curl | httpie | Postman Desktop |
|---------|-------------|------|--------|-----------------|
| Beautiful output | ✅ | ❌ | ✅ | ✅ |
| Lightweight | ✅ | ✅ | ✅ | ❌ |
| Python library | ✅ | ❌ | ❌ | ❌ |
| Request collections | ✅ | ❌ | ❌ | ✅ |
| History tracking | ✅ | ❌ | ❌ | ✅ |
| No GUI required | ✅ | ✅ | ✅ | ❌ |
| Cross-platform | ✅ | ✅ | ✅ | ✅ |
| Open source | ✅ | ✅ | ✅ | ❌ |

PostmanLite strikes the perfect balance between simplicity and functionality, offering the power of Postman in a lightweight, terminal-friendly package.
