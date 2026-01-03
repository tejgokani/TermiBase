"""Challenge environment manager."""

import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum
from rich.console import Console
from rich.panel import Panel

from termibase.storage.engine import StorageEngine
from termibase.challenge.bank import ChallengeBank, Challenge
from termibase.challenge.evaluator import ChallengeEvaluator, EvaluationResult
from termibase.challenge.scorer import ChallengeScorer


class ChallengeMode(Enum):
    """Challenge environment modes."""
    NORMAL = "normal"


class ChallengeEnvironment:
    """Manages the challenge environment state and operations."""
    
    def __init__(self):
        """Initialize challenge environment."""
        self.console = Console()
        self.bank = ChallengeBank()
        self.evaluator = ChallengeEvaluator()
        self.scorer = ChallengeScorer()
        
        # Environment state
        self.active: bool = False
        self.current_challenge: Optional[Challenge] = None
        self.challenge_db_path: Optional[str] = None
        self.storage: Optional[StorageEngine] = None
        self.mode: ChallengeMode = ChallengeMode.NORMAL
        
        # Get challenge database path
        home = Path.home()
        termibase_dir = home / ".termibase"
        termibase_dir.mkdir(exist_ok=True)
        self.base_db_path = str(termibase_dir / "challenges.db")
    
    def enter(self, mode: ChallengeMode = ChallengeMode.NORMAL) -> None:
        """Enter challenge environment.
        
        Args:
            mode: Challenge mode (normal)
        """
        self.active = True
        self.mode = mode
        
        self.console.print("\n")
        self.console.print(Panel.fit(
            "[bold cyan]🎯 Challenge Environment[/bold cyan]\n"
            "[dim]Practice SQL with curated challenges[/dim]",
            border_style="cyan"
        ))
        
        self.console.print("\n[dim]💡 Type [cyan].help[/cyan] for available commands[/dim]")
        self.console.print("[dim]💡 Type [cyan]:exit[/cyan] to return to main REPL[/dim]\n")
    
    def exit(self) -> None:
        """Exit challenge environment."""
        if self.storage:
            self.storage.close()
            self.storage = None
        
        # Clean up challenge database
        if self.challenge_db_path and Path(self.challenge_db_path).exists():
            # Keep database for potential resume, but could delete here
            pass
        
        self.active = False
        self.current_challenge = None
        self.challenge_db_path = None
        
        self.console.print("\n[bold green]Returning to main REPL...[/bold green]\n")
    
    def start_challenge(self, challenge_id: int) -> bool:
        """Start a challenge.
        
        Args:
            challenge_id: Challenge ID to start
            
        Returns:
            True if challenge started successfully
        """
        challenge = self.bank.get_challenge(challenge_id)
        if not challenge:
            self.console.print(f"[bold red]Challenge {challenge_id} not found[/bold red]")
            return False
        
        # Check if already completed
        if self.scorer.is_challenge_completed(challenge_id):
            self.console.print(f"[yellow]Challenge {challenge_id} already completed![/yellow]")
            response = self.console.input("[cyan]Start again? (y/n): [/cyan]")
            if response.lower() != 'y':
                return False
        
        # Set up challenge database
        self.challenge_db_path = f"{self.base_db_path}.{challenge_id}"
        self.bank.setup_challenge_database(challenge, self.challenge_db_path)
        
        # Connect storage
        if self.storage:
            self.storage.close()
        self.storage = StorageEngine(self.challenge_db_path)
        self.storage.connect()
        
        self.current_challenge = challenge
        
        # Display challenge info
        self.console.print("\n[bold cyan]" + "="*60 + "[/bold cyan]")
        self.console.print(f"[bold cyan]Challenge #{challenge.id}: {challenge.title}[/bold cyan]")
        self.console.print(f"[bold]Difficulty:[/bold] {challenge.difficulty.upper()}")
        self.console.print(f"[bold]Concepts:[/bold] {', '.join(challenge.required_concepts)}")
        self.console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")
        self.console.print(f"[white]{challenge.description}[/white]\n")
        
        # Show schema
        self.console.print("[bold yellow]Available Tables:[/bold yellow]")
        tables = self.storage.get_tables()
        for table in tables:
            self.console.print(f"  • [cyan]{table}[/cyan]")
            info = self.storage.get_table_info(table)
            columns = [col[1] for col in info]
            self.console.print(f"    Columns: [dim]{', '.join(columns)}[/dim]")
        self.console.print()
        
        return True
    
    def submit_solution(self, query: str) -> Dict[str, Any]:
        """Submit a solution for evaluation.
        
        Args:
            query: User's SQL query
            
        Returns:
            Dictionary with evaluation results
        """
        if not self.current_challenge or not self.challenge_db_path:
            return {
                'success': False,
                'error': 'No active challenge'
            }
        
        # Evaluate solution
        result, details = self.evaluator.evaluate(
            self.current_challenge,
            query,
            self.challenge_db_path
        )
        
        # Record attempt
        self.scorer.record_attempt(
            self.current_challenge.id,
            result.value,
            query,
            self.current_challenge.difficulty,
            self.current_challenge.required_concepts
        )
        
        # Prepare response
        response = {
            'success': True,
            'result': result.value,
            'details': details,
            'challenge_id': self.current_challenge.id
        }
        
        # Display results
        if result == EvaluationResult.PERFECT:
            self.console.print("\n[bold green]✓ Perfect Solution![/bold green]")
            points = self.scorer._get_points_for_difficulty(self.current_challenge.difficulty)
            self.console.print(f"[green]Points awarded: {points}[/green]")
        elif result == EvaluationResult.PARTIAL:
            self.console.print("\n[yellow]⚠ Partial Solution[/yellow]")
            if details.get('hardcoded_detected'):
                self.console.print("[dim]Note: Hardcoded constants detected. Try a more dynamic solution.[/dim]")
        else:
            self.console.print("\n[bold red]✗ Incorrect Solution[/bold red]")
            if details.get('error'):
                error_msg = self.evaluator.get_friendly_error_message(details['error'])
                self.console.print(f"[red]{error_msg}[/red]")
            if details.get('constraints_violated'):
                self.console.print(f"[red]Violations: {', '.join(details['constraints_violated'])}[/red]")
        
        return response
    
    def reset_challenge(self) -> bool:
        """Reset current challenge database.
        
        Returns:
            True if reset successful
        """
        if not self.current_challenge:
            self.console.print("[red]No active challenge to reset[/red]")
            return False
        
        # Re-setup database
        self.bank.setup_challenge_database(self.current_challenge, self.challenge_db_path)
        
        # Reconnect storage
        if self.storage:
            self.storage.close()
        self.storage = StorageEngine(self.challenge_db_path)
        self.storage.connect()
        
        self.console.print("[green]Challenge reset successfully[/green]")
        return True
    
    def get_storage(self) -> Optional[StorageEngine]:
        """Get current storage engine.
        
        Returns:
            StorageEngine instance or None
        """
        return self.storage
    
    def is_active(self) -> bool:
        """Check if challenge environment is active.
        
        Returns:
            True if active
        """
        return self.active
    
    def get_current_challenge(self) -> Optional[Challenge]:
        """Get current challenge.
        
        Returns:
            Current challenge or None
        """
        return self.current_challenge
    

