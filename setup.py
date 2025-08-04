"""
Setup script for PostmanLite
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements.txt
def read_requirements():
    requirements = []
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        # Fallback requirements if requirements.txt doesn't exist
        requirements = [
            'requests>=2.28.0',
            'click>=8.0.0',
            'rich>=12.0.0',
        ]
    return requirements

setup(
    name="postmanlite",
    version="1.0.0",
    author="BenTex2006",
    author_email="hello.b3xtopia@gmail.com",
    description="A lightweight CLI HTTP client with rich formatting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/postmanlite/postmanlite",
    project_urls={
        "Bug Tracker": "https://github.com/postmanlite/postmanlite/issues",
        "Documentation": "https://github.com/postmanlite/postmanlite#readme",
        "Source Code": "https://github.com/postmanlite/postmanlite",
        "Funding": "https://ko-fi.com/postmanlite",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "twine",
            "build",
        ],
    },
    entry_points={
        "console_scripts": [
            "postmanlite=postmanlite.cli:main",
        ],
    },
    keywords=[
        "http", "cli", "api", "testing", "requests", "postman", "curl",
        "rest", "api-client", "http-client", "command-line", "terminal"
    ],
    include_package_data=True,
    zip_safe=False,
)
