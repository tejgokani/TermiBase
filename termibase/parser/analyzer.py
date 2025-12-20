"""SQL parser and query analyzer."""

import sqlparse
from sqlparse.sql import Statement, TokenList
from sqlparse.tokens import Keyword, DML, Name, Comparison
from typing import Dict, List, Optional, Set, Tuple
import re


class QueryAnalyzer:
    """Analyzes SQL queries to extract structure and metadata."""

    def __init__(self, query: str):
        """Initialize analyzer with a SQL query.
        
        Args:
            query: SQL query string
        """
        self.query = query.strip()
        self.parsed = sqlparse.parse(self.query)[0] if self.query else None

    def get_query_type(self) -> str:
        """Determine the type of SQL query.
        
        Returns:
            Query type (SELECT, INSERT, UPDATE, DELETE, CREATE, etc.)
        """
        if not self.parsed:
            return "UNKNOWN"
        
        first_token = self.parsed.token_first()
        if first_token and first_token.ttype is DML:
            return first_token.value.upper()
        elif first_token and first_token.ttype is Keyword:
            return first_token.value.upper()
        
        return "UNKNOWN"

    def get_tables(self) -> List[str]:
        """Extract table names from the query.
        
        Returns:
            List of table names referenced in the query
        """
        tables = set()
        
        if not self.parsed:
            return list(tables)
        
        # Look for FROM and JOIN clauses using regex for better accuracy
        query_upper = self.query.upper()
        
        # Extract tables from FROM clause
        from_match = re.search(r'FROM\s+(\w+)(?:\s+\w+)?(?:\s*,|\s+WHERE|\s+GROUP|\s+ORDER|\s+HAVING|\s+JOIN|\s+INNER|\s+LEFT|\s+RIGHT|\s+FULL|\s+OUTER|\s+LIMIT|$)', query_upper)
        if from_match:
            table_name = from_match.group(1).lower()
            if table_name:
                tables.add(table_name)
        
        # Extract tables from JOIN clauses
        join_pattern = r'(?:INNER|LEFT|RIGHT|FULL|OUTER)?\s+JOIN\s+(\w+)(?:\s+\w+)?(?:\s+ON|\s+WHERE|\s+GROUP|\s+ORDER|\s+HAVING|\s+LIMIT|$)'
        for match in re.finditer(join_pattern, query_upper, re.IGNORECASE):
            table_name = match.group(1).lower()
            if table_name:
                tables.add(table_name)
        
        # Also check INSERT INTO, UPDATE, DELETE FROM
        query_upper = self.query.upper()
        if 'INSERT INTO' in query_upper:
            match = re.search(r'INSERT\s+INTO\s+(\w+)', query_upper)
            if match:
                tables.add(match.group(1))
        elif 'UPDATE' in query_upper:
            match = re.search(r'UPDATE\s+(\w+)', query_upper)
            if match:
                tables.add(match.group(1))
        elif 'DELETE FROM' in query_upper:
            match = re.search(r'DELETE\s+FROM\s+(\w+)', query_upper)
            if match:
                tables.add(match.group(1))
        
        return sorted(list(tables))

    def get_columns(self) -> List[str]:
        """Extract column names from SELECT clause.
        
        Returns:
            List of column names
        """
        columns = []
        
        if not self.parsed or self.get_query_type() != 'SELECT':
            return columns
        
        # Find SELECT clause
        in_select = False
        select_tokens = []
        
        for token in self.parsed.flatten():
            if token.ttype is DML and token.value.upper() == 'SELECT':
                in_select = True
                continue
            
            if in_select:
                if token.ttype is Keyword and token.value.upper() == 'FROM':
                    break
                select_tokens.append(token)
        
        # Parse column names from SELECT tokens
        select_str = ' '.join(t.value for t in select_tokens)
        if select_str.strip() == '*':
            return ['*']
        
        # Split by comma and extract column names
        for col in select_str.split(','):
            col = col.strip()
            # Remove aliases (AS alias)
            if ' AS ' in col.upper():
                col = col.split(' AS ')[0].strip()
            elif ' ' in col and not col.startswith('('):
                # Might be an alias without AS
                parts = col.split()
                if len(parts) >= 2 and parts[-1] not in ('DISTINCT', 'ALL'):
                    col = parts[0]
            
            # Clean up
            col = col.strip('`"[]')
            if col and col.upper() not in ('DISTINCT', 'ALL'):
                columns.append(col)
        
        return columns

    def get_where_conditions(self) -> List[str]:
        """Extract WHERE clause conditions.
        
        Returns:
            List of condition strings
        """
        conditions = []
        
        if not self.parsed:
            return conditions
        
        in_where = False
        where_tokens = []
        
        for token in self.parsed.flatten():
            if token.ttype is Keyword and token.value.upper() == 'WHERE':
                in_where = True
                continue
            
            if in_where:
                if token.ttype is Keyword and token.value.upper() in ('GROUP', 'ORDER', 'HAVING', 'LIMIT'):
                    break
                where_tokens.append(token)
        
        if where_tokens:
            condition_str = ' '.join(t.value for t in where_tokens)
            # Split by AND/OR (simplified)
            conditions = [c.strip() for c in re.split(r'\s+(?:AND|OR)\s+', condition_str, flags=re.IGNORECASE)]
        
        return conditions

    def has_joins(self) -> bool:
        """Check if query contains JOIN operations.
        
        Returns:
            True if query has joins
        """
        if not self.parsed:
            return False
        
        query_upper = self.query.upper()
        return any(keyword in query_upper for keyword in ['JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN'])

    def get_join_info(self) -> List[Dict[str, str]]:
        """Extract JOIN information.
        
        Returns:
            List of join dictionaries with type and tables
        """
        joins = []
        
        if not self.has_joins():
            return joins
        
        # Simple regex-based extraction
        join_pattern = r'(\w+\s+)?JOIN\s+(\w+)'
        matches = re.finditer(join_pattern, self.query, re.IGNORECASE)
        
        for match in matches:
            join_type = match.group(1).strip().upper() if match.group(1) else 'INNER'
            table = match.group(2).strip()
            joins.append({'type': join_type, 'table': table})
        
        return joins

    def get_order_by(self) -> List[str]:
        """Extract ORDER BY columns.
        
        Returns:
            List of columns in ORDER BY clause
        """
        columns = []
        
        if not self.parsed:
            return columns
        
        query_upper = self.query.upper()
        if 'ORDER BY' not in query_upper:
            return columns
        
        match = re.search(r'ORDER\s+BY\s+(.+?)(?:\s+(?:LIMIT|GROUP|HAVING)|$)', query_upper, re.IGNORECASE)
        if match:
            order_clause = match.group(1).strip()
            columns = [col.strip().split()[0] for col in order_clause.split(',')]
        
        return columns

    def get_group_by(self) -> List[str]:
        """Extract GROUP BY columns.
        
        Returns:
            List of columns in GROUP BY clause
        """
        columns = []
        
        if not self.parsed:
            return columns
        
        query_upper = self.query.upper()
        if 'GROUP BY' not in query_upper:
            return columns
        
        match = re.search(r'GROUP\s+BY\s+(.+?)(?:\s+(?:ORDER|HAVING|LIMIT)|$)', query_upper, re.IGNORECASE)
        if match:
            group_clause = match.group(1).strip()
            columns = [col.strip().split()[0] for col in group_clause.split(',')]
        
        return columns

    def get_limit(self) -> Optional[int]:
        """Extract LIMIT value.
        
        Returns:
            LIMIT value or None
        """
        query_upper = self.query.upper()
        match = re.search(r'LIMIT\s+(\d+)', query_upper)
        if match:
            return int(match.group(1))
        return None

    def analyze(self) -> Dict:
        """Perform complete query analysis.
        
        Returns:
            Dictionary with all analysis results
        """
        return {
            'type': self.get_query_type(),
            'tables': self.get_tables(),
            'columns': self.get_columns(),
            'where_conditions': self.get_where_conditions(),
            'has_joins': self.has_joins(),
            'joins': self.get_join_info(),
            'order_by': self.get_order_by(),
            'group_by': self.get_group_by(),
            'limit': self.get_limit(),
        }

