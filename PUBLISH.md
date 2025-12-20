# 📦 Publishing TermiBase to PyPI

## Prerequisites

1. Create accounts:
   - PyPI: https://pypi.org/account/register/
   - TestPyPI: https://test.pypi.org/account/register/

2. Install build tools:
```bash
pip install build twine
```

## Build Package

```bash
python -m build
```

This creates `dist/` directory with:
- `termibase-0.1.0.tar.gz` (source distribution)
- `termibase-0.1.0-py3-none-any.whl` (wheel)

## Test on TestPyPI First

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ termibase
```

## Publish to PyPI

```bash
# Upload to real PyPI
twine upload dist/*
```

## Verify Installation

After publishing, anyone can install with:

```bash
pip install termibase
```

## Update Version

Before publishing a new version:

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.1.1"
   ```

2. Update version in `termibase/__init__.py`:
   ```python
   __version__ = "0.1.1"
   ```

3. Build and upload:
   ```bash
   python -m build
   twine upload dist/*
   ```

## GitHub Release

After publishing to PyPI:

1. Create a git tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. Create a GitHub release with release notes

