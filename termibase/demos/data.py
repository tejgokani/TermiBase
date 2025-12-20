"""Demo data setup and educational queries."""

from termibase.storage.engine import StorageEngine
from typing import List, Tuple, Dict


def setup_demo_data(storage: StorageEngine) -> None:
    """Initialize demo database with sample data.
    
    Args:
        storage: Storage engine instance
    """
    # Create users table
    storage.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            city TEXT
        )
    """)
    
    # Create orders table
    storage.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Insert sample users
    users_data = [
        ("Alice", 25, "New York"),
        ("Bob", 30, "San Francisco"),
        ("Charlie", 35, "New York"),
        ("Diana", 28, "Boston"),
        ("Eve", 32, "San Francisco"),
        ("Frank", 27, "Chicago"),
        ("Grace", 29, "New York"),
        ("Henry", 31, "Boston"),
    ]
    
    storage.execute("DELETE FROM users")
    storage.execute_many(
        "INSERT INTO users (name, age, city) VALUES (?, ?, ?)",
        users_data
    )
    
    # Insert sample orders
    orders_data = [
        (1, 150.00, "2024-01-15"),
        (1, 75.50, "2024-02-20"),
        (2, 200.00, "2024-01-10"),
        (2, 120.00, "2024-03-05"),
        (3, 90.00, "2024-02-14"),
        (4, 300.00, "2024-01-25"),
        (4, 50.00, "2024-03-10"),
        (5, 180.00, "2024-02-01"),
        (6, 95.00, "2024-01-30"),
        (7, 220.00, "2024-02-15"),
        (7, 110.00, "2024-03-20"),
        (8, 160.00, "2024-01-20"),
    ]
    
    storage.execute("DELETE FROM orders")
    storage.execute_many(
        "INSERT INTO orders (user_id, amount, date) VALUES (?, ?, ?)",
        orders_data
    )
    
    # Create some indexes for demonstration
    storage.execute("CREATE INDEX IF NOT EXISTS idx_users_city ON users(city)")
    storage.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")


def get_demo_queries() -> Dict[str, List[Tuple[str, str]]]:
    """Get educational demo queries.
    
    Returns:
        Dictionary mapping demo names to lists of (query, description) tuples
    """
    return {
        "basics": [
            (
                "SELECT * FROM users",
                "Simple SELECT query - observe full table scan"
            ),
            (
                "SELECT name, age FROM users WHERE age > 28",
                "SELECT with WHERE filter - see how filtering works"
            ),
            (
                "SELECT * FROM users ORDER BY age DESC",
                "SELECT with ORDER BY - observe sorting operation"
            ),
            (
                "SELECT city, COUNT(*) as user_count FROM users GROUP BY city",
                "GROUP BY aggregation - see grouping in action"
            ),
        ],
        "joins": [
            (
                "SELECT u.name, o.amount, o.date FROM users u JOIN orders o ON u.id = o.user_id",
                "INNER JOIN - see how tables are combined"
            ),
            (
                "SELECT u.name, SUM(o.amount) as total_spent FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.name",
                "LEFT JOIN with aggregation - observe join strategy"
            ),
        ],
        "indexes": [
            (
                "SELECT * FROM users WHERE city = 'New York'",
                "Query using indexed column - compare with table scan"
            ),
            (
                "SELECT * FROM users WHERE age > 30",
                "Query on non-indexed column - see full table scan"
            ),
        ],
        "advanced": [
            (
                "SELECT u.name, COUNT(o.id) as order_count, SUM(o.amount) as total FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.name HAVING COUNT(o.id) > 1 ORDER BY total DESC",
                "Complex query with JOIN, GROUP BY, HAVING, and ORDER BY"
            ),
            (
                "SELECT city, AVG(age) as avg_age FROM users GROUP BY city HAVING AVG(age) > 28 ORDER BY avg_age",
                "Aggregation with HAVING clause"
            ),
        ],
    }

