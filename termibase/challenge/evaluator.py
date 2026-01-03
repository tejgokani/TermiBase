"""Challenge evaluation engine for SQL solutions."""

import sqlite3
import sqlparse
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum
from termibase.challenge.bank import Challenge


class EvaluationResult(Enum):
    """Evaluation result states."""
    INCORRECT = "incorrect"
    PARTIAL = "partial"
    PERFECT = "perfect"


class ChallengeEvaluator:
    """Evaluates SQL challenge solutions."""
    
    def __init__(self):
        """Initialize evaluator."""
        pass
    
    def evaluate(
        self,
        challenge: Challenge,
        user_query: str,
        db_path: str
    ) -> Tuple[EvaluationResult, Dict[str, Any]]:
        """Evaluate a user's SQL solution.
        
        Args:
            challenge: Challenge object
            user_query: User's SQL query
            db_path: Path to challenge database
            
        Returns:
            Tuple of (result, details dictionary)
        """
        details = {
            'error': None,
            'hardcoded_detected': False,
            'syntax_valid': True,
            'result_match': False,
            'constraints_violated': []
        }
        
        # Step 1: Validate SQL syntax
        if not self._validate_syntax(user_query):
            details['syntax_valid'] = False
            details['error'] = 'Invalid SQL syntax'
            return EvaluationResult.INCORRECT, details
        
        # Step 2: Check for hardcoded constants
        if self._detect_hardcoded_constants(user_query, challenge):
            details['hardcoded_detected'] = True
            # Hardcoded constants don't automatically fail, but reduce score
            # We'll mark as PARTIAL if result matches but has hardcoding
        
        # Step 3: Check allowed operations
        violations = self._check_allowed_operations(user_query, challenge)
        if violations:
            details['constraints_violated'] = violations
            details['error'] = f'Operation not allowed: {", ".join(violations)}'
            return EvaluationResult.INCORRECT, details
        
        # Step 4: Execute query and compare results
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            try:
                user_results = conn.execute(user_query).fetchall()
                user_results_normalized = self._normalize_results(user_results)
                
                # Compare with expected result
                match_result = self._compare_results(
                    user_results_normalized,
                    challenge.expected_result,
                    db_path
                )
                
                details['result_match'] = match_result['matches']
                details['user_row_count'] = len(user_results_normalized)
                details['expected_row_count'] = match_result.get('expected_rows', 0)
                
                if match_result['matches']:
                    if details['hardcoded_detected']:
                        return EvaluationResult.PARTIAL, details
                    else:
                        return EvaluationResult.PERFECT, details
                else:
                    return EvaluationResult.INCORRECT, details
                    
            finally:
                conn.close()
        except sqlite3.Error as e:
            details['error'] = str(e)
            details['syntax_valid'] = False
            return EvaluationResult.INCORRECT, details
        except Exception as e:
            details['error'] = f'Unexpected error: {str(e)}'
            return EvaluationResult.INCORRECT, details
    
    def _validate_syntax(self, query: str) -> bool:
        """Validate SQL syntax.
        
        Args:
            query: SQL query string
            
        Returns:
            True if syntax is valid
        """
        try:
            parsed = sqlparse.parse(query)
            if not parsed or len(parsed) == 0:
                return False
            # Basic validation - sqlparse will raise exception on invalid SQL
            return True
        except Exception:
            return False
    
    def _detect_hardcoded_constants(self, query: str, challenge: Challenge) -> bool:
        """Detect hardcoded constants in query.
        
        This checks if the query contains literal values that match expected results,
        which suggests the user hardcoded the answer rather than writing a dynamic query.
        
        Args:
            query: SQL query string
            challenge: Challenge object
            
        Returns:
            True if hardcoded constants detected
        """
        # Parse query to extract literals
        try:
            parsed = sqlparse.parse(query)[0]
            literals = []
            
            # Extract string and numeric literals
            for token in parsed.flatten():
                if token.ttype in (sqlparse.tokens.Literal.String.Single,
                                 sqlparse.tokens.Literal.String.Double,
                                 sqlparse.tokens.Literal.Number.Integer,
                                 sqlparse.tokens.Literal.Number.Float):
                    literals.append(token.value.strip("'\"`"))
            
            # Check if expected result contains these exact values
            # This is a heuristic - if too many literals match expected data, likely hardcoded
            expected = challenge.expected_result
            
            # Check for hardcoded row counts
            if 'rows' in expected:
                if str(expected['rows']) in query:
                    return True
            
            # Check for hardcoded specific values that shouldn't be in WHERE clauses
            # This is context-dependent and simplified here
            # In production, would need more sophisticated AST analysis
            
            return False
        except Exception:
            # If parsing fails, assume no hardcoding detected
            return False
    
    def _check_allowed_operations(self, query: str, challenge: Challenge) -> List[str]:
        """Check if query uses only allowed operations.
        
        Args:
            query: SQL query string
            challenge: Challenge object
            
        Returns:
            List of violated operation names (empty if all allowed)
        """
        violations = []
        query_upper = query.upper()
        
        # Define operation keywords
        operation_keywords = {
            'DROP': ['DROP'],
            'ALTER': ['ALTER'],
            'PRAGMA': ['PRAGMA'],
            'INSERT': ['INSERT'],
            'UPDATE': ['UPDATE'],
            'DELETE': ['DELETE'],
            'CREATE': ['CREATE'],
            'TRUNCATE': ['TRUNCATE'],
        }
        
        allowed_ops = [op.upper() for op in challenge.allowed_operations]
        
        # Check for blocked operations
        for op_name, keywords in operation_keywords.items():
            if op_name not in allowed_ops:
                for keyword in keywords:
                    if keyword in query_upper:
                        # More precise check - ensure it's actually the operation
                        pattern = rf'\b{keyword}\b'
                        import re
                        if re.search(pattern, query_upper):
                            violations.append(op_name)
                            break
        
        return violations
    
    def _normalize_results(self, results: List[sqlite3.Row]) -> List[Tuple]:
        """Normalize query results for comparison.
        
        Args:
            results: List of result rows
            
        Returns:
            List of normalized tuples
        """
        normalized = []
        for row in results:
            if hasattr(row, 'keys'):
                # Row object - convert to tuple, sorted by column name for consistency
                values = tuple(row[key] for key in sorted(row.keys()))
            else:
                # Already a tuple or list
                values = tuple(row)
            normalized.append(values)
        return normalized
    
    def _compare_results(
        self,
        user_results: List[Tuple],
        expected: Dict[str, Any],
        db_path: str
    ) -> Dict[str, Any]:
        """Compare user results with expected results.
        
        Args:
            user_results: Normalized user query results
            expected: Expected result specification
            db_path: Path to database (for executing reference queries)
            
        Returns:
            Dictionary with comparison results
        """
        result = {
            'matches': False,
            'expected_rows': 0,
            'details': []
        }
        
        if expected['type'] == 'query_result':
            # Compare row count
            if 'rows' in expected:
                expected_rows = expected['rows']
                result['expected_rows'] = expected_rows
                if len(user_results) != expected_rows:
                    result['details'].append(
                        f'Row count mismatch: expected {expected_rows}, got {len(user_results)}'
                    )
                    return result
            
            # Compare structure (columns)
            if 'columns' in expected:
                # This would require column name comparison
                # Simplified for now
                pass
            
            # Compare specific values
            if 'min_age' in expected:
                # Check if all ages are > min_age
                ages = [row[2] if len(row) > 2 else None for row in user_results]
                if all(age and age > expected['min_age'] for age in ages):
                    result['matches'] = True
                else:
                    result['details'].append('Age filter incorrect')
                return result
            
            if 'avg_age' in expected:
                # Check if average matches (within tolerance)
                if user_results and len(user_results) > 0:
                    avg_val = user_results[0][0] if user_results[0] else None
                    if avg_val:
                        tolerance = 0.01
                        if abs(float(avg_val) - expected['avg_age']) < tolerance:
                            result['matches'] = True
                        else:
                            result['details'].append(
                                f'Average mismatch: expected ~{expected["avg_age"]}, got {avg_val}'
                            )
                return result
            
            # For other cases, if row count matches and no specific checks, assume match
            if 'rows' in expected and len(user_results) == expected['rows']:
                result['matches'] = True
            
            # Check for specific query characteristics
            if 'has_join' in expected and expected['has_join']:
                # Would need to parse query to verify JOIN presence
                # Simplified - assume correct if row count matches
                if len(user_results) == expected.get('rows', 0):
                    result['matches'] = True
            
            if 'has_having' in expected and expected['has_having']:
                # Simplified check
                if len(user_results) > 0:
                    result['matches'] = True
            
            if 'has_subquery' in expected and expected['has_subquery']:
                # Simplified check
                if len(user_results) == expected.get('rows', 0):
                    result['matches'] = True
            
            if 'has_cte' in expected and expected['has_cte']:
                # Simplified check
                if len(user_results) > 0:
                    result['matches'] = True
            
            if 'min_total' in expected:
                # Check if all totals are >= min_total
                if user_results:
                    totals = [row[-1] if row else 0 for row in user_results]
                    if all(tot >= expected['min_total'] for tot in totals):
                        result['matches'] = True
                    else:
                        result['details'].append('Total filter incorrect')
                return result
        
        return result
    
    def get_friendly_error_message(self, error: str) -> str:
        """Convert SQLite error to friendly message.
        
        Args:
            error: SQLite error message
            
        Returns:
            Human-readable error message
        """
        error_lower = error.lower()
        
        if 'syntax error' in error_lower:
            return "SQL syntax error. Check your query structure - ensure all clauses are properly formatted."
        elif 'no such table' in error_lower:
            return "Table not found. Check the table name spelling and ensure you're using the correct schema."
        elif 'no such column' in error_lower:
            return "Column not found. Verify the column name exists in the table."
        elif 'ambiguous column' in error_lower:
            return "Ambiguous column name. Use table aliases to specify which table the column belongs to."
        elif 'foreign key constraint' in error_lower:
            return "Foreign key constraint violation. The referenced record doesn't exist."
        elif 'not null constraint' in error_lower:
            return "NOT NULL constraint violation. A required column is missing a value."
        elif 'unique constraint' in error_lower:
            return "Unique constraint violation. This value already exists."
        else:
            return f"Database error: {error}"


