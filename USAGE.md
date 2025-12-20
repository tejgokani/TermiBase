# 📖 TermiBase Usage Guide

## Installation

```bash
pip install termibase
```

## Basic Usage

### Launch Interactive REPL (Default)

Simply run:
```bash
termibase
```

This launches a Gemini-like interactive terminal where you can:
- Type SQL queries directly
- See query execution plans
- Get optimization suggestions
- Learn database internals

### Example Session

```bash
$ termibase

✨ TermiBase - Your Database Learning Playground

💡 Tip: Type SQL queries to see how they're executed step-by-step
   Use .help for commands, .exit to quit

termibase> SELECT * FROM users LIMIT 3;

Query Analysis
┌─────────────┬─────────────────┐
│ Property    │ Value           │
├─────────────┼─────────────────┤
│ Query Type  │ SELECT          │
│ Tables      │ users           │
│ Columns     │ *               │
│ LIMIT       │ 3               │
└─────────────┴─────────────────┘

Query Results
┌──────┬─────────┬─────┬──────────────┐
│ id   │ name    │ age │ city         │
├──────┼─────────┼─────┼──────────────┤
│ 1    │ Alice   │ 25  │ New York     │
│ 2    │ Bob     │ 30  │ San Francisco│
│ 3    │ Charlie │ 35  │ New York     │
└──────┴─────────┴─────┴──────────────┘

termibase> .help

📚 TermiBase Commands

  .help     - Show this help
  .explain  - Toggle execution plan display
  .tables   - List all tables
  .schema   - Show table schemas
  .examples - Show example queries
  .exit     - Exit REPL

💡 Just type SQL queries to execute them!

termibase> .exit
Goodbye!
```

## Commands

### `termibase` (No Arguments)
Launches interactive REPL - the main way to use TermiBase.

### `termibase init`
Initialize or reset the sandbox database.

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
Execute a single query with visualization.

```bash
termibase run "SELECT * FROM users WHERE age > 25"
termibase run "SELECT * FROM users" --no-explain
```

### `termibase explain`
Show execution plan without running query.

```bash
termibase explain "SELECT * FROM users JOIN orders ON users.id = orders.user_id"
```

### `termibase demo`
Run educational demo queries.

```bash
termibase demo              # All demos
termibase demo basics       # Basic queries
termibase demo joins       # JOIN examples
termibase demo indexes     # Index examples
termibase demo advanced    # Advanced queries
```

## REPL Commands

Inside the REPL, use these commands:

- `.help` - Show help
- `.explain` - Toggle execution plan display on/off
- `.tables` - List all tables
- `.schema` - Show table schemas
- `.examples` - Show example queries
- `.exit` or `.quit` - Exit REPL

## Features

### 1. Query Analysis
Every query is automatically analyzed showing:
- Query type (SELECT, INSERT, etc.)
- Tables involved
- Columns selected
- WHERE conditions
- JOIN operations
- GROUP BY, ORDER BY, LIMIT clauses

### 2. Execution Visualization
See step-by-step execution:
- Table scans vs index scans
- Filter operations
- Join strategies
- Sorting and grouping
- Cost estimates

### 3. Optimization Suggestions
Get tips on improving queries:
- Index recommendations
- Full table scan warnings
- Large result set alerts

## Example Queries

```sql
-- Simple select
SELECT * FROM users;

-- Filtering
SELECT name, age FROM users WHERE age > 28;

-- Grouping
SELECT city, COUNT(*) FROM users GROUP BY city;

-- Joins
SELECT u.name, o.amount 
FROM users u 
JOIN orders o ON u.id = o.user_id;

-- Aggregation
SELECT city, AVG(age) as avg_age 
FROM users 
GROUP BY city 
HAVING AVG(age) > 28;
```

## Tips

1. **Start Simple**: Begin with basic SELECT queries
2. **Use .explain**: Toggle execution plans to see how queries work
3. **Try .examples**: See example queries for inspiration
4. **Check .schema**: Understand table structure before querying
5. **Learn Internals**: Pay attention to execution steps and costs

## Troubleshooting

**Command not found:**
- Make sure you activated virtual environment (if using one)
- Check PATH includes pip installation directory
- Try: `python3 -m termibase.cli.main`

**Database errors:**
- Run `termibase init` to reset database
- Check file permissions

**Import errors:**
- Reinstall: `pip install --upgrade termibase`
- Check Python version: `python3 --version` (needs 3.8+)

## Next Steps

- Read `QUICKSTART.md` for quick examples
- Read `README.md` for full documentation
- Explore `termibase demo` for educational examples

Happy learning! 🎉

