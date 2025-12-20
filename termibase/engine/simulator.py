"""Query execution simulator."""

from typing import Dict, List, Any, Optional
from termibase.parser.analyzer import QueryAnalyzer
from termibase.storage.engine import StorageEngine


class ExecutionStep:
    """Represents a single step in query execution."""
    
    def __init__(self, step_type: str, description: str, cost: float = 0.0, 
                 rows_processed: int = 0, details: Optional[Dict] = None):
        self.step_type = step_type
        self.description = description
        self.cost = cost
        self.rows_processed = rows_processed
        self.details = details or {}

    def __repr__(self):
        return f"ExecutionStep({self.step_type}, {self.description})"


class ExecutionSimulator:
    """Simulates query execution step by step."""

    def __init__(self, storage: StorageEngine):
        """Initialize simulator with storage engine.
        
        Args:
            storage: Storage engine instance
        """
        self.storage = storage

    def simulate(self, query: str) -> List[ExecutionStep]:
        """Simulate query execution and return steps.
        
        Args:
            query: SQL query string
            
        Returns:
            List of execution steps
        """
        analyzer = QueryAnalyzer(query)
        analysis = analyzer.analyze()
        steps = []
        
        query_type = analysis['type']
        
        if query_type == 'SELECT':
            steps = self._simulate_select(analysis)
        elif query_type == 'INSERT':
            steps = self._simulate_insert(analysis)
        elif query_type == 'UPDATE':
            steps = self._simulate_update(analysis)
        elif query_type == 'DELETE':
            steps = self._simulate_delete(analysis)
        else:
            steps.append(ExecutionStep(
                'UNKNOWN',
                f"Executing {query_type} query",
                cost=1.0
            ))
        
        return steps

    def _simulate_select(self, analysis: Dict) -> List[ExecutionStep]:
        """Simulate SELECT query execution.
        
        Args:
            analysis: Query analysis results
            
        Returns:
            List of execution steps
        """
        steps = []
        tables = analysis['tables']
        
        if not tables:
            return steps
        
        # Step 1: Table scan or index scan
        for table in tables:
            # Check if there are indexes
            indexes = self.storage.get_indexes(table)
            has_indexes = len(indexes) > 0
            
            # Check if WHERE conditions can use indexes
            where_conditions = analysis['where_conditions']
            can_use_index = has_indexes and where_conditions
            
            if can_use_index:
                steps.append(ExecutionStep(
                    'INDEX_SCAN',
                    f"Scanning index on {table}",
                    cost=0.5,
                    rows_processed=self._estimate_rows(table, where_conditions),
                    details={'table': table, 'index_used': True}
                ))
            else:
                steps.append(ExecutionStep(
                    'TABLE_SCAN',
                    f"Scanning table {table}",
                    cost=1.0,
                    rows_processed=self._estimate_rows(table, None),
                    details={'table': table, 'index_used': False}
                ))
        
        # Step 2: JOIN operations
        if analysis['has_joins']:
            for join in analysis['joins']:
                steps.append(ExecutionStep(
                    'JOIN',
                    f"Performing {join['type']} JOIN with {join['table']}",
                    cost=0.8,
                    rows_processed=self._estimate_join_rows(),
                    details={'join_type': join['type'], 'table': join['table']}
                ))
        
        # Step 3: WHERE filter
        if analysis['where_conditions']:
            steps.append(ExecutionStep(
                'FILTER',
                f"Applying WHERE filter: {', '.join(analysis['where_conditions'])}",
                cost=0.3,
                rows_processed=self._estimate_filtered_rows(),
                details={'conditions': analysis['where_conditions']}
            ))
        
        # Step 4: GROUP BY
        if analysis['group_by']:
            steps.append(ExecutionStep(
                'GROUP',
                f"Grouping by: {', '.join(analysis['group_by'])}",
                cost=0.5,
                rows_processed=self._estimate_grouped_rows(),
                details={'columns': analysis['group_by']}
            ))
        
        # Step 5: ORDER BY
        if analysis['order_by']:
            steps.append(ExecutionStep(
                'SORT',
                f"Sorting by: {', '.join(analysis['order_by'])}",
                cost=0.6,
                rows_processed=self._estimate_sorted_rows(),
                details={'columns': analysis['order_by']}
            ))
        
        # Step 6: LIMIT
        if analysis['limit']:
            steps.append(ExecutionStep(
                'LIMIT',
                f"Applying LIMIT {analysis['limit']}",
                cost=0.1,
                rows_processed=analysis['limit'],
                details={'limit': analysis['limit']}
            ))
        
        # Step 7: Projection (SELECT columns)
        steps.append(ExecutionStep(
            'PROJECT',
            f"Projecting columns: {', '.join(analysis['columns']) if analysis['columns'] else '*'}"
            if analysis['columns'] != ['*'] else "Projecting all columns",
            cost=0.2,
            rows_processed=self._estimate_final_rows(),
            details={'columns': analysis['columns']}
        ))
        
        return steps

    def _simulate_insert(self, analysis: Dict) -> List[ExecutionStep]:
        """Simulate INSERT query execution."""
        steps = []
        tables = analysis['tables']
        
        if tables:
            steps.append(ExecutionStep(
                'INSERT',
                f"Inserting row into {tables[0]}",
                cost=0.3,
                rows_processed=1,
                details={'table': tables[0]}
            ))
        
        return steps

    def _simulate_update(self, analysis: Dict) -> List[ExecutionStep]:
        """Simulate UPDATE query execution."""
        steps = []
        tables = analysis['tables']
        
        if tables:
            steps.append(ExecutionStep(
                'TABLE_SCAN',
                f"Scanning table {tables[0]} for matching rows",
                cost=1.0,
                rows_processed=self._estimate_rows(tables[0], analysis['where_conditions']),
                details={'table': tables[0]}
            ))
            
            if analysis['where_conditions']:
                steps.append(ExecutionStep(
                    'FILTER',
                    f"Filtering rows: {', '.join(analysis['where_conditions'])}",
                    cost=0.3,
                    rows_processed=self._estimate_filtered_rows(),
                    details={'conditions': analysis['where_conditions']}
                ))
            
            steps.append(ExecutionStep(
                'UPDATE',
                f"Updating matching rows in {tables[0]}",
                cost=0.5,
                rows_processed=self._estimate_filtered_rows(),
                details={'table': tables[0]}
            ))
        
        return steps

    def _simulate_delete(self, analysis: Dict) -> List[ExecutionStep]:
        """Simulate DELETE query execution."""
        steps = []
        tables = analysis['tables']
        
        if tables:
            steps.append(ExecutionStep(
                'TABLE_SCAN',
                f"Scanning table {tables[0]} for matching rows",
                cost=1.0,
                rows_processed=self._estimate_rows(tables[0], analysis['where_conditions']),
                details={'table': tables[0]}
            ))
            
            if analysis['where_conditions']:
                steps.append(ExecutionStep(
                    'FILTER',
                    f"Filtering rows: {', '.join(analysis['where_conditions'])}",
                    cost=0.3,
                    rows_processed=self._estimate_filtered_rows(),
                    details={'conditions': analysis['where_conditions']}
                ))
            
            steps.append(ExecutionStep(
                'DELETE',
                f"Deleting matching rows from {tables[0]}",
                cost=0.5,
                rows_processed=self._estimate_filtered_rows(),
                details={'table': tables[0]}
            ))
        
        return steps

    def _estimate_rows(self, table: str, conditions: Optional[List[str]]) -> int:
        """Estimate number of rows in a table.
        
        Args:
            table: Table name
            conditions: Optional WHERE conditions
            
        Returns:
            Estimated row count
        """
        try:
            result = self.storage.execute(f"SELECT COUNT(*) FROM {table}")
            total_rows = result[0][0] if result else 100
            
            # If there are conditions, estimate filtered rows
            if conditions:
                # Simple heuristic: assume 30% of rows match
                return max(1, int(total_rows * 0.3))
            
            return total_rows
        except:
            return 100  # Default estimate

    def _estimate_join_rows(self) -> int:
        """Estimate rows after join."""
        return 50

    def _estimate_filtered_rows(self) -> int:
        """Estimate rows after filtering."""
        return 30

    def _estimate_grouped_rows(self) -> int:
        """Estimate rows after grouping."""
        return 10

    def _estimate_sorted_rows(self) -> int:
        """Estimate rows after sorting."""
        return 25

    def _estimate_final_rows(self) -> int:
        """Estimate final result rows."""
        return 20

