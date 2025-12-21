# TermiBase 🚀

A terminal-native database learning playground that lets you run SQL queries and observe how they're parsed, planned, and executed—all from your command line.

**Install in one command:** `brew install tejgokani/termibase/termibase` or `pip install termibase`  
**Use immediately:** Just type `termibase` and start querying!

## 🎯 What is TermiBase?

TermiBase is an educational tool designed to help developers understand database internals by providing:
- **Interactive SQL REPL** with real-time query analysis
- **Multi-line query support** (SQL*Plus style) - write queries across multiple lines
- **Command history** with arrow key navigation (↑↓)
- **Execution plan visualization** showing how queries are processed step-by-step
- **Query optimization suggestions** to learn best practices
- **Interactive learning mode** (`.learn`) with guided SQL lessons
- **Commit/rollback tracking** to manage database changes
- **Beautiful terminal UI** using Rich for a modern CLI experience
- **No browser required** - everything runs in your terminal

## 🚀 Quick Start

### Installation

**Option 1: Homebrew (Recommended for macOS)**
```bash
brew install termibase
```

**Option 2: pip (Recommended for Windows)**
```bash
pip install termibase
# After installation, use: python -m termibase
```

**Option 3: pip3**
```bash
pip3 install termibase
```

**Option 4: pipx (Recommended for CLI tools)**
```bash
pipx install termibase
```

### First Use

**macOS/Linux:**
```bash
termibase
```

**Windows:**
```bash
python -m termibase
```

> **Windows Note:** If the `termibase` command doesn't work, use `python -m termibase` instead. This is because Windows doesn't automatically add Python Scripts to PATH. The `python -m` method works on all systems without PATH configuration.

The database will be automatically initialized on first run. You'll see:

```
✨ TermiBase - Your Database Learning Playground

💡 Tip: Type SQL queries to see how they're executed step-by-step
   Use .help for commands, .exit to quit
   Write multi-line queries (end with ';') or use arrow keys for history

termibase> 
```

## 📖 Features

### 1. Multi-Line Query Input

Write SQL queries across multiple lines, just like SQL*Plus:

```sql
termibase> SELECT DISTINCT
      ->     c.customer_id,
      ->     c.first_name,
      ->     c.last_name
      -> FROM rental r
      -> INNER JOIN customer c ON r.customer_id = c.customer_id
      -> WHERE c.city = 'Lethbridge';
```

End your query with `;` to execute. Use `\` on an empty line to cancel.

### 2. Command History

Navigate your query history using arrow keys:
- **↑** - Previous query
- **↓** - Next query
- History is saved to `.termibase_history` and persists across sessions

### 3. Interactive Learning Mode

Learn SQL interactively with guided lessons:

```bash
termibase> .learn
```

**Available Topics:**
1. SELECT Basics
2. WHERE Clause
3. JOINs
4. GROUP BY & Aggregation
5. ORDER BY
6. Subqueries
7. Indexes & Performance

Each lesson includes:
- Detailed explanations
- Example queries
- Practice queries you can run
- Option to write your own queries

### 4. Commit/Rollback Tracking

TermiBase tracks uncommitted changes and prompts you to save before exiting:

```sql
termibase> INSERT INTO users (name, age, city) VALUES ('Alice', 25, 'NYC');
✓ Query executed successfully.
💡 Use .commit to save changes or .rollback to discard

termibase> .commit
✓ Changes committed successfully
```

**Commands:**
- `.commit` - Save pending changes
- `.rollback` - Discard pending changes

If you try to exit with uncommitted changes, you'll be prompted to commit.

### 5. Query Analysis & Visualization

Every query is automatically analyzed and visualized:

```sql
termibase> SELECT * FROM users WHERE age > 28;
```

**Shows:**
- Query structure (tables, columns, WHERE conditions)
- Execution plan (step-by-step processing)
- Query results (beautifully formatted tables)
- Optimization suggestions

### 6. Execution Plan Visualization

See how your query is executed internally:

```
Execution Plan
Query Execution
├── [1] TABLE_SCAN - Scanning table users (cost: 1.00, rows: 8)
├── [2] FILTER - Applying WHERE filter: age > 28 (cost: 0.30, rows: 4)
└── [3] PROJECT - Projecting all columns (cost: 0.20, rows: 4)
```

## 📚 REPL Commands

Inside the TermiBase REPL, use these commands:

| Command | Description |
|---------|-------------|
| `.help` | Show all available commands |
| `.learn` | Interactive SQL learning mode |
| `.explain` | Toggle execution plan display on/off |
| `.commit` | Commit pending database changes |
| `.rollback` | Rollback pending database changes |
| `.tables` | List all tables in the database |
| `.schema` | Show table schemas |
| `.examples` | Show example queries |
| `.exit` or `.quit` | Exit REPL |

## 🎮 Usage Examples

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

### Multi-Line Complex Query

```sql
termibase> SELECT DISTINCT
      ->     c.customer_id,
      ->     c.first_name,
      ->     c.last_name,
      ->     c.email,
      ->     s.store_id
      -> FROM rental r
      -> INNER JOIN staff st ON st.staff_id = r.staff_id
      -> INNER JOIN store s ON s.manager_staff_id = st.staff_id 
      ->     AND s.store_id = st.store_id
      -> INNER JOIN customer c ON r.customer_id = c.customer_id 
      ->     AND s.store_id = c.store_id
      -> INNER JOIN address a ON s.address_id = a.address_id
      -> INNER JOIN city ci ON ci.city_id = a.city_id
      -> WHERE ci.city = 'Lethbridge';
```

### Using Learning Mode

```bash
termibase> .learn

📚 SQL Learning Topics

#  Topic                        Description
─────────────────────────────────────────────────────────────────────
1  SELECT Basics               Learn the fundamentals of SELECT queries
2  WHERE Clause                Filter data using WHERE conditions
3  JOINs                       Combine data from multiple tables
4  GROUP BY & Aggregation      Group data and use aggregate functions
5  ORDER BY                    Sort query results
6  Subqueries                  Nested queries and subqueries
7  Indexes & Performance       Understand indexes and query optimization

Select a topic (1-7) or 'q' to quit: 3

📖 JOINs

Explanation:
JOINs combine rows from two or more tables.

Types:
  • INNER JOIN - Returns matching rows from both tables
  • LEFT JOIN - Returns all rows from left table + matching from right
  ...

Options:
  1 - Run practice query
  2 - Write your own query
  3 - See execution plan
  4 - Back to topics
```

## 🛠️ Command-Line Commands

### `termibase` (No Arguments)
Launches interactive REPL - the main way to use TermiBase.

```bash
termibase
```

### `termibase init`
Initialize or reset the sandbox database with demo data.

```bash
termibase init
termibase init --db-path ./my-db.db
```

### `termibase repl`
Explicitly launch REPL (same as `termibase`).

```bash
termibase repl
termibase repl --explain  # Always show execution plans
```

### `termibase run`
Execute a single query with full visualization.

```bash
termibase run "SELECT * FROM users WHERE age > 25"
termibase run "SELECT * FROM users" --no-explain  # Skip execution plan
```

### `termibase explain`
Show execution plan for a query without running it.

```bash
termibase explain "SELECT * FROM users JOIN orders ON users.id = orders.user_id"
```

### `termibase demo`
Run educational demo queries.

```bash
termibase demo              # Run all demos
termibase demo basics       # Run specific demo
```

## 🎓 Demo Data

TermiBase comes with pre-loaded demo data:

**Users Table:**
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `age` (INTEGER)
- `city` (TEXT)

**Orders Table:**
- `id` (INTEGER PRIMARY KEY)
- `user_id` (INTEGER, FOREIGN KEY)
- `amount` (REAL)
- `date` (TEXT)

**Indexes:**
- `idx_users_city` on `users(city)`
- `idx_orders_user_id` on `orders(user_id)`

## 🏗️ Architecture

TermiBase is built with a modular architecture:

```
termibase/
├── cli/          # Command-line interface (Typer)
│   ├── main.py    # Main CLI commands
│   └── input_handler.py  # Multi-line input & history
├── parser/        # SQL parsing and analysis
├── engine/       # Query execution simulation
├── visualizer/   # Rich-based terminal rendering
├── storage/      # SQLite wrapper
├── learn/        # Interactive learning module
└── demos/        # Educational examples
```

### Key Components

- **CLI Interface**: Handles commands, flags, and REPL loop
- **Input Handler**: Multi-line query input with readline history support
- **SQL Parser**: Parses SQL into tokens and AST using `sqlparse`
- **Query Analyzer**: Identifies query type, tables, indexes, joins
- **Execution Simulator**: Simulates logical execution steps
- **Storage Engine**: SQLite wrapper for actual query execution
- **Visualizer**: Renders execution plans and results using Rich
- **Learning Module**: Interactive SQL lessons and practice

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

## 🔧 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/tejgokani/TermiBase.git
cd TermiBase

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .
```

### Running Tests

```bash
pytest termibase/tests/
```

## 🎨 Design Philosophy

- **Terminal-first**: Everything works in the terminal, no browser needed
- **Educational**: Transparent about how queries are processed
- **Fast feedback**: Immediate visualization of query execution
- **Developer-centric**: Built for developers learning databases
- **Interactive**: Multi-line queries, history, and guided learning
- **Safe**: Commit/rollback tracking prevents accidental data loss

## 📝 Requirements

- Python 3.8 or higher
- SQLite (included with Python)

## 🌐 Platform Support

- ✅ **macOS** - Install via Homebrew or pip. Use `termibase` command.
- ✅ **Linux** - Install via pip or pipx. Use `termibase` command.
- ✅ **Windows** - Install via pip. Use `python -m termibase` (recommended) or add Scripts to PATH for `termibase` command.

## 🔄 Update TermiBase

**Homebrew:**
```bash
brew upgrade termibase
```

**pip:**
```bash
pip install --upgrade termibase
```

## 🗑️ Uninstall

**Homebrew:**
```bash
brew uninstall termibase
```

**pip:**
```bash
pip uninstall termibase
```

## License

TermiBase is **source-available**.
You are free to use and study the code, but modification and redistribution
are not permitted without explicit permission.



## 🙏 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - Modern CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [sqlparse](https://github.com/andialbrecht/sqlparse) - SQL parsing
- [SQLite](https://www.sqlite.org/) - Embedded database

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/tejgokani/TermiBase/issues)
- **Documentation**: This README

---

**Happy Learning!** 🎉
