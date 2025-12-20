"""Tests for query analyzer."""

import pytest
from termibase.parser.analyzer import QueryAnalyzer


def test_select_query():
    """Test basic SELECT query analysis."""
    analyzer = QueryAnalyzer("SELECT * FROM users")
    analysis = analyzer.analyze()
    
    assert analysis['type'] == 'SELECT'
    assert 'users' in analysis['tables']
    assert analysis['columns'] == ['*']


def test_select_with_where():
    """Test SELECT with WHERE clause."""
    analyzer = QueryAnalyzer("SELECT name, age FROM users WHERE age > 25")
    analysis = analyzer.analyze()
    
    assert analysis['type'] == 'SELECT'
    assert 'users' in analysis['tables']
    assert 'name' in analysis['columns']
    assert 'age' in analysis['columns']
    assert len(analysis['where_conditions']) > 0


def test_join_query():
    """Test JOIN query analysis."""
    analyzer = QueryAnalyzer(
        "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id"
    )
    analysis = analyzer.analyze()
    
    assert analysis['type'] == 'SELECT'
    assert 'users' in analysis['tables']
    assert 'orders' in analysis['tables']
    assert analysis['has_joins'] is True
    assert len(analysis['joins']) > 0


def test_group_by():
    """Test GROUP BY analysis."""
    analyzer = QueryAnalyzer(
        "SELECT city, COUNT(*) FROM users GROUP BY city"
    )
    analysis = analyzer.analyze()
    
    assert 'city' in analysis['group_by']


def test_order_by():
    """Test ORDER BY analysis."""
    analyzer = QueryAnalyzer(
        "SELECT * FROM users ORDER BY age DESC"
    )
    analysis = analyzer.analyze()
    
    assert 'age' in analysis['order_by']


def test_limit():
    """Test LIMIT analysis."""
    analyzer = QueryAnalyzer(
        "SELECT * FROM users LIMIT 10"
    )
    analysis = analyzer.analyze()
    
    assert analysis['limit'] == 10

