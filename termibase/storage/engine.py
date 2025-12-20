"""Storage engine wrapper around SQLite."""

import sqlite3
import os
from pathlib import Path
from typing import Optional, List, Tuple, Any
from contextlib import contextmanager


class StorageEngine:
    """Manages SQLite database connections and operations."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize storage engine.
        
        Args:
            db_path: Path to SQLite database file. If None, uses in-memory database.
        """
        if db_path is None:
            self.db_path = ":memory:"
        else:
            self.db_path = db_path
            # Ensure directory exists
            if db_path != ":memory:":
                Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Establish database connection."""
        if self.conn is None:
            # Use DEFERRED isolation level to support transactions
            self.conn = sqlite3.connect(self.db_path, isolation_level="DEFERRED")
            self.conn.row_factory = sqlite3.Row  # Return dict-like rows
            # Enable foreign keys
            self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """Execute a query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result rows
        """
        if self.conn is None:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        
        if query.strip().upper().startswith(('SELECT', 'WITH', 'PRAGMA')):
            return cursor.fetchall()
        else:
            # Commit only if not in a transaction context
            # Check if we're in a transaction by trying to access isolation_level
            # If isolation_level is None, we're in autocommit mode
            if hasattr(self.conn, 'in_transaction') and self.conn.in_transaction:
                pass  # Transaction context manager will handle commit
            else:
                self.conn.commit()
            return []

    def execute_many(self, query: str, params_list: List[Tuple]) -> None:
        """Execute a query multiple times with different parameters.
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
        """
        if self.conn is None:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.executemany(query, params_list)
        self.conn.commit()

    def get_table_info(self, table_name: str) -> List[sqlite3.Row]:
        """Get schema information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information rows
        """
        return self.execute(f"PRAGMA table_info({table_name})")

    def get_tables(self) -> List[str]:
        """Get list of all tables in the database.
        
        Returns:
            List of table names
        """
        rows = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row[0] for row in rows]

    def get_indexes(self, table_name: Optional[str] = None) -> List[sqlite3.Row]:
        """Get index information.
        
        Args:
            table_name: Optional table name to filter indexes
            
        Returns:
            List of index information rows
        """
        if table_name:
            return self.execute(f"PRAGMA index_list({table_name})")
        else:
            rows = self.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
            )
            return rows

    def explain_query_plan(self, query: str) -> List[sqlite3.Row]:
        """Get SQLite's query plan explanation.
        
        Args:
            query: SQL query string
            
        Returns:
            Query plan rows
        """
        return self.execute(f"EXPLAIN QUERY PLAN {query}")

    @contextmanager
    def transaction(self):
        """Context manager for transactions."""
        if self.conn is None:
            self.connect()
        
        # SQLite with DEFERRED isolation level auto-starts transactions
        # We just need to handle commit/rollback
        try:
            yield
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

