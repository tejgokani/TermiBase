"""Main CLI interface for TermiBase."""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table

from termibase.storage.engine import StorageEngine
from termibase.parser.analyzer import QueryAnalyzer
from termibase.engine.simulator import ExecutionSimulator
from termibase.visualizer.renderer import QueryVisualizer
from termibase.demos.data import setup_demo_data, get_demo_queries
from termibase.learn.menu import show_learning_menu_simple
from termibase.learn.lesson import show_lesson
from termibase.cli.input_handler import QueryInputHandler

app = typer.Typer(
    name="termibase",
    help="TermiBase - A terminal-native database learning playground",
    add_completion=False,
)
console = Console()


def get_db_path() -> Path:
    """Get the default database path."""
    home = Path.home()
    termibase_dir = home / ".termibase"
    termibase_dir.mkdir(exist_ok=True)
    return termibase_dir / "sandbox.db"


@app.command()
def init(
    db_path: Optional[str] = typer.Option(
        None, "--db-path", "-d", help="Path to database file"
    ),
):
    """Initialize a new TermiBase sandbox database."""
    if db_path:
        db = Path(db_path)
    else:
        db = get_db_path()
    
    console.print(f"[bold green]Initializing TermiBase database...[/bold green]")
    console.print(f"Database path: {db}")
    
    storage = StorageEngine(str(db))
    storage.connect()
    
    # Create demo tables
    setup_demo_data(storage)
    
    storage.close()
    
    console.print("[bold green]✓ Database initialized successfully![/bold green]")
    console.print("\nRun [cyan]termibase repl[/cyan] to start the interactive shell.")


@app.command()
def repl(
    db_path: Optional[str] = typer.Option(
        None, "--db-path", "-d", help="Path to database file"
    ),
    explain: bool = typer.Option(
        False, "--explain", "-e", help="Show execution plan for each query"
    ),
):
    """Launch interactive SQL REPL."""
    if db_path:
        db = Path(db_path)
    else:
        db = get_db_path()
    
    if not db.exists():
        console.print("[bold yellow]Database not found. Initializing...[/bold yellow]")
        storage = StorageEngine(str(db))
        storage.connect()
        setup_demo_data(storage)
        storage.close()
    
    storage = StorageEngine(str(db))
    storage.connect()
    
    visualizer = QueryVisualizer()
    simulator = ExecutionSimulator(storage)
    input_handler = QueryInputHandler()
    
    # Track uncommitted changes
    has_uncommitted_changes = False
    has_successful_query = False
    
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]✨ TermiBase[/bold cyan] - Your Database Learning Playground",
        border_style="cyan"
    ))
    console.print("\n[dim]💡 Tip: Type SQL queries to see how they're executed step-by-step[/dim]")
    console.print("[dim]   Use [cyan].help[/cyan] for commands, [cyan].exit[/cyan] to quit[/dim]")
    console.print("[dim]   Write multi-line queries (end with ';') or use arrow keys for history[/dim]\n")
    
    show_explain = explain
    
    query_count = 0
    
    while True:
        try:
            # Get query using multi-line input handler
            query = input_handler.get_multiline_query("[bold cyan]termibase>[/bold cyan]")
            query_count += 1
            
            if query is None:
                # User cancelled input
                continue
            
            if not query.strip():
                continue
            
            # Handle special commands
            if query.startswith('.'):
                cmd = query[1:].strip().lower()
                
                if cmd in ('exit', 'quit'):
                    # Check for uncommitted changes
                    if has_uncommitted_changes and has_successful_query:
                        console.print("\n[yellow]⚠️  You have uncommitted changes![/yellow]")
                        console.print("[dim]Use [cyan].commit[/cyan] to save your work, or [cyan].rollback[/cyan] to discard[/dim]")
                        response = Prompt.ask("\n[cyan]Commit changes before exiting?[/cyan] (yes/no)", default="yes")
                        if response.lower() in ('yes', 'y'):
                            try:
                                storage.conn.commit()
                                console.print("[green]✓ Changes committed successfully[/green]")
                                has_uncommitted_changes = False
                            except Exception as e:
                                console.print(f"[red]Error committing: {str(e)}[/red]")
                        else:
                            console.print("[yellow]Changes not committed. Exiting...[/yellow]")
                    break
                elif cmd == 'help':
                    console.print("\n[bold cyan]📚 TermiBase Commands[/bold cyan]\n")
                    console.print("  [cyan].help[/cyan]     - Show this help")
                    console.print("  [cyan].learn[/cyan]    - Interactive SQL learning mode")
                    console.print("  [cyan].explain[/cyan]  - Toggle execution plan display")
                    console.print("  [cyan].commit[/cyan]   - Commit pending changes")
                    console.print("  [cyan].rollback[/cyan] - Rollback pending changes")
                    console.print("  [cyan].tables[/cyan]   - List all tables")
                    console.print("  [cyan].schema[/cyan]   - Show table schemas")
                    console.print("  [cyan].examples[/cyan] - Show example queries")
                    console.print("  [cyan].exit[/cyan]     - Exit REPL")
                    console.print("\n[dim]💡 Write multi-line queries (end with ';')[/dim]")
                    console.print("[dim]💡 Use ↑↓ arrow keys for command history[/dim]\n")
                elif cmd == 'commit':
                    if has_uncommitted_changes:
                        try:
                            storage.conn.commit()
                            console.print("[green]✓ Changes committed successfully[/green]")
                            has_uncommitted_changes = False
                        except Exception as e:
                            console.print(f"[red]Error committing: {str(e)}[/red]")
                    else:
                        console.print("[dim]No uncommitted changes to commit[/dim]")
                elif cmd == 'rollback':
                    if has_uncommitted_changes:
                        try:
                            storage.conn.rollback()
                            console.print("[yellow]✓ Changes rolled back[/yellow]")
                            has_uncommitted_changes = False
                        except Exception as e:
                            console.print(f"[red]Error rolling back: {str(e)}[/red]")
                    else:
                        console.print("[dim]No uncommitted changes to rollback[/dim]")
                elif cmd == 'learn':
                    # Enter learning mode
                    while True:
                        topic = show_learning_menu_simple()
                        if topic is None:
                            break
                        show_lesson(topic, storage)
                elif cmd == 'explain':
                    show_explain = not show_explain
                    console.print(f"[green]Execution plan display: {'ON' if show_explain else 'OFF'}[/green]")
                elif cmd == 'tables':
                    tables = storage.get_tables()
                    if tables:
                        console.print("\n[bold]Tables:[/bold]")
                        for table in tables:
                            console.print(f"  • {table}")
                    else:
                        console.print("\n[dim]No tables found.[/dim]")
                elif cmd == 'schema':
                    tables = storage.get_tables()
                    if tables:
                        for table in tables:
                            info = storage.get_table_info(table)
                            console.print(f"\n[bold cyan]Table: {table}[/bold cyan]")
                            schema_table = Table(show_header=True)
                            schema_table.add_column("Column", style="cyan")
                            schema_table.add_column("Type", style="green")
                            schema_table.add_column("Nullable", style="yellow")
                            for col in info:
                                schema_table.add_row(
                                    col[1],  # name
                                    col[2] or "TEXT",  # type
                                    "YES" if col[3] else "NO"  # notnull
                                )
                            console.print(schema_table)
                    else:
                        console.print("\n[dim]No tables found.[/dim]")
                elif cmd == 'examples':
                    console.print("\n[bold cyan]💡 Example Queries:[/bold cyan]\n")
                    examples = [
                        ("SELECT * FROM users LIMIT 5", "View first 5 users"),
                        ("SELECT name, age FROM users WHERE age > 28", "Filter users by age"),
                        ("SELECT city, COUNT(*) FROM users GROUP BY city", "Count users by city"),
                        ("SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id", "Join users with orders"),
                    ]
                    for i, (query, desc) in enumerate(examples, 1):
                        console.print(f"  {i}. [cyan]{query}[/cyan]")
                        console.print(f"     [dim]{desc}[/dim]\n")
                else:
                    console.print(f"[red]❌ Unknown command: {cmd}[/red]")
                    console.print("[dim]Type .help for available commands[/dim]")
                continue
            
            # Execute SQL query
            try:
                # Check if this is a DML statement (INSERT, UPDATE, DELETE)
                query_upper = query.strip().upper()
                is_dml = any(query_upper.startswith(cmd) for cmd in ['INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER'])
                
                # Show analysis
                visualizer.show_query_analysis(query)
                
                # Show execution plan if enabled
                if show_explain:
                    steps = simulator.simulate(query)
                    visualizer.show_execution_plan(steps)
                    visualizer.show_execution_steps(steps)
                    visualizer.show_ascii_plan(steps)
                    
                    analyzer = QueryAnalyzer(query)
                    analysis = analyzer.analyze()
                    visualizer.show_suggestions(analysis, steps)
                
                # Execute query
                results = storage.execute(query)
                
                # Track changes
                if is_dml:
                    has_uncommitted_changes = True
                    has_successful_query = True
                
                # Show results
                if results:
                    visualizer.show_results(results)
                    has_successful_query = True
                else:
                    console.print("\n[green]✓ Query executed successfully.[/green]")
                    if is_dml:
                        console.print("[dim]💡 Use [cyan].commit[/cyan] to save changes or [cyan].rollback[/cyan] to discard[/dim]")
                
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Interrupted. Use .exit to quit.[/yellow]")
        except EOFError:
            break
    
    # Final check for uncommitted changes
    if has_uncommitted_changes and has_successful_query:
        console.print("\n[yellow]⚠️  Warning: You have uncommitted changes![/yellow]")
        console.print("[dim]Your changes will be lost. Use [cyan].commit[/cyan] before exiting next time.[/dim]")
    
    storage.close()
    console.print("\n[bold green]Goodbye![/bold green]")


@app.command()
def explain(
    query: str = typer.Argument(..., help="SQL query to explain"),
    db_path: Optional[str] = typer.Option(
        None, "--db-path", "-d", help="Path to database file"
    ),
):
    """Show execution plan for a query without running it."""
    if db_path:
        db = Path(db_path)
    else:
        db = get_db_path()
    
    if not db.exists():
        console.print("[bold red]Database not found. Run 'termibase init' first.[/bold red]")
        raise typer.Exit(1)
    
    storage = StorageEngine(str(db))
    storage.connect()
    
    visualizer = QueryVisualizer()
    simulator = ExecutionSimulator(storage)
    
    # Show analysis
    visualizer.show_query_analysis(query)
    
    # Show execution plan
    steps = simulator.simulate(query)
    visualizer.show_execution_plan(steps)
    visualizer.show_execution_steps(steps)
    visualizer.show_ascii_plan(steps)
    
    # Show suggestions
    analyzer = QueryAnalyzer(query)
    analysis = analyzer.analyze()
    visualizer.show_suggestions(analysis, steps)
    
    storage.close()


@app.command()
def run(
    query: str = typer.Argument(..., help="SQL query to execute"),
    db_path: Optional[str] = typer.Option(
        None, "--db-path", "-d", help="Path to database file"
    ),
    explain: bool = typer.Option(
        True, "--explain/--no-explain", "-e/-E", help="Show execution plan"
    ),
):
    """Execute a query with visualization."""
    if db_path:
        db = Path(db_path)
    else:
        db = get_db_path()
    
    if not db.exists():
        console.print("[bold red]Database not found. Run 'termibase init' first.[/bold red]")
        raise typer.Exit(1)
    
    storage = StorageEngine(str(db))
    storage.connect()
    
    visualizer = QueryVisualizer()
    simulator = ExecutionSimulator(storage)
    
    try:
        # Show analysis
        visualizer.show_query_analysis(query)
        
        # Show execution plan if enabled
        if explain:
            steps = simulator.simulate(query)
            visualizer.show_execution_plan(steps)
            visualizer.show_execution_steps(steps)
            visualizer.show_ascii_plan(steps)
            
            analyzer = QueryAnalyzer(query)
            analysis = analyzer.analyze()
            visualizer.show_suggestions(analysis, steps)
        
        # Execute query
        results = storage.execute(query)
        
        # Show results
        if results:
            visualizer.show_results(results)
        else:
            console.print("\n[green]✓ Query executed successfully.[/green]")
    
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)
    finally:
        storage.close()


@app.command()
def demo(
    name: Optional[str] = typer.Argument(None, help="Demo name to run"),
    db_path: Optional[str] = typer.Option(
        None, "--db-path", "-d", help="Path to database file"
    ),
):
    """Run educational demo queries."""
    if db_path:
        db = Path(db_path)
    else:
        db = get_db_path()
    
    if not db.exists():
        console.print("[bold yellow]Database not found. Initializing...[/bold yellow]")
        storage = StorageEngine(str(db))
        storage.connect()
        setup_demo_data(storage)
        storage.close()
    
    storage = StorageEngine(str(db))
    storage.connect()
    
    visualizer = QueryVisualizer()
    simulator = ExecutionSimulator(storage)
    
    demos = get_demo_queries()
    
    if name:
        if name not in demos:
            console.print(f"[bold red]Demo '{name}' not found.[/bold red]")
            console.print(f"Available demos: {', '.join(demos.keys())}")
            storage.close()
            raise typer.Exit(1)
        
        demo_queries = {name: demos[name]}
    else:
        demo_queries = demos
    
    for demo_name, queries in demo_queries.items():
        console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
        console.print(f"[bold cyan]Demo: {demo_name}[/bold cyan]")
        console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")
        
        for i, (query, description) in enumerate(queries, 1):
            console.print(f"\n[bold yellow]Example {i}:[/bold yellow] {description}\n")
            
            try:
                visualizer.show_query_analysis(query)
                
                steps = simulator.simulate(query)
                visualizer.show_execution_plan(steps)
                visualizer.show_execution_steps(steps)
                
                results = storage.execute(query)
                visualizer.show_results(results)
                
                analyzer = QueryAnalyzer(query)
                analysis = analyzer.analyze()
                visualizer.show_suggestions(analysis, steps)
                
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {str(e)}")
            
            if i < len(queries):
                console.print("\n[dim]Press Enter to continue...[/dim]")
                try:
                    input()
                except (EOFError, KeyboardInterrupt):
                    break
    
    storage.close()


def main():
    """Entry point for the CLI."""
    # If no arguments provided, launch REPL by default
    import sys
    if len(sys.argv) == 1:
        # No arguments - launch REPL
        repl(db_path=None, explain=False)
    else:
        app()


if __name__ == "__main__":
    main()

