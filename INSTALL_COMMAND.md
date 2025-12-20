# 🎯 One-Command Installation

## For Users (Simple Install)

Copy and paste this command in your terminal:

```bash
pip install termibase
```

That's it! Now use TermiBase:

```bash
termibase
```

## Alternative Commands (if pip doesn't work)

**macOS/Linux:**
```bash
pip3 install termibase
# or
python3 -m pip install termibase
```

**Windows:**
```bash
py -m pip install termibase
```

**Using pipx (recommended for CLI tools):**
```bash
pipx install termibase
```

## After Installation

Just run:
```bash
termibase
```

This launches an interactive SQL REPL (like Gemini in terminal) where you can:
- Type SQL queries and see them executed
- Learn how queries are parsed and planned
- See execution steps with visualizations
- Get optimization suggestions

## Quick Example

```bash
$ termibase
✨ TermiBase - Your Database Learning Playground

termibase> SELECT * FROM users LIMIT 3;
[Query results displayed with beautiful formatting]

termibase> .help
[Shows all available commands]

termibase> .exit
Goodbye!
```

## Need Help?

- Run `termibase --help` for all commands
- See `QUICKSTART.md` for examples
- See `README.md` for full documentation

