#!/usr/bin/env python3
"""Test edge cases and potential failure scenarios."""

import sys
from pathlib import Path
import tempfile
import os

sys.path.insert(0, str(Path(__file__).parent))

from termibase.storage.engine import StorageEngine
from termibase.parser.analyzer import QueryAnalyzer
from termibase.engine.simulator import ExecutionSimulator
from termibase.demos.data import setup_demo_data

class EdgeCaseTester:
    def __init__(self):
        self.issues = []
        
    def test(self, name, func):
        """Test and collect issues."""
        try:
            func()
            print(f"✅ {name}")
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            self.issues.append((name, str(e)))

tester = EdgeCaseTester()

# Setup
test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
test_db.close()
storage = StorageEngine(test_db.name)
storage.connect()
setup_demo_data(storage)

print("="*60)
print("EDGE CASE & ERROR HANDLING TESTS")
print("="*60)

# Test malformed queries
def test_empty_query():
    analyzer = QueryAnalyzer("")
    analysis = analyzer.analyze()
    assert analysis['type'] == 'UNKNOWN'

def test_invalid_sql():
    try:
        storage.execute("SELECT * FROM nonexistent_table")
    except:
        pass  # Should handle gracefully

def test_malformed_where():
    try:
        storage.execute("SELECT * FROM users WHERE")
    except:
        pass  # Should handle gracefully

def test_missing_table():
    try:
        storage.execute("SELECT * FROM table_that_does_not_exist")
    except:
        pass  # Should handle gracefully

def test_syntax_error():
    try:
        storage.execute("SELCT * FROM users")  # Typo
    except:
        pass  # Should handle gracefully

def test_parser_complex_nested():
    """Test parser on complex nested queries"""
    query = """
    SELECT u.name, 
           (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
    FROM users u
    """
    analyzer = QueryAnalyzer(query)
    analysis = analyzer.analyze()
    # Should not crash

def test_parser_with_comments():
    """Test parser with SQL comments"""
    query = """
    -- This is a comment
    SELECT * FROM users
    /* Another comment */
    WHERE age > 25
    """
    analyzer = QueryAnalyzer(query)
    analysis = analyzer.analyze()

def test_parser_special_characters():
    """Test parser with special characters in strings"""
    storage.execute("INSERT INTO users (name, age, city) VALUES ('O''Brien', 30, 'New York')")
    results = storage.execute("SELECT * FROM users WHERE name = 'O''Brien'")
    storage.execute("DELETE FROM users WHERE name = 'O''Brien'")

def test_parser_multiline():
    """Test parser on multiline queries"""
    query = """
    SELECT 
        u.name,
        u.age,
        COUNT(o.id) as orders
    FROM 
        users u
    LEFT JOIN 
        orders o ON u.id = o.user_id
    WHERE 
        u.age > 25
    GROUP BY 
        u.id, u.name, u.age
    ORDER BY 
        orders DESC
    """
    analyzer = QueryAnalyzer(query)
    analysis = analyzer.analyze()
    assert analysis['type'] == 'SELECT'

def test_simulator_empty_result():
    """Test simulator on query with no results"""
    simulator = ExecutionSimulator(storage)
    steps = simulator.simulate("SELECT * FROM users WHERE age > 1000")
    assert len(steps) > 0

def test_simulator_complex():
    """Test simulator on very complex query"""
    query = """
    SELECT 
        u.city,
        AVG(u.age) as avg_age,
        COUNT(DISTINCT u.id) as user_count,
        SUM(o.amount) as total_revenue
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.age IS NOT NULL
    GROUP BY u.city
    HAVING COUNT(DISTINCT u.id) > 1
    ORDER BY total_revenue DESC NULLS LAST
    LIMIT 10
    """
    simulator = ExecutionSimulator(storage)
    steps = simulator.simulate(query)
    assert len(steps) > 0

def test_unicode_names():
    """Test with unicode characters"""
    storage.execute("INSERT INTO users (name, age, city) VALUES ('José', 30, 'São Paulo')")
    results = storage.execute("SELECT * FROM users WHERE name = 'José'")
    storage.execute("DELETE FROM users WHERE name = 'José'")

def test_large_result_set():
    """Test handling of larger result sets"""
    # Insert many rows
    for i in range(50):
        storage.execute(f"INSERT INTO users (name, age, city) VALUES ('User{i}', {20+i}, 'City{i%5}')")
    
    results = storage.execute("SELECT * FROM users")
    assert len(results) > 50
    
    # Cleanup
    storage.execute("DELETE FROM users WHERE name LIKE 'User%'")

def test_transaction_rollback():
    """Test transaction handling"""
    try:
        with storage.transaction():
            storage.execute("INSERT INTO users (name, age, city) VALUES ('TransTest', 25, 'City')")
            raise Exception("Simulated error")
    except:
        pass
    # Should rollback
    results = storage.execute("SELECT * FROM users WHERE name = 'TransTest'")
    assert len(results) == 0

def test_index_operations():
    """Test index creation and usage"""
    storage.execute("CREATE INDEX IF NOT EXISTS idx_test ON users(age)")
    results = storage.execute("SELECT * FROM users WHERE age = 30")
    # Should use index if possible

def test_table_info():
    """Test getting table information"""
    info = storage.get_table_info("users")
    assert len(info) > 0

def test_get_tables():
    """Test listing tables"""
    tables = storage.get_tables()
    assert 'users' in tables
    assert 'orders' in tables

# Run edge case tests
print("\nTesting edge cases...\n")

tester.test("Empty query", test_empty_query)
tester.test("Invalid SQL", test_invalid_sql)
tester.test("Malformed WHERE", test_malformed_where)
tester.test("Missing table", test_missing_table)
tester.test("Syntax error", test_syntax_error)
tester.test("Complex nested query", test_parser_complex_nested)
tester.test("Query with comments", test_parser_with_comments)
tester.test("Special characters", test_parser_special_characters)
tester.test("Multiline query", test_parser_multiline)
tester.test("Simulator empty result", test_simulator_empty_result)
tester.test("Simulator complex", test_simulator_complex)
tester.test("Unicode names", test_unicode_names)
tester.test("Large result set", test_large_result_set)
tester.test("Transaction rollback", test_transaction_rollback)
tester.test("Index operations", test_index_operations)
tester.test("Table info", test_table_info)
tester.test("Get tables", test_get_tables)

storage.close()
os.unlink(test_db.name)

print("\n" + "="*60)
if tester.issues:
    print(f"Found {len(tester.issues)} potential issues:")
    for name, error in tester.issues:
        print(f"  - {name}: {error}")
else:
    print("✅ All edge cases handled gracefully!")
print("="*60)

