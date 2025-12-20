"""Interactive lesson display and practice."""

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt
from rich.table import Table
from typing import Optional

from termibase.learn.content import get_learning_topics
from termibase.storage.engine import StorageEngine
from termibase.parser.analyzer import QueryAnalyzer
from termibase.engine.simulator import ExecutionSimulator
from termibase.visualizer.renderer import QueryVisualizer


def show_lesson(topic: str, storage: StorageEngine) -> None:
    """Display lesson content and allow practice.
    
    Args:
        topic: Topic name to learn
        storage: Storage engine for executing practice queries
    """
    console = Console()
    topics = get_learning_topics()
    
    if topic not in topics:
        console.print(f"[red]Topic '{topic}' not found[/red]")
        return
    
    content = topics[topic]
    visualizer = QueryVisualizer()
    simulator = ExecutionSimulator(storage)
    
    while True:
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]📖 {topic}[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
        
        # Show explanation
        console.print("[bold]Explanation:[/bold]")
        console.print(Panel(content['explanation'], border_style="blue", padding=(1, 2)))
        console.print()
        
        # Show examples
        console.print("[bold]Example Queries:[/bold]")
        for i, example in enumerate(content['examples'], 1):
            console.print(f"\n[dim]Example {i}:[/dim]")
            console.print(Panel(Syntax(example, "sql", theme="monokai"), 
                              border_style="green", padding=(0, 1)))
        console.print()
        
        # Practice section
        console.print("[bold yellow]💡 Practice Time![/bold yellow]")
        console.print("[dim]Try writing your own query, or run the practice query below:[/dim]\n")
        
        # Show practice query option
        console.print(f"[cyan]Practice Query:[/cyan]")
        console.print(Panel(Syntax(content['practice_query'], "sql", theme="monokai"),
                          border_style="yellow", padding=(0, 1)))
        console.print()
        
        # Menu options
        console.print("[bold]Options:[/bold]")
        console.print("  [cyan]1[/cyan] - Run practice query")
        console.print("  [cyan]2[/cyan] - Write your own query")
        console.print("  [cyan]3[/cyan] - See execution plan")
        console.print("  [cyan]4[/cyan] - Back to topics")
        console.print("  [cyan]q[/cyan] - Quit learning mode")
        console.print()
        
        choice = Prompt.ask("[cyan]Choose an option[/cyan]", default="4")
        
        if choice == '1':
            # Run practice query
            _run_practice_query(content['practice_query'], storage, visualizer, simulator)
        elif choice == '2':
            # Write custom query
            _run_custom_query(storage, visualizer, simulator)
        elif choice == '3':
            # Show execution plan
            _show_execution_plan(content['practice_query'], storage, visualizer, simulator)
        elif choice == '4':
            return  # Back to topics
        elif choice.lower() == 'q':
            return  # Quit


def _run_practice_query(query: str, storage: StorageEngine, 
                       visualizer: QueryVisualizer, simulator: ExecutionSimulator) -> None:
    """Run the practice query with visualization."""
    console = Console()
    
    console.print(f"\n[bold green]Running practice query...[/bold green]\n")
    
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
    
    console.print("\n[dim]Press Enter to continue...[/dim]")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def _run_custom_query(storage: StorageEngine, visualizer: QueryVisualizer, 
                      simulator: ExecutionSimulator) -> None:
    """Allow user to write and run custom query."""
    console = Console()
    
    console.print("\n[bold yellow]Write your own query:[/bold yellow]")
    console.print("[dim]Type your SQL query (or 'back' to return)[/dim]\n")
    
    try:
        query = Prompt.ask("[cyan]SQL>[/cyan]", default="")
        
        if query.lower() == 'back':
            return
        
        if not query.strip():
            return
        
        console.print()
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
    
    console.print("\n[dim]Press Enter to continue...[/dim]")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def _show_execution_plan(query: str, storage: StorageEngine, 
                        visualizer: QueryVisualizer, simulator: ExecutionSimulator) -> None:
    """Show execution plan for practice query."""
    console = Console()
    
    console.print(f"\n[bold yellow]Execution Plan for Practice Query:[/bold yellow]\n")
    
    try:
        visualizer.show_query_analysis(query)
        
        steps = simulator.simulate(query)
        visualizer.show_execution_plan(steps)
        visualizer.show_execution_steps(steps)
        visualizer.show_ascii_plan(steps)
        
        analyzer = QueryAnalyzer(query)
        analysis = analyzer.analyze()
        visualizer.show_suggestions(analysis, steps)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    console.print("\n[dim]Press Enter to continue...[/dim]")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass

