"""Scoring and progress tracking for challenges."""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class RankTier(Enum):
    """User rank tiers based on score."""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


@dataclass
class ChallengeAttempt:
    """Represents a single challenge attempt."""
    challenge_id: int
    timestamp: str
    result: str  # 'perfect', 'partial', 'incorrect'
    query: str
    attempts_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChallengeAttempt':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class UserProgress:
    """User progress tracking."""
    total_score: int
    perfect_solves: int
    total_attempts: int
    challenges_completed: List[int]
    attempts: List[ChallengeAttempt]
    concept_mastery: Dict[str, int]  # concept -> count of perfect solves
    difficulty_stats: Dict[str, Dict[str, int]]  # difficulty -> {perfect, attempts}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'total_score': self.total_score,
            'perfect_solves': self.perfect_solves,
            'total_attempts': self.total_attempts,
            'challenges_completed': self.challenges_completed,
            'attempts': [a.to_dict() for a in self.attempts],
            'concept_mastery': self.concept_mastery,
            'difficulty_stats': self.difficulty_stats
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProgress':
        """Create from dictionary."""
        attempts = [ChallengeAttempt.from_dict(a) for a in data.get('attempts', [])]
        return cls(
            total_score=data.get('total_score', 0),
            perfect_solves=data.get('perfect_solves', 0),
            total_attempts=data.get('total_attempts', 0),
            challenges_completed=data.get('challenges_completed', []),
            attempts=attempts,
            concept_mastery=data.get('concept_mastery', {}),
            difficulty_stats=data.get('difficulty_stats', {
                'easy': {'perfect': 0, 'attempts': 0},
                'medium': {'perfect': 0, 'attempts': 0},
                'hard': {'perfect': 0, 'attempts': 0}
            })
        )


class ChallengeScorer:
    """Manages scoring and progress tracking."""
    
    # Points per difficulty
    POINTS_EASY = 10
    POINTS_MEDIUM = 25
    POINTS_HARD = 50
    MAX_SCORE = 2600  # 40*10 + 40*25 + 20*50
    
    def __init__(self, progress_file: Optional[Path] = None):
        """Initialize scorer.
        
        Args:
            progress_file: Path to progress JSON file. If None, uses default location.
        """
        if progress_file is None:
            home = Path.home()
            termibase_dir = home / ".termibase"
            termibase_dir.mkdir(exist_ok=True)
            progress_file = termibase_dir / "challenge_progress.json"
        
        self.progress_file = progress_file
        self._progress: Optional[UserProgress] = None
        self._load_progress()
    
    def _load_progress(self) -> None:
        """Load progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._progress = UserProgress.from_dict(data)
            except (json.JSONDecodeError, KeyError, TypeError):
                # Invalid file, start fresh
                self._progress = self._create_empty_progress()
        else:
            self._progress = self._create_empty_progress()
    
    def _save_progress(self) -> None:
        """Save progress to file."""
        if self._progress:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self._progress.to_dict(), f, indent=2)
    
    def _create_empty_progress(self) -> UserProgress:
        """Create empty progress object."""
        return UserProgress(
            total_score=0,
            perfect_solves=0,
            total_attempts=0,
            challenges_completed=[],
            attempts=[],
            concept_mastery={},
            difficulty_stats={
                'easy': {'perfect': 0, 'attempts': 0},
                'medium': {'perfect': 0, 'attempts': 0},
                'hard': {'perfect': 0, 'attempts': 0}
            }
        )
    
    def record_attempt(
        self,
        challenge_id: int,
        result: str,
        query: str,
        difficulty: str,
        concepts: List[str]
    ) -> None:
        """Record a challenge attempt.
        
        Args:
            challenge_id: Challenge ID
            result: 'perfect', 'partial', or 'incorrect'
            query: User's query
            difficulty: Challenge difficulty
            concepts: List of required concepts
        """
        if not self._progress:
            self._progress = self._create_empty_progress()
        
        # Count attempts for this challenge
        challenge_attempts = [
            a for a in self._progress.attempts
            if a.challenge_id == challenge_id
        ]
        attempts_count = len(challenge_attempts) + 1
        
        # Create attempt record
        attempt = ChallengeAttempt(
            challenge_id=challenge_id,
            timestamp=datetime.now().isoformat(),
            result=result,
            query=query,
            attempts_count=attempts_count
        )
        
        self._progress.attempts.append(attempt)
        self._progress.total_attempts += 1
        
        # Update difficulty stats
        if difficulty in self._progress.difficulty_stats:
            self._progress.difficulty_stats[difficulty]['attempts'] += 1
        
        # Update score and completion if perfect
        if result == 'perfect':
            # Only award points if not already completed
            if challenge_id not in self._progress.challenges_completed:
                points = self._get_points_for_difficulty(difficulty)
                self._progress.total_score += points
                self._progress.perfect_solves += 1
                self._progress.challenges_completed.append(challenge_id)
                
                # Update difficulty stats
                if difficulty in self._progress.difficulty_stats:
                    self._progress.difficulty_stats[difficulty]['perfect'] += 1
                
                # Update concept mastery
                for concept in concepts:
                    self._progress.concept_mastery[concept] = \
                        self._progress.concept_mastery.get(concept, 0) + 1
        
        self._save_progress()
    
    def _get_points_for_difficulty(self, difficulty: str) -> int:
        """Get points for a difficulty level.
        
        Args:
            difficulty: Difficulty level
            
        Returns:
            Points value
        """
        difficulty_lower = difficulty.lower()
        if difficulty_lower == 'easy':
            return self.POINTS_EASY
        elif difficulty_lower == 'medium':
            return self.POINTS_MEDIUM
        elif difficulty_lower == 'hard':
            return self.POINTS_HARD
        return 0
    
    def get_progress(self) -> UserProgress:
        """Get current progress.
        
        Returns:
            UserProgress object
        """
        if not self._progress:
            self._progress = self._create_empty_progress()
        return self._progress
    
    def get_rank(self) -> RankTier:
        """Get user's current rank.
        
        Returns:
            RankTier enum value
        """
        if not self._progress:
            return RankTier.BEGINNER
        
        score = self._progress.total_score
        max_score = self.MAX_SCORE
        
        if score >= max_score * 0.6:  # 60%+
            return RankTier.ADVANCED
        elif score >= max_score * 0.3:  # 30%+
            return RankTier.INTERMEDIATE
        else:
            return RankTier.BEGINNER
    
    def get_challenge_attempts(self, challenge_id: int) -> List[ChallengeAttempt]:
        """Get all attempts for a challenge.
        
        Args:
            challenge_id: Challenge ID
            
        Returns:
            List of attempts
        """
        if not self._progress:
            return []
        return [
            a for a in self._progress.attempts
            if a.challenge_id == challenge_id
        ]
    
    def is_challenge_completed(self, challenge_id: int) -> bool:
        """Check if challenge is completed (perfect solve).
        
        Args:
            challenge_id: Challenge ID
            
        Returns:
            True if completed
        """
        if not self._progress:
            return False
        return challenge_id in self._progress.challenges_completed
    
    def reset_progress(self) -> None:
        """Reset all progress."""
        self._progress = self._create_empty_progress()
        self._save_progress()

