"""Multi-line query input handler with command history."""

import sys
import readline
from typing import List, Optional
from rich.console import Console
from rich.prompt import Prompt


class QueryInputHandler:
    """Handles multi-line query input with history support."""
    
    def __init__(self):
        self.console = Console()
        self.history: List[str] = []
        self.history_index = -1
        self._setup_readline()
    
    def _setup_readline(self):
        """Setup readline for command history."""
        try:
            # Enable readline history
            readline.set_history_length(1000)
            
            # Try to load history from file
            try:
                readline.read_history_file('.termibase_history')
            except FileNotFoundError:
                pass
        except (ImportError, AttributeError):
            # readline not available (Windows)
            pass
    
    def _save_history(self):
        """Save history to file."""
        try:
            readline.write_history_file('.termibase_history')
        except (ImportError, AttributeError, IOError):
            pass
    
    def get_multiline_query(self, prompt: str = "termibase>") -> Optional[str]:
        """Get a multi-line query from user, ending with semicolon.
        
        Uses readline for arrow key history navigation (works on Unix/Mac).
        On Windows, falls back to basic input.
        
        Args:
            prompt: Prompt text to display (Rich markup will be stripped)
            
        Returns:
            Complete query string or None if cancelled
        """
        # Strip Rich markup from prompt for readline
        import re
        clean_prompt = re.sub(r'\[.*?\]', '', prompt).strip()
        
        lines = []
        continuation_prompt = "      -> "
        
        while True:
            try:
                # Get input line using readline (supports arrow keys)
                if lines:
                    # Continuation line
                    line = input(continuation_prompt)
                else:
                    # First line - use readline for history
                    try:
                        line = input(f"{clean_prompt} ")
                    except (ImportError, AttributeError):
                        # Fallback if readline not available
                        line = input(f"{clean_prompt} ")
                
                # Handle empty line
                if not line.strip() and not lines:
                    continue
                
                # Check for special commands (only on first line)
                if not lines and line.strip().startswith('.'):
                    # Add to history if not empty
                    if line.strip():
                        self.history.append(line.strip())
                        self._save_history()
                    return line.strip()
                
                # Add line to query
                lines.append(line)
                
                # Check if query is complete (ends with semicolon)
                full_query = '\n'.join(lines)
                if full_query.strip().endswith(';'):
                    # Remove trailing semicolon spaces and return
                    query = full_query.strip()
                    # Add to history
                    if query:
                        self.history.append(query)
                        self._save_history()
                    return query
                
                # Check for cancellation (Ctrl+C or empty line with backslash)
                if line.strip() == '\\':
                    return None
                    
            except (KeyboardInterrupt, EOFError):
                # User cancelled
                if lines:
                    self.console.print("\n[yellow]Query cancelled. (Use '\\' on empty line to cancel)[/yellow]")
                return None
    
    def get_single_line_query(self, prompt: str = "termibase>") -> Optional[str]:
        """Get a single line query (for compatibility).
        
        Args:
            prompt: Prompt text to display
            
        Returns:
            Query string or None
        """
        try:
            query = input(f"{prompt} ")
            if query.strip():
                self.history.append(query.strip())
                self._save_history()
            return query.strip() if query.strip() else None
        except (KeyboardInterrupt, EOFError):
            return None
    
    def add_to_history(self, query: str):
        """Manually add a query to history."""
        if query.strip():
            self.history.append(query.strip())
            self._save_history()
    
    def get_history(self) -> List[str]:
        """Get query history."""
        return self.history.copy()
    
    def clear_history(self):
        """Clear query history."""
        self.history.clear()
        try:
            readline.clear_history()
        except (ImportError, AttributeError):
            pass

