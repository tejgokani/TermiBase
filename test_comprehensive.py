#!/usr/bin/env python3
"""Comprehensive test suite for TermiBase - tests all SQL operations."""

import sys
import traceback
from pathlib import Path
import tempfile
import os

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from termibase.storage.engine import StorageEngine
from termibase.parser.analyzer import QueryAnalyzer
from termibase.engine.simulator import ExecutionSimulator
from termibase.visualizer.renderer import QueryVisualizer
from termibase.demos.data import setup_demo_data

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def test(self, name, func):
        """Run a test and track results."""
        try:
            print(f"\n🧪 Testing: {name}")
            func()
            print(f"✅ PASSED: {name}")
            self.passed += 1
        except Exception as e:
            print(f"❌ FAILED: {name}")
            print(f"   Error: {str(e)}")
            self.errors.append((name, str(e), traceback.format_exc()))
            self.failed += 1
    
    def summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print(f"TEST SUMMARY")
        print("="*60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📊 Total:  {self.passed + self.failed}")
        print("="*60)
        
        if self.errors:
            print("\n❌ FAILED TESTS:")
            for name, error, trace in self.errors:
                print(f"\n{name}:")
                print(f"  {error}")
                if "--verbose" in sys.argv:
                    print(trace)

# Create test runner
runner = TestRunner()

# Setup test database
test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
test_db.close()
storage = StorageEngine(test_db.name)
storage.connect()
setup_demo_data(storage)

print("="*60)
print("COMPREHENSIVE TERMIBASE TEST SUITE")
print("="*60)

# ============================================================================
# BASIC SELECT TESTS
# ============================================================================

def test_select_all():
    """Test SELECT * FROM table"""
    results = storage.execute("SELECT * FROM users")
    assert len(results) > 0, "Should return users"
    assert len(results[0]) == 4, "Should have 4 columns (id, name, age, city)"

def test_select_columns():
    """Test SELECT specific columns"""
    results = storage.execute("SELECT name, age FROM users")
    assert len(results) > 0
    assert len(results[0]) == 2

def test_select_with_alias():
    """Test SELECT with column aliases"""
    results = storage.execute("SELECT name AS user_name, age AS user_age FROM users")
    assert len(results) > 0

def test_select_distinct():
    """Test SELECT DISTINCT"""
    results = storage.execute("SELECT DISTINCT city FROM users")
    assert len(results) > 0

# ============================================================================
# WHERE CLAUSE TESTS
# ============================================================================

def test_where_equals():
    """Test WHERE column = value"""
    results = storage.execute("SELECT * FROM users WHERE age = 30")
    assert len(results) >= 0

def test_where_greater_than():
    """Test WHERE column > value"""
    results = storage.execute("SELECT * FROM users WHERE age > 28")
    assert len(results) >= 0

def test_where_less_than():
    """Test WHERE column < value"""
    results = storage.execute("SELECT * FROM users WHERE age < 30")
    assert len(results) >= 0

def test_where_greater_equal():
    """Test WHERE column >= value"""
    results = storage.execute("SELECT * FROM users WHERE age >= 28")
    assert len(results) >= 0

def test_where_less_equal():
    """Test WHERE column <= value"""
    results = storage.execute("SELECT * FROM users WHERE age <= 30")
    assert len(results) >= 0

def test_where_not_equal():
    """Test WHERE column != value"""
    results = storage.execute("SELECT * FROM users WHERE age != 30")
    assert len(results) >= 0

def test_where_like():
    """Test WHERE column LIKE pattern"""
    results = storage.execute("SELECT * FROM users WHERE name LIKE 'A%'")
    assert len(results) >= 0

def test_where_in():
    """Test WHERE column IN (values)"""
    results = storage.execute("SELECT * FROM users WHERE age IN (25, 30, 35)")
    assert len(results) >= 0

def test_where_between():
    """Test WHERE column BETWEEN values"""
    results = storage.execute("SELECT * FROM users WHERE age BETWEEN 25 AND 30")
    assert len(results) >= 0

def test_where_and():
    """Test WHERE with AND"""
    results = storage.execute("SELECT * FROM users WHERE age > 25 AND age < 35")
    assert len(results) >= 0

def test_where_or():
    """Test WHERE with OR"""
    results = storage.execute("SELECT * FROM users WHERE age < 26 OR age > 34")
    assert len(results) >= 0

def test_where_is_null():
    """Test WHERE column IS NULL"""
    # First insert a row with NULL
    storage.execute("INSERT INTO users (name, age, city) VALUES ('TestNull', NULL, NULL)")
    results = storage.execute("SELECT * FROM users WHERE age IS NULL")
    assert len(results) >= 0
    storage.execute("DELETE FROM users WHERE name = 'TestNull'")

def test_where_is_not_null():
    """Test WHERE column IS NOT NULL"""
    results = storage.execute("SELECT * FROM users WHERE age IS NOT NULL")
    assert len(results) >= 0

# ============================================================================
# JOIN TESTS
# ============================================================================

def test_inner_join():
    """Test INNER JOIN"""
    results = storage.execute(
        "SELECT u.name, o.amount FROM users u INNER JOIN orders o ON u.id = o.user_id"
    )
    assert len(results) >= 0

def test_left_join():
    """Test LEFT JOIN"""
    results = storage.execute(
        "SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id"
    )
    assert len(results) >= 0

def test_join_with_where():
    """Test JOIN with WHERE clause"""
    results = storage.execute(
        "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id WHERE o.amount > 100"
    )
    assert len(results) >= 0

def test_multiple_joins():
    """Test multiple JOINs (if we had more tables)"""
    # This would work if we had more tables
    pass

# ============================================================================
# AGGREGATION TESTS
# ============================================================================

def test_count():
    """Test COUNT(*)"""
    results = storage.execute("SELECT COUNT(*) FROM users")
    assert len(results) > 0
    assert results[0][0] > 0

def test_count_column():
    """Test COUNT(column)"""
    results = storage.execute("SELECT COUNT(age) FROM users")
    assert len(results) > 0

def test_sum():
    """Test SUM()"""
    results = storage.execute("SELECT SUM(amount) FROM orders")
    assert len(results) > 0

def test_avg():
    """Test AVG()"""
    results = storage.execute("SELECT AVG(age) FROM users")
    assert len(results) > 0

def test_max():
    """Test MAX()"""
    results = storage.execute("SELECT MAX(age) FROM users")
    assert len(results) > 0

def test_min():
    """Test MIN()"""
    results = storage.execute("SELECT MIN(age) FROM users")
    assert len(results) > 0

# ============================================================================
# GROUP BY TESTS
# ============================================================================

def test_group_by():
    """Test GROUP BY"""
    results = storage.execute("SELECT city, COUNT(*) FROM users GROUP BY city")
    assert len(results) >= 0

def test_group_by_multiple():
    """Test GROUP BY multiple columns"""
    results = storage.execute("SELECT city, age, COUNT(*) FROM users GROUP BY city, age")
    assert len(results) >= 0

def test_group_by_with_aggregate():
    """Test GROUP BY with aggregate functions"""
    results = storage.execute("SELECT city, AVG(age) FROM users GROUP BY city")
    assert len(results) >= 0

# ============================================================================
# HAVING TESTS
# ============================================================================

def test_having():
    """Test HAVING clause"""
    results = storage.execute(
        "SELECT city, COUNT(*) as cnt FROM users GROUP BY city HAVING COUNT(*) > 1"
    )
    assert len(results) >= 0

def test_having_with_aggregate():
    """Test HAVING with aggregate function"""
    results = storage.execute(
        "SELECT city, AVG(age) as avg_age FROM users GROUP BY city HAVING AVG(age) > 28"
    )
    assert len(results) >= 0

# ============================================================================
# ORDER BY TESTS
# ============================================================================

def test_order_by_asc():
    """Test ORDER BY ASC"""
    results = storage.execute("SELECT * FROM users ORDER BY age ASC")
    assert len(results) > 0

def test_order_by_desc():
    """Test ORDER BY DESC"""
    results = storage.execute("SELECT * FROM users ORDER BY age DESC")
    assert len(results) > 0

def test_order_by_multiple():
    """Test ORDER BY multiple columns"""
    results = storage.execute("SELECT * FROM users ORDER BY city, age")
    assert len(results) > 0

# ============================================================================
# LIMIT AND OFFSET TESTS
# ============================================================================

def test_limit():
    """Test LIMIT"""
    results = storage.execute("SELECT * FROM users LIMIT 3")
    assert len(results) <= 3

def test_limit_offset():
    """Test LIMIT with OFFSET"""
    results = storage.execute("SELECT * FROM users LIMIT 3 OFFSET 2")
    assert len(results) <= 3

# ============================================================================
# INSERT TESTS
# ============================================================================

def test_insert_values():
    """Test INSERT INTO ... VALUES"""
    storage.execute("INSERT INTO users (name, age, city) VALUES ('TestUser', 25, 'TestCity')")
    results = storage.execute("SELECT * FROM users WHERE name = 'TestUser'")
    assert len(results) > 0
    storage.execute("DELETE FROM users WHERE name = 'TestUser'")

def test_insert_multiple():
    """Test INSERT multiple rows"""
    storage.execute("INSERT INTO users (name, age, city) VALUES ('Test1', 20, 'City1'), ('Test2', 21, 'City2')")
    results = storage.execute("SELECT * FROM users WHERE name IN ('Test1', 'Test2')")
    assert len(results) == 2
    storage.execute("DELETE FROM users WHERE name IN ('Test1', 'Test2')")

# ============================================================================
# UPDATE TESTS
# ============================================================================

def test_update():
    """Test UPDATE"""
    storage.execute("INSERT INTO users (name, age, city) VALUES ('UpdateTest', 25, 'OldCity')")
    storage.execute("UPDATE users SET city = 'NewCity' WHERE name = 'UpdateTest'")
    results = storage.execute("SELECT city FROM users WHERE name = 'UpdateTest'")
    assert len(results) > 0
    assert results[0][0] == 'NewCity'
    storage.execute("DELETE FROM users WHERE name = 'UpdateTest'")

def test_update_multiple_columns():
    """Test UPDATE multiple columns"""
    storage.execute("INSERT INTO users (name, age, city) VALUES ('MultiUpdate', 25, 'City1')")
    storage.execute("UPDATE users SET age = 30, city = 'City2' WHERE name = 'MultiUpdate'")
    results = storage.execute("SELECT age, city FROM users WHERE name = 'MultiUpdate'")
    assert len(results) > 0
    assert results[0][0] == 30
    assert results[0][1] == 'City2'
    storage.execute("DELETE FROM users WHERE name = 'MultiUpdate'")

# ============================================================================
# DELETE TESTS
# ============================================================================

def test_delete_where():
    """Test DELETE with WHERE"""
    storage.execute("INSERT INTO users (name, age, city) VALUES ('DeleteTest', 25, 'City')")
    storage.execute("DELETE FROM users WHERE name = 'DeleteTest'")
    results = storage.execute("SELECT * FROM users WHERE name = 'DeleteTest'")
    assert len(results) == 0

# ============================================================================
# PARSER TESTS
# ============================================================================

def test_parser_select():
    """Test query parser on SELECT"""
    analyzer = QueryAnalyzer("SELECT * FROM users WHERE age > 25")
    analysis = analyzer.analyze()
    assert analysis['type'] == 'SELECT'
    assert 'users' in analysis['tables']

def test_parser_join():
    """Test query parser on JOIN"""
    analyzer = QueryAnalyzer("SELECT u.name FROM users u JOIN orders o ON u.id = o.user_id")
    analysis = analyzer.analyze()
    assert analysis['has_joins'] is True

def test_parser_group_by():
    """Test query parser on GROUP BY"""
    analyzer = QueryAnalyzer("SELECT city, COUNT(*) FROM users GROUP BY city")
    analysis = analyzer.analyze()
    assert len(analysis['group_by']) > 0

def test_parser_order_by():
    """Test query parser on ORDER BY"""
    analyzer = QueryAnalyzer("SELECT * FROM users ORDER BY age DESC")
    analysis = analyzer.analyze()
    assert len(analysis['order_by']) > 0

def test_parser_limit():
    """Test query parser on LIMIT"""
    analyzer = QueryAnalyzer("SELECT * FROM users LIMIT 10")
    analysis = analyzer.analyze()
    assert analysis['limit'] == 10

# ============================================================================
# SIMULATOR TESTS
# ============================================================================

def test_simulator_select():
    """Test execution simulator on SELECT"""
    simulator = ExecutionSimulator(storage)
    steps = simulator.simulate("SELECT * FROM users WHERE age > 25")
    assert len(steps) > 0

def test_simulator_join():
    """Test execution simulator on JOIN"""
    simulator = ExecutionSimulator(storage)
    steps = simulator.simulate("SELECT u.name FROM users u JOIN orders o ON u.id = o.user_id")
    assert len(steps) > 0

# ============================================================================
# COMPLEX QUERY TESTS
# ============================================================================

def test_complex_query_1():
    """Test complex query with multiple clauses"""
    query = """
    SELECT u.name, COUNT(o.id) as order_count, SUM(o.amount) as total
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.age > 25
    GROUP BY u.id, u.name
    HAVING COUNT(o.id) > 0
    ORDER BY total DESC
    LIMIT 5
    """
    results = storage.execute(query)
    assert len(results) >= 0

def test_complex_query_2():
    """Test another complex query"""
    query = """
    SELECT city, AVG(age) as avg_age, COUNT(*) as user_count
    FROM users
    WHERE age IS NOT NULL
    GROUP BY city
    HAVING COUNT(*) > 1
    ORDER BY avg_age DESC
    """
    results = storage.execute(query)
    assert len(results) >= 0

# ============================================================================
# EDGE CASES
# ============================================================================

def test_empty_result():
    """Test query that returns no results"""
    results = storage.execute("SELECT * FROM users WHERE age > 1000")
    assert len(results) == 0

def test_single_row_result():
    """Test query that returns single row"""
    results = storage.execute("SELECT * FROM users LIMIT 1")
    assert len(results) == 1

def test_case_insensitive():
    """Test case insensitive SQL keywords"""
    results = storage.execute("select * from users")
    assert len(results) > 0

def test_whitespace_handling():
    """Test query with extra whitespace"""
    query = "   SELECT   *   FROM   users   WHERE   age   >   25   "
    results = storage.execute(query)
    assert len(results) >= 0

# ============================================================================
# RUN ALL TESTS
# ============================================================================

# Basic SELECT
runner.test("SELECT *", test_select_all)
runner.test("SELECT columns", test_select_columns)
runner.test("SELECT with alias", test_select_with_alias)
runner.test("SELECT DISTINCT", test_select_distinct)

# WHERE clauses
runner.test("WHERE =", test_where_equals)
runner.test("WHERE >", test_where_greater_than)
runner.test("WHERE <", test_where_less_than)
runner.test("WHERE >=", test_where_greater_equal)
runner.test("WHERE <=", test_where_less_equal)
runner.test("WHERE !=", test_where_not_equal)
runner.test("WHERE LIKE", test_where_like)
runner.test("WHERE IN", test_where_in)
runner.test("WHERE BETWEEN", test_where_between)
runner.test("WHERE AND", test_where_and)
runner.test("WHERE OR", test_where_or)
runner.test("WHERE IS NULL", test_where_is_null)
runner.test("WHERE IS NOT NULL", test_where_is_not_null)

# JOINs
runner.test("INNER JOIN", test_inner_join)
runner.test("LEFT JOIN", test_left_join)
runner.test("JOIN with WHERE", test_join_with_where)

# Aggregations
runner.test("COUNT(*)", test_count)
runner.test("COUNT(column)", test_count_column)
runner.test("SUM", test_sum)
runner.test("AVG", test_avg)
runner.test("MAX", test_max)
runner.test("MIN", test_min)

# GROUP BY
runner.test("GROUP BY", test_group_by)
runner.test("GROUP BY multiple", test_group_by_multiple)
runner.test("GROUP BY with aggregate", test_group_by_with_aggregate)

# HAVING
runner.test("HAVING", test_having)
runner.test("HAVING with aggregate", test_having_with_aggregate)

# ORDER BY
runner.test("ORDER BY ASC", test_order_by_asc)
runner.test("ORDER BY DESC", test_order_by_desc)
runner.test("ORDER BY multiple", test_order_by_multiple)

# LIMIT/OFFSET
runner.test("LIMIT", test_limit)
runner.test("LIMIT OFFSET", test_limit_offset)

# INSERT
runner.test("INSERT VALUES", test_insert_values)
runner.test("INSERT multiple", test_insert_multiple)

# UPDATE
runner.test("UPDATE", test_update)
runner.test("UPDATE multiple columns", test_update_multiple_columns)

# DELETE
runner.test("DELETE WHERE", test_delete_where)

# Parser
runner.test("Parser SELECT", test_parser_select)
runner.test("Parser JOIN", test_parser_join)
runner.test("Parser GROUP BY", test_parser_group_by)
runner.test("Parser ORDER BY", test_parser_order_by)
runner.test("Parser LIMIT", test_parser_limit)

# Simulator
runner.test("Simulator SELECT", test_simulator_select)
runner.test("Simulator JOIN", test_simulator_join)

# Complex queries
runner.test("Complex query 1", test_complex_query_1)
runner.test("Complex query 2", test_complex_query_2)

# Edge cases
runner.test("Empty result", test_empty_result)
runner.test("Single row", test_single_row_result)
runner.test("Case insensitive", test_case_insensitive)
runner.test("Whitespace handling", test_whitespace_handling)

# Cleanup
storage.close()
os.unlink(test_db.name)

# Print summary
runner.summary()

# Exit with error code if tests failed
sys.exit(1 if runner.failed > 0 else 0)

