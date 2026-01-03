# TermiBase

A terminal-based SQL learning and exam-preparation environment designed to simulate the workflow and constraints of SQL*Plus, while adding clarity, safety, and guided understanding.

**Install:** `brew install tejgokani/termibase/termibase` or `pip install termibase`  
**Use:** `termibase`

## What TermiBase Is and Is Not

**TermiBase IS:**
- A learning tool for SQL syntax and query construction
- A practice environment for SQL*Plus-style terminal workflows
- An exam-preparation aid for Oracle SQL*Plus environments
- A safe sandbox for experimenting with SQL queries

**TermiBase IS NOT:**
- A production database client or DBA tool
- A query optimizer or performance analysis tool
- A replacement for professional database tools (psql, mysql client, etc.)
- A tool for understanding physical database internals

## Quick Start

### Installation

**macOS/Linux (Homebrew):**
```bash
brew install tejgokani/termibase/termibase
```

**Windows (pip):**
```bash
pip install termibase
python -m termibase_setup  # Adds to PATH
```

**All Platforms (pipx - Recommended):**
```bash
pipx install termibase
```

### First Use

```bash
termibase
```

The database initializes automatically. You'll see:

```
✨ TermiBase - Your Database Learning Playground

💡 Type SQL queries to see how they're executed step-by-step
   Use .help for commands, .exit to quit

termibase> 
```

## Operating Modes

TermiBase supports different modes for different learning contexts:

### Practice Mode (Default)

SQL*Plus-like minimal output. Queries execute and return results without additional analysis.

- Minimal output: query results only
- Execution plan visualization: disabled by default (toggle with `.explain`)
- Suitable for: building muscle memory, practicing SQL*Plus workflows

### Learning Mode

Enhanced output with explanations and conceptual visualizations.

- Query analysis: shows query structure and components
- Conceptual execution flow: logical visualization of query processing order
- Hints and suggestions: guidance on query construction
- Suitable for: understanding SQL syntax, learning query structure

Enable learning features:
```bash
termibase> .explain  # Toggle execution plan display
termibase> .learn    # Interactive SQL lessons
```

### Exam Simulation Mode

Strict mode that mirrors SQL*Plus behavior for exam preparation.

- No hints or suggestions
- Minimal output matching SQL*Plus defaults
- Strict error handling
- Suitable for: preparing for Oracle SQL*Plus exams

Enter via challenge environment:
```bash
termibase> .challenge
challenge> .start <id>
```

## Key Features

### 1. SQL Challenge Environment

Practice with 200 unique SQL challenges:

```bash
termibase> .challenge

🎯 Challenge Environment
💡 Type .help for available commands
💡 Type :exit to return to main REPL

challenge> .list          # List all challenges
challenge> .start 1       # Start challenge #1
challenge> .submit        # Submit your solution
challenge> .stats         # View your progress
```

**Challenge Features:**
- 50 Easy, 75 Medium, 75 Hard challenges
- Each challenge has unique problem statement and solution
- Progress tracking and scoring system
- Exam-like constraints (no DROP, ALTER operations)

### 2. Multi-Line Query Input

Write SQL queries across multiple lines (SQL*Plus style):

```sql
termibase> SELECT DISTINCT
      ->     c.customer_id,
      ->     c.first_name,
      ->     c.last_name
      -> FROM rental r
      -> INNER JOIN customer c ON r.customer_id = c.customer_id
      -> WHERE c.city = 'Lethbridge';
```

End with `;` to execute. Use `\` on empty line to cancel.

### 3. Conceptual Execution Flow Visualization

**Important:** This feature shows logical query processing order, not physical database execution.

When enabled (`.explain`), TermiBase displays a conceptual visualization of how SQL queries are logically processed:

```
Conceptual Execution Flow
├── [1] TABLE_SCAN - Scanning table users (conceptual)
├── [2] FILTER - Applying WHERE filter: age > 28 (conceptual)
└── [3] PROJECT - Projecting all columns (conceptual)
```

**This is NOT:**
- Real execution cost from the database engine
- Physical execution plan from SQLite
- Accurate row count estimates
- Performance optimization guidance

**This IS:**
- A logical representation of SQL processing order
- A teaching aid for understanding query structure
- A visualization of how SQL clauses relate to each other

See the "Accuracy & Transparency" section for details.

### 4. Interactive Learning Mode

Learn SQL interactively with guided lessons:

```bash
termibase> .learn
```

**Topics:** SELECT Basics, WHERE Clause, JOINs, GROUP BY, ORDER BY, Subqueries

### 5. Transaction Management

Track database changes with commit/rollback:

```sql
termibase> INSERT INTO users (name, age) VALUES ('Alice', 25);
💡 Use .commit to save changes or .rollback to discard

termibase> .commit
✓ Changes committed successfully
```

## REPL Commands

| Command | Description |
|---------|-------------|
| `.help` | Show all available commands |
| `.challenge` | Enter SQL challenge environment |
| `.learn` | Interactive SQL learning mode |
| `.explain` | Toggle conceptual execution flow display |
| `.commit` | Commit pending database changes |
| `.rollback` | Rollback pending changes |
| `.tables` | List all tables |
| `.schema` | Show table schemas |
| `.exit` or `.quit` | Exit REPL |

## Usage Examples

### Basic Queries

```sql
-- Simple select
SELECT * FROM users LIMIT 5;

-- Filtering
SELECT name, age FROM users WHERE age > 28;

-- Grouping
SELECT city, COUNT(*) as count FROM users GROUP BY city;

-- Joins
SELECT u.name, o.amount 
FROM users u 
JOIN orders o ON u.id = o.user_id;
```

### Challenge Environment

```bash
termibase> .challenge
challenge> .list                    # View all challenges
challenge> .list easy               # Filter by difficulty
challenge> .start 42                # Start challenge #42
challenge> SELECT * FROM ...        # Write your solution
challenge> .submit                  # Submit and check
challenge> .stats                   # View progress
challenge> :exit                    # Return to main REPL
```

## Command-Line Commands

### `termibase`
Launch interactive REPL (main interface).

```bash
termibase
```

### `termibase init`
Initialize or reset the sandbox database.

```bash
termibase init
termibase init --db-path ./my-db.db
```

### `termibase run`
Execute a single query with optional visualization.

```bash
termibase run "SELECT * FROM users WHERE age > 25"
termibase run "SELECT * FROM users" --no-explain  # Results only
```

### `termibase explain`
Show conceptual execution flow without running query.

```bash
termibase explain "SELECT * FROM users JOIN orders ON users.id = orders.user_id"
```

## Demo Data

Pre-loaded tables:
- **users** - `id`, `name`, `age`, `city`
- **orders** - `id`, `user_id`, `amount`, `date`

## How TermiBase Differs from Oracle SQL*Plus

### What SQL*Plus Does Poorly for Students

- **Cryptic error messages:** SQL*Plus errors are often unhelpful for beginners
- **No query structure feedback:** Students can't see how their query is parsed
- **No safe experimentation:** Easy to accidentally modify or drop data
- **Minimal learning support:** No guided lessons or practice challenges
- **Hostile defaults:** Verbose output and complex configuration

### What TermiBase Intentionally Improves

- **Clear error messages:** Friendly explanations of SQL syntax errors
- **Query analysis:** Shows how queries are structured and parsed
- **Safe sandbox:** Isolated environment for experimentation
- **Guided learning:** Interactive lessons and structured challenges
- **Progressive disclosure:** Start simple, enable advanced features as needed

### What TermiBase Intentionally Does NOT Change

- **Terminal-first workflow:** Maintains SQL*Plus command-line interface
- **Multi-line input:** Preserves SQL*Plus continuation prompt style
- **Command structure:** Uses dot-commands (`.help`, `.exit`) similar to SQL*Plus
- **Result presentation:** Table output format matches SQL*Plus conventions

## Accuracy & Transparency

### Conceptual Visualizations

TermiBase's execution flow visualizations are **conceptual teaching aids**, not accurate representations of physical database execution.

**What they show:**
- Logical order of SQL clause processing (FROM → WHERE → SELECT, etc.)
- Relationships between query components
- How different SQL constructs relate to each other

**What they do NOT show:**
- Actual execution costs from the database engine
- Real row count estimates
- Physical execution plans (index usage, scan types, etc.)
- Performance characteristics

### Physical Execution Behavior

Physical execution behavior depends entirely on the database engine (SQLite in TermiBase's case). The database engine:
- Chooses execution strategies based on available indexes
- Estimates costs using its own statistics
- Optimizes queries according to its internal algorithms

**Students should not:**
- Generalize conceptual flow as physical execution
- Use conceptual visualizations for query optimization
- Assume costs or row counts reflect real database behavior

**Students should:**
- Use conceptual visualizations to understand SQL syntax and structure
- Learn physical execution from database-specific tools (SQLite's `EXPLAIN QUERY PLAN`, PostgreSQL's `EXPLAIN`, etc.)
- Practice SQL*Plus workflows for exam preparation

### Implementation Notes

- Execution flow visualization uses heuristics and simulation, not database engine output
- Query analysis is based on SQL parsing, not execution metadata
- Suggestions are educational guidance, not optimization recommendations

## Architecture

```
termibase/
├── cli/          # Command-line interface
├── parser/       # SQL parsing and analysis
├── engine/       # Query execution simulation (conceptual)
├── visualizer/   # Rich-based terminal rendering
├── storage/      # SQLite wrapper
├── challenge/    # SQL challenge environment
└── learn/        # Interactive learning module
```

## Development

```bash
# Clone and setup
git clone https://github.com/tejgokani/TermiBase.git
cd TermiBase
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Run tests
pytest termibase/tests/
```

## Requirements

- Python 3.8+
- SQLite (included with Python)

## Platform Support

- ✅ **macOS** - Homebrew or pip
- ✅ **Linux** - pip or pipx
- ✅ **Windows** - pip (use `python -m termibase` or add to PATH)

## Update

**Homebrew:**
```bash
brew upgrade termibase
```

**pip:**
```bash
pip install --upgrade termibase
```

## Built With

- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal output
- [sqlparse](https://github.com/andialbrecht/sqlparse) - SQL parsing
- [SQLite](https://www.sqlite.org/) - Database

## Support

- **Issues**: [GitHub Issues](https://github.com/tejgokani/TermiBase/issues)
- **Documentation**: This README

---

**Happy Learning!**
