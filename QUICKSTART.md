# 🚀 Quick Start Guide

## Install in 10 Seconds

```bash
pip install termibase
```

## Use Immediately

Just type `termibase` and start querying:

```bash
termibase
```

You'll see:
```
✨ TermiBase - Your Database Learning Playground

💡 Tip: Type SQL queries to see how they're executed step-by-step
   Use .help for commands, .exit to quit

termibase> 
```

## Try These Commands

```sql
-- See all users
SELECT * FROM users;

-- Filter by age
SELECT name, age FROM users WHERE age > 28;

-- Group by city
SELECT city, COUNT(*) as count FROM users GROUP BY city;

-- Join tables
SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id;
```

## Built-in Commands

- `.help` - Show all commands
- `.tables` - List all tables
- `.schema` - Show table structure
- `.examples` - Show example queries
- `.explain` - Toggle execution plan display
- `.exit` - Quit REPL

## That's It!

No setup needed. The database initializes automatically on first run.

Enjoy learning SQL! 🎉

