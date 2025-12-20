"""Tests for storage engine."""

import pytest
import tempfile
import os
from termibase.storage.engine import StorageEngine


def test_in_memory_database():
    """Test in-memory database operations."""
    storage = StorageEngine()
    storage.connect()
    
    # Create table
    storage.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    
    # Insert data
    storage.execute("INSERT INTO test VALUES (1, 'Alice')")
    
    # Query data
    results = storage.execute("SELECT * FROM test")
    assert len(results) == 1
    assert results[0][0] == 1
    assert results[0][1] == 'Alice'
    
    storage.close()


def test_file_database():
    """Test file-based database operations."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    try:
        storage = StorageEngine(db_path)
        storage.connect()
        
        storage.execute("CREATE TABLE test (id INTEGER, name TEXT)")
        storage.execute("INSERT INTO test VALUES (1, 'Bob')")
        
        results = storage.execute("SELECT * FROM test")
        assert len(results) == 1
        assert results[0][1] == 'Bob'
        
        storage.close()
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_table_info():
    """Test getting table information."""
    storage = StorageEngine()
    storage.connect()
    
    storage.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    info = storage.get_table_info("users")
    
    assert len(info) == 3
    column_names = [row[1] for row in info]
    assert 'id' in column_names
    assert 'name' in column_names
    assert 'age' in column_names
    
    storage.close()

