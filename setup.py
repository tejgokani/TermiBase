"""Setup script for TermiBase (fallback for older pip versions)."""

from setuptools import setup, find_packages

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="termibase",
    version="0.1.0",
    author="TermiBase Contributors",
    description="A terminal-native database learning playground",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/termibase",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "sqlparse>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "termibase=termibase.cli.main:main",
        ],
    },
)

