"""Interactive menu for learning section."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from typing import Optional
import sys

from termibase.learn.content import get_learning_topics, get_topic_list


def show_learning_menu() -> Optional[str]:
    """Show interactive learning menu with arrow key navigation.
    
    Returns:
        Selected topic name or None if cancelled
    """
    console = Console()
    topics = get_topic_list()
    selected_index = 0
    
    while True:
        console.clear()
        
        # Show menu
        console.print("\n[bold cyan]📚 SQL Learning Topics[/bold cyan]\n")
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("", width=3)
        table.add_column("Topic", width=30)
        table.add_column("Description", width=50)
        
        for i, topic in enumerate(topics):
            topic_data = get_learning_topics()[topic]
            marker = "→" if i == selected_index else " "
            style = "bold cyan" if i == selected_index else "white"
            table.add_row(
                f"[{style}]{marker}[/{style}]",
                f"[{style}]{topic}[/{style}]",
                f"[dim]{topic_data['description']}[/dim]"
            )
        
        console.print(table)
        console.print("\n[dim]Use ↑↓ arrows to navigate, Enter to select, 'q' to quit[/dim]")
        
        # Get user input
        try:
            key = _get_key()
            
            if key == 'up':
                selected_index = (selected_index - 1) % len(topics)
            elif key == 'down':
                selected_index = (selected_index + 1) % len(topics)
            elif key == 'enter':
                return topics[selected_index]
            elif key == 'q':
                return None
        except (KeyboardInterrupt, EOFError):
            return None


def _get_key() -> str:
    """Get a single keypress (for arrow key navigation).
    
    Note: This is kept for potential future use but show_learning_menu_simple
    is the recommended method for better compatibility.
    """
    try:
        import tty
        import termios
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        
        # Read single character
        ch = sys.stdin.read(1)
        
        # Check for escape sequence (arrow keys)
        if ch == '\x1b':
            ch = sys.stdin.read(1)
            if ch == '[':
                ch = sys.stdin.read(1)
                if ch == 'A':
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    return 'up'
                elif ch == 'B':
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    return 'down'
        
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        if ch == '\r' or ch == '\n':
            return 'enter'
        elif ch.lower() == 'q':
            return 'q'
        else:
            return ch
    except (ImportError, OSError, AttributeError):
        # Fallback - not available on all systems
        return 'q'


def show_learning_menu_simple() -> Optional[str]:
    """Show learning menu with number selection (simpler, more compatible)."""
    console = Console()
    topics = get_topic_list()
    
    console.print("\n[bold cyan]📚 SQL Learning Topics[/bold cyan]\n")
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("#", width=4, justify="right")
    table.add_column("Topic", width=30)
    table.add_column("Description", width=50)
    
    for i, topic in enumerate(topics, 1):
        topic_data = get_learning_topics()[topic]
        table.add_row(
            f"[cyan]{i}[/cyan]",
            f"[bold]{topic}[/bold]",
            f"[dim]{topic_data['description']}[/dim]"
        )
    
    console.print(table)
    console.print()
    
    while True:
        try:
            choice = Prompt.ask(
                "[cyan]Select a topic (1-{}) or 'q' to quit[/cyan]".format(len(topics)),
                default="q"
            )
            
            if choice.lower() == 'q':
                return None
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(topics):
                    return topics[index]
                else:
                    console.print(f"[red]Please enter a number between 1 and {len(topics)}[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number[/red]")
        except (KeyboardInterrupt, EOFError):
            return None

