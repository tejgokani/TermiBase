# TermiBase 🚀

A terminal-native database learning playground that lets you run SQL queries and observe how they're parsed, planned, and executed—all from your command line.

**Install in one command:** `pip install termibase`  
**Use immediately:** Just type `termibase` and start querying!

## 🎯 What is TermiBase?

TermiBase is an educational tool designed to help developers understand database internals by providing:
- **Interactive SQL REPL** with real-time query analysis
- **Execution plan visualization** showing how queries are processed step-by-step
- **Query optimization suggestions** to learn best practices
- **Beautiful terminal UI** using Rich for a modern CLI experience
- **No browser required** - everything runs in your terminal

## 🚀 Quick Start

### One-Command Installation

```bash
pip install termibase
```

That's it! Now you can use TermiBase:

```bash
termibase          # Launch interactive REPL (Gemini-like experience)
termibase init     # Initialize database (auto-runs on first launch)
termibase --help   # See all commands
```

### Alternative Installation Methods

**Using pip3:**
```bash
pip3 install termibase
```

**Using python3 -m pip:**
```bash
python3 -m pip install termibase
```

**Using pipx (recommended for CLI tools):**
```bash
pipx install termibase
```

**For development (clone repo):**
```bash
git clone https://github.com/yourusername/termibase.git
cd termibase
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**Note:** On macOS with Homebrew Python, you may need to use a virtual environment or `pipx` to avoid externally-managed environment errors.

### First Steps

```bash
# Initialize a sandbox database
termibase init

# Launch interactive SQL REPL
termibase repl

# Or run a query directly
termibase run "SELECT * FROM users WHERE age > 25"

# See execution plan without running
termibase explain "SELECT * FROM users JOIN orders ON users.id = orders.user_id"

# Run educational demos
termibase demo
```

## 📖 Usage

### Interactive REPL

The REPL provides a full-featured SQL shell with built-in commands:

```bash
termibase repl
```

**REPL Commands:**
- `.help` - Show help
- `.explain` - Toggle execution plan display
- `.tables` - List all tables
- `.schema` - Show table schemas
- `.exit` or `.quit` - Exit REPL

**Example Session:**
```sql
termibase> SELECT * FROM users WHERE age > 28

Query Analysis
┌─────────────┬─────────────────────────────┐
│ Property    │ Value                       │
├─────────────┼─────────────────────────────┤
│ Query Type  │ SELECT                      │
│ Tables      │ users                       │
│ WHERE       │ age > 28                     │
└─────────────┴─────────────────────────────┘

Execution Plan
Query Execution
├── [1] TABLE_SCAN - Scanning table users (cost: 1.00, rows: 8)
├── [2] FILTER - Applying WHERE filter: age > 28 (cost: 0.30, rows: 30)
└── [3] PROJECT - Projecting all columns (cost: 0.20, rows: 20)

Query Results
┌──────┬─────────┬─────┬──────────────┐
│ id   │ name    │ age │ city         │
├──────┼─────────┼─────┼──────────────┤
│ 2    │ Bob     │ 30  │ San Francisco│
│ 3    │ Charlie │ 35  │ New York     │
│ 5    │ Eve     │ 32  │ San Francisco│
│ 8    │ Henry   │ 31  │ Boston       │
└──────┴─────────┴─────┴──────────────┘
```

### Command Reference

#### `termibase init`
Initialize a new TermiBase sandbox database with demo data.

```bash
termibase init
termibase init --db-path ./my-db.db
```

#### `termibase repl`
Launch an interactive SQL REPL with query visualization.

```bash
termibase repl
termibase repl --explain  # Always show execution plans
```

#### `termibase run`
Execute a single query with full visualization.

```bash
termibase run "SELECT * FROM users"
termibase run "SELECT * FROM users" --no-explain  # Skip execution plan
```

#### `termibase explain`
Show execution plan for a query without running it.

```bash
termibase explain "SELECT * FROM users WHERE city = 'New York'"
```

#### `termibase demo`
Run educational demo queries.

```bash
termibase demo              # Run all demos
termibase demo basics       # Run specific demo
termibase demo joins        # Run joins demo
```

## 🏗️ Architecture

TermiBase is built with a modular architecture:

```
termibase/
├── cli/          # Command-line interface (Typer)
├── parser/       # SQL parsing and analysis
├── engine/       # Query execution simulation
├── visualizer/   # Rich-based terminal rendering
├── storage/      # SQLite wrapper
└── demos/        # Educational examples
```

### Key Components

- **CLI Interface**: Handles commands, flags, and REPL loop
- **SQL Parser**: Parses SQL into tokens and AST using `sqlparse`
- **Query Analyzer**: Identifies query type, tables, indexes, joins
- **Execution Simulator**: Simulates logical execution steps
- **Storage Engine**: SQLite wrapper for actual query execution
- **Visualizer**: Renders execution plans and results using Rich

## 📚 Educational Features

### Query Analysis
Every query is analyzed to show:
- Query type (SELECT, INSERT, UPDATE, DELETE)
- Tables involved
- Columns selected
- WHERE conditions
- JOIN operations
- GROUP BY and ORDER BY clauses
- LIMIT values

### Execution Visualization
See how your query is executed:
- **Table scans** vs **index scans**
- **Filter operations** for WHERE clauses
- **Join strategies** (INNER, LEFT, etc.)
- **Sorting** for ORDER BY
- **Grouping** for GROUP BY
- **Cost estimates** for each step

### Optimization Suggestions
Get tips on improving your queries:
- Index recommendations
- Full table scan warnings
- Large result set alerts
- Join optimization hints

## 🎓 Demo Data

TermiBase comes with pre-loaded demo data:

**Users Table:**
- id, name, age, city

**Orders Table:**
- id, user_id, amount, date

**Indexes:**
- `idx_users_city` on `users(city)`
- `idx_orders_user_id` on `orders(user_id)`

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/termibase.git
cd termibase

# Install in editable mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest termibase/tests/
```

### Project Structure

```
TermiBase/
├── termibase/
│   ├── cli/
│   │   └── main.py          # CLI commands
│   ├── parser/
│   │   └── analyzer.py      # SQL analysis
│   ├── engine/
│   │   └── simulator.py     # Execution simulation
│   ├── visualizer/
│   │   └── renderer.py      # Rich rendering
│   ├── storage/
│   │   └── engine.py        # SQLite wrapper
│   ├── demos/
│   │   └── data.py          # Demo data
│   └── tests/               # Test suite
├── pyproject.toml           # Package config
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🎨 Design Philosophy

- **Terminal-first**: Everything works in the terminal, no browser needed
- **Educational**: Transparent about how queries are processed
- **Fast feedback**: Immediate visualization of query execution
- **Developer-centric**: Built for developers learning databases
- **Opinionated**: Provides clear suggestions and best practices

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - Modern CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [sqlparse](https://github.com/andialbrecht/sqlparse) - SQL parsing
- [SQLite](https://www.sqlite.org/) - Embedded database

---

**Happy Learning!** 🎉

