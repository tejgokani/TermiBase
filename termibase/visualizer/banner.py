"""Colorful banner and welcome screen for TermiBase."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box


def print_welcome_banner():
    """Print a colorful welcome banner similar to Gemini's terminal UI."""
    console = Console()
    
    # Create gradient-like colored blocks using Rich
    banner_text = Text()
    
    # Top section with gradient blocks
    console.print()
    
    # Create colorful header blocks
    colors = ["#0066FF", "#3366FF", "#6666FF", "#9966FF", "#CC66FF", "#FF66FF", "#FF66CC", "#FF6699"]
    
    # Print gradient blocks
    gradient_line = ""
    for i, color in enumerate(colors):
        gradient_line += f"[{color}]█[/{color}]" * 3
        if i < len(colors) - 1:
            gradient_line += " "
    
    console.print(gradient_line)
    console.print()
    
    # Main banner text with gradient colors
    title_colors = ["#0066FF", "#3366FF", "#6666FF", "#9966FF", "#CC66FF", "#FF66FF", "#FF66CC", "#FF6699", "#FF66FF"]
    title_letters = "TermiBase"
    
    # Create gradient title
    title_text = ""
    for i, letter in enumerate(title_letters):
        color = title_colors[i % len(title_colors)]
        title_text += f"[bold {color}]{letter}[/bold {color}]"
    
    banner = f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║                    {title_text}                    ║
    ║                                                           ║
    ║              [dim]Your Database Learning Playground[/dim]              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    
    console.print(banner)
    console.print()
    
    # Bottom gradient blocks
    console.print(gradient_line)
    console.print()
    
    # Welcome message
    welcome_panel = Panel.fit(
        "[bold cyan]✨ Welcome to TermiBase![/bold cyan]\n\n"
        "[white]Type SQL queries to see how they're executed step-by-step.[/white]\n"
        "[dim]Use [cyan].help[/cyan] for commands, [cyan].exit[/cyan] to quit[/dim]",
        border_style="blue",
        padding=(1, 2),
        box=box.ROUNDED
    )
    console.print(welcome_panel)
    console.print()


def print_colorful_blocks():
    """Print colorful gradient blocks similar to Gemini UI."""
    console = Console()
    
    # Create gradient colors from blue to pink (hex colors)
    colors = [
        "#0066FF", "#1A66FF", "#3366FF", "#4D66FF",
        "#6666FF", "#8066FF", "#9966FF", "#B366FF",
        "#CC66FF", "#E666FF", "#FF66FF", "#FF66F0",
        "#FF66E0", "#FF66D0", "#FF66C0", "#FF66B0",
        "#FF66A0", "#FF6690", "#FF6680", "#FF6670"
    ]
    
    console.print()
    
    # Create staggered grid pattern with varying block sizes
    # Each row has different block arrangements
    rows = [
        # Row 1: Long blocks, some dotted
        [("long", 0), ("dot", 1), ("medium", 2), ("dot", 3), ("long", 4)],
        # Row 2: Medium blocks, staggered
        [("medium", 5), ("long", 6), ("dot", 7), ("medium", 8), ("dot", 9)],
        # Row 3: Mix of sizes
        [("dot", 10), ("long", 11), ("medium", 12), ("dot", 13), ("long", 14)],
        # Row 4: More dots
        [("medium", 15), ("dot", 16), ("long", 17), ("dot", 18), ("medium", 19)],
    ]
    
    for row in rows:
        line_parts = []
        for block_type, color_idx in row:
            color = colors[color_idx % len(colors)]
            if block_type == "long":
                block = f"[{color}]████[/{color}]"
            elif block_type == "medium":
                block = f"[{color}]███[/{color}]"
            elif block_type == "dot":
                # Dotted pattern using unicode box-drawing
                block = f"[{color}]░░░[/{color}]"
            else:
                block = f"[{color}]██[/{color}]"
            line_parts.append(block)
        
        # Add spacing between blocks
        console.print("  ".join(line_parts))
    
    console.print()


def print_minimal_banner():
    """Print a minimal but colorful banner."""
    console = Console()
    
    console.print()
    
    # Gradient line
    gradient = "[#0066FF]█[/#0066FF][#3366FF]█[/#3366FF][#6666FF]█[/#6666FF][#9966FF]█[/#9966FF][#CC66FF]█[/#CC66FF][#FF66FF]█[/#FF66FF][#FF66CC]█[/#FF66CC][#FF6699]█[/#FF6699]"
    console.print(gradient * 10)
    
    # Title
    title = Text("TermiBase", style="bold")
    title.stylize("#0066FF", 0, 2)
    title.stylize("#3366FF", 2, 4)
    title.stylize("#6666FF", 4, 6)
    title.stylize("#9966FF", 6, 8)
    
    console.print(Align.center(title))
    console.print(Align.center("[dim]Database Learning Playground[/dim]"))
    
    console.print(gradient * 10)
    console.print()

