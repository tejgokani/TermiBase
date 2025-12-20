# Installation Guide

## 🚀 Quick Install (One Command)

### Option 1: Using pip (Recommended)

```bash
pip install termibase
```

Or if you need to use `pip3`:

```bash
pip3 install termibase
```

Or if pip is not in PATH:

```bash
python3 -m pip install termibase
```

### Option 2: Using Installation Script

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/termibase/main/install.sh | bash
```

Or download and run:

```bash
wget https://raw.githubusercontent.com/yourusername/termibase/main/install.sh
chmod +x install.sh
./install.sh
```

### Option 3: Using pipx (For CLI Tools)

```bash
pipx install termibase
```

## ✅ Verify Installation

After installation, verify it works:

```bash
termibase --help
```

If you see the help menu, installation was successful!

## 🎯 First Use

Simply run `termibase` to launch the interactive REPL:

```bash
termibase
```

The database will be automatically initialized on first run.

## 🔧 Troubleshooting

### Command Not Found

If `termibase` command is not found:

1. **Check if it's installed:**
   ```bash
   python3 -m pip show termibase
   ```

2. **Add to PATH (if installed with --user):**
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
   Add this to your `~/.bashrc` or `~/.zshrc` for persistence.

3. **Use Python module directly:**
   ```bash
   python3 -m termibase.cli.main
   ```

### Permission Errors

If you get permission errors, use `--user` flag:

```bash
pip install --user termibase
```

### Virtual Environment (Recommended for Development)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install termibase
```

## 📦 Requirements

- Python 3.8 or higher
- pip (Python package installer)

## 🌐 Platform Support

- ✅ macOS
- ✅ Linux
- ✅ Windows (with WSL recommended)

## 🔄 Update TermiBase

```bash
pip install --upgrade termibase
```

## 🗑️ Uninstall

```bash
pip uninstall termibase
```
