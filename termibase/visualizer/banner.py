"""Colorful banner and welcome screen for TermiBase - Gemini style."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

# Gemini's actual colors
BEIGE = "#f8f8f2"
DARK_GREY = "#44475a"
DARK_BG = "#282a36"


def print_colorful_blocks():
    """Print blocks matching Gemini's actual terminal style - flag pattern."""
    console = Console()
    
    console.print()
    
def print_colorful_blocks():
    """Print blocks matching Gemini's actual terminal style - flag pattern."""
    console = Console()
    
    console.print()
    
    # Top row: Flag-like pattern - 4 vertical segments
    # Using full-width blocks for better visual match
    
    # Row 1: Top of flag pattern
    row1 = f"[{BEIGE}]██[/{BEIGE}][{BEIGE}]██[/{BEIGE}]  [{DARK_GREY}]░░[/{DARK_GREY}][{DARK_GREY}]░░[/{DARK_GREY}]  [{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}][{BEIGE}]██[/{BEIGE}]"
    console.print(row1)
    
    # Row 2: Second row
    row2 = f"[{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}][{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}]"
    console.print(row2)
    
    # Row 3: Dotted bands
    row3 = f"[{DARK_GREY}]░░[/{DARK_GREY}][{DARK_GREY}]░░[/{DARK_GREY}]  [{DARK_GREY}]░░[/{DARK_GREY}]  [{DARK_GREY}]░░[/{DARK_GREY}][{DARK_GREY}]░░[/{DARK_GREY}]  [{DARK_GREY}]░░[/{DARK_GREY}][{DARK_GREY}]░░[/{DARK_GREY}]"
    console.print(row3)
    
    # Row 4: Bottom of segments
    row4 = f"[{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}]"
    console.print(row4)
    
    # Row 5: Continue segments
    row5 = f"[{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}]  [{BEIGE}]██[/{BEIGE}]"
    console.print(row5)
    
    console.print()
    
    # Bottom row: 8 identical beige squares
    bottom_squares = f"[{BEIGE}]██[/{BEIGE}]  " * 8
    console.print(bottom_squares)
    console.print()


def print_welcome_banner():
    """Print welcome banner in Gemini's minimalist style."""
    console = Console()
    
    console.print()
    
    # Simple beige title (Gemini's minimalist style)
    title_text = f"[bold {BEIGE}]TermiBase[/bold {BEIGE}]"
    
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
    
    # Welcome message (Gemini's minimalist style)
    welcome_panel = Panel.fit(
        f"[bold {BEIGE}]✨ Welcome to TermiBase![/bold {BEIGE}]\n\n"
        "[white]Type SQL queries to see how they're executed step-by-step.[/white]\n"
        f"[dim]Use [{BEIGE}].help[/{BEIGE}] for commands, [{BEIGE}].exit[/{BEIGE}] to quit[/dim]",
        border_style=BEIGE,  # Beige border (Gemini style)
        padding=(1, 2),
        box=box.ROUNDED
    )
    console.print(welcome_panel)
    console.print()


def print_minimal_banner():
    """Print a minimal banner in Gemini style."""
    console = Console()
    
    console.print()
    
    # Beige line (Gemini style)
    beige_line = f"[{BEIGE}]█[/{BEIGE}]" * 20
    console.print(beige_line)
    
    # Title in beige (Gemini's minimalist style)
    title = Text("TermiBase", style="bold")
    title.stylize(BEIGE, 0, 9)
    
    console.print(Align.center(title))
    console.print(Align.center("[dim]Database Learning Playground[/dim]"))
    
    console.print(beige_line)
    console.print()
