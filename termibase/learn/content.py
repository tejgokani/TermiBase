"""SQL learning content and lessons."""

from typing import Dict, List, Tuple


def get_learning_topics() -> Dict[str, Dict]:
    """Get all available learning topics.
    
    Returns:
        Dictionary mapping topic names to their content
    """
    return {
        "SELECT Basics": {
            "description": "Learn the fundamentals of SELECT queries",
            "examples": [
                "SELECT * FROM users;",
                "SELECT name, age FROM users;",
                "SELECT name AS user_name FROM users;"
            ],
            "explanation": """
SELECT is the most fundamental SQL command. It retrieves data from tables.

Basic Syntax:
  SELECT column1, column2 FROM table_name;

Key Concepts:
  • Use * to select all columns
  • Specify column names to select specific columns
  • Use AS to create aliases for columns
  • Always end with semicolon (;)
            """.strip(),
            "practice_query": "SELECT * FROM users LIMIT 5;"
        },
        
        "WHERE Clause": {
            "description": "Filter data using WHERE conditions",
            "examples": [
                "SELECT * FROM users WHERE age > 25;",
                "SELECT * FROM users WHERE city = 'New York';",
                "SELECT * FROM users WHERE age BETWEEN 25 AND 35;"
            ],
            "explanation": """
WHERE clause filters rows based on conditions.

Operators:
  • = (equals)
  • >, <, >=, <= (comparisons)
  • != or <> (not equal)
  • BETWEEN (range)
  • IN (list of values)
  • LIKE (pattern matching)
  • IS NULL / IS NOT NULL

Examples:
  WHERE age > 25        -- Greater than
  WHERE city = 'NYC'    -- Exact match
  WHERE name LIKE 'A%'  -- Starts with A
            """.strip(),
            "practice_query": "SELECT * FROM users WHERE age > 28;"
        },
        
        "JOINs": {
            "description": "Combine data from multiple tables",
            "examples": [
                "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id;",
                "SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id;",
                "SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id;"
            ],
            "explanation": """
JOINs combine rows from two or more tables.

Types:
  • INNER JOIN - Returns matching rows from both tables
  • LEFT JOIN - Returns all rows from left table + matching from right
  • RIGHT JOIN - Returns all rows from right table + matching from left
  • FULL OUTER JOIN - Returns all rows from both tables

Syntax:
  SELECT columns
  FROM table1
  JOIN table2 ON table1.id = table2.foreign_id

The ON clause specifies how tables are related.
            """.strip(),
            "practice_query": "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id LIMIT 5;"
        },
        
        "GROUP BY & Aggregation": {
            "description": "Group data and use aggregate functions",
            "examples": [
                "SELECT city, COUNT(*) FROM users GROUP BY city;",
                "SELECT city, AVG(age) FROM users GROUP BY city;",
                "SELECT city, COUNT(*) FROM users GROUP BY city HAVING COUNT(*) > 1;"
            ],
            "explanation": """
GROUP BY groups rows with the same values in specified columns.

Aggregate Functions:
  • COUNT() - Count rows
  • SUM() - Sum of values
  • AVG() - Average of values
  • MAX() - Maximum value
  • MIN() - Minimum value

HAVING vs WHERE:
  • WHERE filters rows BEFORE grouping
  • HAVING filters groups AFTER grouping

Example:
  SELECT city, COUNT(*) as count
  FROM users
  GROUP BY city
  HAVING COUNT(*) > 1;
            """.strip(),
            "practice_query": "SELECT city, COUNT(*) as user_count FROM users GROUP BY city;"
        },
        
        "ORDER BY": {
            "description": "Sort query results",
            "examples": [
                "SELECT * FROM users ORDER BY age;",
                "SELECT * FROM users ORDER BY age DESC;",
                "SELECT * FROM users ORDER BY city, age DESC;"
            ],
            "explanation": """
ORDER BY sorts the result set.

Syntax:
  ORDER BY column1 [ASC|DESC], column2 [ASC|DESC]

Key Points:
  • ASC (ascending) is default
  • DESC (descending) for reverse order
  • Can sort by multiple columns
  • First column takes priority

Examples:
  ORDER BY age              -- Ascending (youngest first)
  ORDER BY age DESC         -- Descending (oldest first)
  ORDER BY city, age DESC    -- Sort by city, then age descending
            """.strip(),
            "practice_query": "SELECT * FROM users ORDER BY age DESC LIMIT 5;"
        },
        
        "Subqueries": {
            "description": "Nested queries and subqueries",
            "examples": [
                "SELECT name FROM users WHERE age > (SELECT AVG(age) FROM users);",
                "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);"
            ],
            "explanation": """
Subqueries are queries nested inside other queries.

Types:
  • Scalar subquery - Returns single value
  • Row subquery - Returns single row
  • Table subquery - Returns multiple rows

Common Uses:
  • In WHERE clause for filtering
  • In SELECT clause for calculations
  • In FROM clause as derived table

Example:
  SELECT name
  FROM users
  WHERE age > (SELECT AVG(age) FROM users);
  
This finds users older than the average age.
            """.strip(),
            "practice_query": "SELECT name, age FROM users WHERE age > (SELECT AVG(age) FROM users);"
        },
        
        "Indexes & Performance": {
            "description": "Understand indexes and query optimization",
            "examples": [
                "CREATE INDEX idx_age ON users(age);",
                "SELECT * FROM users WHERE age = 30;  -- Uses index",
                "EXPLAIN QUERY PLAN SELECT * FROM users WHERE age > 25;"
            ],
            "explanation": """
Indexes speed up queries by creating a data structure for fast lookups.

When to Use:
  • Columns used in WHERE clauses
  • Columns used in JOIN conditions
  • Columns used in ORDER BY

Trade-offs:
  • Faster SELECT queries
  • Slower INSERT/UPDATE (index must be updated)
  • Uses additional storage

Best Practices:
  • Index frequently queried columns
  • Don't over-index (slows writes)
  • Use EXPLAIN to see query plans
            """.strip(),
            "practice_query": "SELECT * FROM users WHERE city = 'New York';"
        }
    }


def get_topic_list() -> List[str]:
    """Get list of available topics.
    
    Returns:
        List of topic names
    """
    return list(get_learning_topics().keys())

