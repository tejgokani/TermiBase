"""Query execution visualization using Rich."""

from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
from rich.syntax import Syntax
from termibase.engine.simulator import ExecutionStep


class QueryVisualizer:
    """Visualizes execution plans and results.

    Note: Query structure analysis has been removed to keep output minimal and
    closer to a traditional SQL*Plus-style experience.
    """

    def __init__(self):
        """Initialize visualizer."""
        self.console = Console()
        # Get terminal width, with fallback
        try:
            self.terminal_width = self.console.width
        except:
            self.terminal_width = 80

    def show_query_analysis(self, query: str) -> None:
        """Previously displayed query analysis.

        This method is now a no-op to disable the visual \"Query Analysis\"
        panel and table while keeping the public API stable.
        """
        return

    def show_execution_plan(self, steps: List[ExecutionStep]) -> None:
        """Display execution plan as a tree.
        
        Args:
            steps: List of execution steps
        """
        self.console.print("\n[bold yellow]Execution Plan[/bold yellow]")
        
        tree = Tree("Query Execution")
        
        total_cost = sum(step.cost for step in steps)
        
        for i, step in enumerate(steps, 1):
            step_label = f"[{i}] {step.step_type}"
            step_text = Text(step_label)
            step_text.append(f" - {step.description}", style="dim")
            step_text.append(f" (cost: {step.cost:.2f}, rows: {step.rows_processed})", 
                           style="yellow")
            
            branch = tree.add(step_text)
            
            # Add details if available
            if step.details:
                for key, value in step.details.items():
                    if isinstance(value, list):
                        value = ", ".join(str(v) for v in value)
                    branch.add(f"{key}: {value}")
        
        self.console.print(tree)
        self.console.print(f"\n[bold]Total Estimated Cost:[/bold] {total_cost:.2f}")

    def show_execution_steps(self, steps: List[ExecutionStep]) -> None:
        """Display execution steps in a table.
        
        Args:
            steps: List of execution steps
        """
        self.console.print("\n[bold green]Execution Steps[/bold green]")
        
        safe_width = min(self.terminal_width - 4, 120)
        table = Table(show_header=True, header_style="bold magenta", width=safe_width, show_lines=False)
        table.add_column("Step", style="cyan", width=6, overflow="fold")
        table.add_column("Operation", style="green", width=12, overflow="fold")
        table.add_column("Description", style="white", overflow="fold")
        table.add_column("Cost", style="yellow", justify="right", width=8)
        table.add_column("Rows", style="blue", justify="right", width=8)
        
        for i, step in enumerate(steps, 1):
            table.add_row(
                str(i),
                step.step_type,
                step.description,
                f"{step.cost:.2f}",
                str(step.rows_processed)
            )
        
        self.console.print(table)
        
        total_cost = sum(step.cost for step in steps)
        total_rows = steps[-1].rows_processed if steps else 0
        self.console.print(f"\n[bold]Total Cost:[/bold] {total_cost:.2f} | "
                          f"[bold]Final Rows:[/bold] {total_rows}")

    def show_results(self, results: List, limit: int = 100) -> None:
        """Display query results in a table.
        
        Args:
            results: List of result rows
            limit: Maximum rows to display
        """
        if not results:
            self.console.print("\n[dim]No rows returned.[/dim]")
            return
        
        self.console.print(f"\n[bold green]Query Results[/bold green] "
                          f"[dim](showing {min(len(results), limit)} of {len(results)} rows)[/dim]")
        
        # Get column names from first row
        if hasattr(results[0], 'keys'):
            columns = list(results[0].keys())
        else:
            columns = [f"Column_{i+1}" for i in range(len(results[0]))]
        
        safe_width = min(self.terminal_width - 4, 120)
        # Calculate column width based on number of columns
        num_cols = len(columns)
        col_width = max(10, (safe_width - (num_cols * 3)) // num_cols) if num_cols > 0 else 20
        
        table = Table(show_header=True, header_style="bold magenta", width=safe_width, show_lines=False)
        for col in columns:
            table.add_column(col, style="cyan", width=col_width, overflow="fold")
        
        for row in results[:limit]:
            if hasattr(row, 'values'):
                table.add_row(*[str(val) if val is not None else "NULL" for val in row.values()])
            else:
                table.add_row(*[str(val) if val is not None else "NULL" for val in row])
        
        self.console.print(table)
        
        if len(results) > limit:
            self.console.print(f"\n[dim]... and {len(results) - limit} more rows[/dim]")

    def show_ascii_plan(self, steps: List[ExecutionStep]) -> None:
        """Display execution plan as ASCII diagram.
        
        Args:
            steps: List of execution steps
        """
        self.console.print("\n[bold cyan]Execution Flow[/bold cyan]")
        
        for i, step in enumerate(steps):
            if i < len(steps) - 1:
                connector = "│"
            else:
                connector = "└"
            
            step_type_short = step.step_type.replace('_', ' ').title()
            self.console.print(f"{connector}── {step_type_short}")
            self.console.print(f"{'│' if i < len(steps) - 1 else ' '}   {step.description}")
            
            if step.details:
                for key, value in step.details.items():
                    if isinstance(value, list):
                        value = ", ".join(str(v) for v in value)
                    self.console.print(f"{'│' if i < len(steps) - 1 else ' '}   └─ {key}: {value}")

    def show_suggestions(self, analysis: Dict, steps: List[ExecutionStep]) -> None:
        """Show optimization suggestions.
        
        Args:
            analysis: Query analysis results
            steps: Execution steps
        """
        suggestions = []
        
        # Check for table scans without indexes
        for step in steps:
            if step.step_type == 'TABLE_SCAN' and not step.details.get('index_used', False):
                table = step.details.get('table', '')
                if table:
                    suggestions.append(
                        f"Consider creating an index on {table} to avoid full table scan"
                    )
        
        # Check for inefficient WHERE conditions
        if analysis['where_conditions'] and not any(
            step.step_type == 'INDEX_SCAN' for step in steps
        ):
            suggestions.append(
                "Consider adding indexes on columns used in WHERE clause"
            )
        
        # Check for large result sets
        if steps:
            final_rows = steps[-1].rows_processed
            if final_rows > 1000:
                suggestions.append(
                    f"Large result set ({final_rows} rows). Consider adding LIMIT or more specific WHERE conditions"
                )
        
        if suggestions:
            self.console.print("\n[bold yellow]💡 Optimization Suggestions[/bold yellow]")
            for i, suggestion in enumerate(suggestions, 1):
                self.console.print(f"  {i}. {suggestion}")
        else:
            self.console.print("\n[bold green]✓ Query looks well-optimized![/bold green]")

