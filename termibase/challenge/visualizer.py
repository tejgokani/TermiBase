"""Rich visualizations for challenge progress and stats."""

from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.text import Text
from rich.layout import Layout
from rich import box

from termibase.challenge.scorer import ChallengeScorer, RankTier, UserProgress


class ChallengeVisualizer:
    """Visualizes challenge progress and statistics."""
    
    def __init__(self, scorer: ChallengeScorer):
        """Initialize visualizer.
        
        Args:
            scorer: ChallengeScorer instance
        """
        self.console = Console()
        self.scorer = scorer
    
    def show_stats(self) -> None:
        """Display comprehensive challenge statistics."""
        progress = self.scorer.get_progress()
        rank = self.scorer.get_rank()
        
        self.console.print("\n[bold cyan]" + "="*60 + "[/bold cyan]")
        self.console.print("[bold cyan]Challenge Statistics[/bold cyan]")
        self.console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")
        
        # Overall stats
        stats_table = Table(show_header=False, box=None, padding=(0, 2))
        stats_table.add_column("Metric", style="cyan", width=25)
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Total Score", f"{progress.total_score} / {ChallengeScorer.MAX_SCORE}")
        stats_table.add_row("Perfect Solves", str(progress.perfect_solves))
        stats_table.add_row("Total Attempts", str(progress.total_attempts))
        stats_table.add_row("Rank", f"[bold]{rank.value}[/bold]")
        
        if progress.total_attempts > 0:
            success_rate = (progress.perfect_solves / progress.total_attempts) * 100
            stats_table.add_row("Success Rate", f"{success_rate:.1f}%")
        
        self.console.print(stats_table)
        self.console.print()
        
        # Score progress bar
        score_percent = (progress.total_score / ChallengeScorer.MAX_SCORE) * 100
        self.console.print("[bold]Overall Progress:[/bold]")
        self._render_progress_bar(score_percent, progress.total_score, ChallengeScorer.MAX_SCORE)
        self.console.print()
        
        # Difficulty breakdown
        self._show_difficulty_stats(progress)
        
        # Concept mastery
        if progress.concept_mastery:
            self._show_concept_mastery(progress)
    
    def _show_difficulty_stats(self, progress: UserProgress) -> None:
        """Show statistics by difficulty.
        
        Args:
            progress: UserProgress object
        """
        self.console.print("\n[bold yellow]Difficulty Breakdown:[/bold yellow]")
        
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Difficulty", style="cyan", width=12)
        table.add_column("Perfect", style="green", justify="right")
        table.add_column("Attempts", style="yellow", justify="right")
        table.add_column("Progress", style="blue")
        
        for difficulty in ['easy', 'medium', 'hard']:
            stats = progress.difficulty_stats.get(difficulty, {'perfect': 0, 'attempts': 0})
            perfect = stats['perfect']
            attempts = stats['attempts']
            
            # Calculate progress
            if difficulty == 'easy':
                total = 40
                points = ChallengeScorer.POINTS_EASY
            elif difficulty == 'medium':
                total = 40
                points = ChallengeScorer.POINTS_MEDIUM
            else:
                total = 20
                points = ChallengeScorer.POINTS_HARD
            
            progress_pct = (perfect / total * 100) if total > 0 else 0
            progress_bar = self._create_progress_bar_string(progress_pct, 20)
            
            table.add_row(
                difficulty.upper(),
                str(perfect),
                str(attempts),
                progress_bar
            )
        
        self.console.print(table)
    
    def _show_concept_mastery(self, progress: UserProgress) -> None:
        """Show concept mastery statistics.
        
        Args:
            progress: UserProgress object
        """
        if not progress.concept_mastery:
            return
        
        self.console.print("\n[bold yellow]Concept Mastery:[/bold yellow]")
        
        # Sort by mastery count
        sorted_concepts = sorted(
            progress.concept_mastery.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Concept", style="cyan", width=25)
        table.add_column("Perfect Solves", style="green", justify="right")
        table.add_column("Mastery", style="blue")
        
        max_mastery = max(progress.concept_mastery.values()) if progress.concept_mastery.values() else 1
        
        for concept, count in sorted_concepts[:10]:  # Top 10
            mastery_pct = (count / max_mastery * 100) if max_mastery > 0 else 0
            mastery_bar = self._create_progress_bar_string(mastery_pct, 15)
            table.add_row(concept, str(count), mastery_bar)
        
        self.console.print(table)
    
    def show_progress(self) -> None:
        """Show detailed progress information."""
        progress = self.scorer.get_progress()
        
        self.console.print("\n[bold cyan]Your Progress[/bold cyan]\n")
        
        # Completed challenges
        completed = progress.challenges_completed
        if completed:
            self.console.print(f"[green]Completed Challenges: {len(completed)}[/green]")
            # Show first 10
            display_list = sorted(completed)[:10]
            self.console.print(f"  {', '.join(map(str, display_list))}")
            if len(completed) > 10:
                self.console.print(f"  ... and {len(completed) - 10} more")
        else:
            self.console.print("[dim]No challenges completed yet[/dim]")
        
        self.console.print()
    
    def show_challenge_list(self, challenges: List, completed_ids: List[int], difficulty_filter: Optional[str] = None) -> None:
        """Display list of challenges in multi-column compact format.
        
        Args:
            challenges: List of Challenge objects
            completed_ids: List of completed challenge IDs
            difficulty_filter: Optional difficulty filter ('easy', 'medium', 'hard')
        """
        self.console.print("\n[bold cyan]Available Challenges[/bold cyan]")
        if difficulty_filter:
            self.console.print(f"[dim]Filter: {difficulty_filter.upper()}[/dim]")
        self.console.print()
        
        # Filter by difficulty if specified
        if difficulty_filter:
            challenges = [c for c in challenges if c.difficulty == difficulty_filter.lower()]
            if not challenges:
                self.console.print(f"[yellow]No {difficulty_filter} challenges found.[/yellow]\n")
                return
        
        # Group by difficulty
        by_difficulty = {'easy': [], 'medium': [], 'hard': []}
        for challenge in challenges:
            by_difficulty[challenge.difficulty].append(challenge)
        
        for difficulty in ['easy', 'medium', 'hard']:
            if not by_difficulty[difficulty]:
                continue
            
            self.console.print(f"[bold yellow]{difficulty.upper()} Challenges:[/bold yellow]")
            
            # Sort challenges by ID
            sorted_challenges = sorted(by_difficulty[difficulty], key=lambda c: c.id)
            
            # Calculate number of columns based on terminal width
            # Each challenge column needs: ID (5) + Status (8) + spacing = ~15 chars
            try:
                terminal_width = self.console.width
            except:
                terminal_width = 120
            
            # Determine challenges per row (aim for 6-8 columns)
            challenges_per_row = max(4, min(8, terminal_width // 15))
            
            # Create table with multiple challenge columns
            table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE, show_lines=False, padding=(0, 1))
            
            # Add header columns (ID, Status for each challenge column)
            for col_idx in range(challenges_per_row):
                table.add_column("ID", style="cyan", width=5, justify="right", no_wrap=True)
                table.add_column("Status", style="green", width=8, no_wrap=True)
            
            # Add rows
            num_challenges = len(sorted_challenges)
            num_rows = (num_challenges + challenges_per_row - 1) // challenges_per_row
            
            for row_idx in range(num_rows):
                row_data = []
                for col_idx in range(challenges_per_row):
                    challenge_idx = row_idx * challenges_per_row + col_idx
                    if challenge_idx < num_challenges:
                        challenge = sorted_challenges[challenge_idx]
                        status = "[green]✓ Done[/green]" if challenge.id in completed_ids else "[dim]○[/dim]"
                        row_data.extend([
                            str(challenge.id),
                            status
                        ])
                    else:
                        # Empty cells for incomplete row
                        row_data.extend(["", ""])
                
                table.add_row(*row_data)
            
            self.console.print(table)
            self.console.print()
    
    def show_rank_info(self) -> None:
        """Display rank information."""
        rank = self.scorer.get_rank()
        progress = self.scorer.get_progress()
        
        score_percent = (progress.total_score / ChallengeScorer.MAX_SCORE) * 100
        
        rank_colors = {
            RankTier.BEGINNER: "yellow",
            RankTier.INTERMEDIATE: "cyan",
            RankTier.ADVANCED: "green"
        }
        
        color = rank_colors.get(rank, "white")
        
        self.console.print("\n[bold cyan]Your Rank[/bold cyan]\n")
        self.console.print(Panel.fit(
            f"[{color}]{rank.value}[/{color}]",
            title="Current Rank",
            border_style=color
        ))
        
        self.console.print(f"\nScore: {progress.total_score} / {ChallengeScorer.MAX_SCORE}")
        self._render_progress_bar(score_percent, progress.total_score, ChallengeScorer.MAX_SCORE)
        
        # Show next rank requirements
        if rank != RankTier.ADVANCED:
            next_thresholds = {
                RankTier.BEGINNER: (ChallengeScorer.MAX_SCORE * 0.3, RankTier.INTERMEDIATE),
                RankTier.INTERMEDIATE: (ChallengeScorer.MAX_SCORE * 0.6, RankTier.ADVANCED),
            }
            
            if rank in next_thresholds:
                threshold, next_rank = next_thresholds[rank]
                needed = int(threshold - progress.total_score)
                if needed > 0:
                    self.console.print(f"\n[dim]Next rank ({next_rank.value}): {needed} more points needed[/dim]")
    
    def _render_progress_bar(self, percent: float, current: int, total: int) -> None:
        """Render a progress bar.
        
        Args:
            percent: Percentage (0-100)
            current: Current value
            total: Total value
        """
        bar_width = 40
        filled = int(bar_width * percent / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        
        self.console.print(f"[green]{bar}[/green] {percent:.1f}% ({current}/{total})")
    
    def _create_progress_bar_string(self, percent: float, width: int) -> str:
        """Create a progress bar string.
        
        Args:
            percent: Percentage (0-100)
            width: Bar width
            
        Returns:
            Progress bar string
        """
        filled = int(width * percent / 100)
        return "█" * filled + "░" * (width - filled)
    
    def show_ascii_chart(self, data: List[Tuple[str, float]], title: str = "Chart") -> None:
        """Render a simple ASCII bar chart.
        
        Args:
            data: List of (label, value) tuples
            title: Chart title
        """
        if not data:
            return
        
        self.console.print(f"\n[bold cyan]{title}[/bold cyan]")
        
        max_value = max(v for _, v in data)
        bar_width = 30
        
        for label, value in data:
            bar_length = int((value / max_value) * bar_width) if max_value > 0 else 0
            bar = "█" * bar_length
            self.console.print(f"  {label:20} {bar} {value:.1f}")

