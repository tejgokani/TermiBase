"""Challenge bank with predefined SQL challenges."""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class Difficulty(Enum):
    """Challenge difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class Challenge:
    """Represents a single SQL challenge."""
    id: int
    title: str
    description: str
    difficulty: str
    required_concepts: List[str]
    initial_schema: Dict[str, Any]  # Table definitions with CREATE TABLE statements
    initial_data: List[Dict[str, Any]]  # INSERT statements or data
    expected_result: Dict[str, Any]  # Expected query result or query itself
    allowed_operations: List[str]  # SQL operations allowed (SELECT, JOIN, etc.)
    hints: Optional[List[str]] = None
    solution_query: Optional[str] = None  # Reference solution (not shown to user)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert challenge to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Challenge':
        """Create challenge from dictionary."""
        return cls(**data)


class ChallengeBank:
    """Manages the collection of SQL challenges."""
    
    def __init__(self, challenges_file: Optional[Path] = None):
        """Initialize challenge bank.
        
        Args:
            challenges_file: Path to challenges JSON file. If None, uses default location.
        """
        if challenges_file is None:
            # Use package-relative path
            challenges_file = Path(__file__).parent / "challenges.json"
        
        self.challenges_file = challenges_file
        self._challenges: Dict[int, Challenge] = {}
        self._load_challenges()
    
    def _load_challenges(self) -> None:
        """Load challenges from JSON file."""
        if not self.challenges_file.exists():
            # Generate default challenges if file doesn't exist
            self._generate_default_challenges()
            self._save_challenges()
            return
        
        try:
            with open(self.challenges_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for challenge_data in data.get('challenges', []):
                    challenge = Challenge.from_dict(challenge_data)
                    self._challenges[challenge.id] = challenge
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            # If loading fails, generate defaults
            self._generate_default_challenges()
            self._save_challenges()
    
    def _save_challenges(self) -> None:
        """Save challenges to JSON file."""
        # Ensure directory exists
        self.challenges_file.parent.mkdir(parents=True, exist_ok=True)
        
        challenges_data = {
            'challenges': [challenge.to_dict() for challenge in self._challenges.values()]
        }
        with open(self.challenges_file, 'w', encoding='utf-8') as f:
            json.dump(challenges_data, f, indent=2, ensure_ascii=False)
    
    def _generate_default_challenges(self) -> None:
        """Generate 200 truly distinct challenges with unique problem statements and solutions."""
        # Import the distinct challenges module
        from termibase.challenge.distinct_200_challenges import generate_all_200_challenges
        
        # Generate all 200 distinct challenges
        challenges_data = generate_all_200_challenges()
        
        for challenge_data in challenges_data:
            challenge = Challenge.from_dict(challenge_data)
            self._challenges[challenge.id] = challenge
    
    def get_challenge(self, challenge_id: int) -> Optional[Challenge]:
        """Get a challenge by ID.
        
        Args:
            challenge_id: Challenge ID
            
        Returns:
            Challenge object or None if not found
        """
        return self._challenges.get(challenge_id)
    
    def list_challenges(self, difficulty: Optional[str] = None) -> List[Challenge]:
        """List all challenges, optionally filtered by difficulty.
        
        Args:
            difficulty: Optional difficulty filter ('easy', 'medium', 'hard')
            
        Returns:
            List of Challenge objects
        """
        challenges = list(self._challenges.values())
        if difficulty:
            challenges = [c for c in challenges if c.difficulty == difficulty]
        return sorted(challenges, key=lambda c: c.id)
    
    def get_challenge_count(self, difficulty: Optional[str] = None) -> int:
        """Get total number of challenges.
        
        Args:
            difficulty: Optional difficulty filter
            
        Returns:
            Number of challenges
        """
        if difficulty:
            return len([c for c in self._challenges.values() if c.difficulty == difficulty])
        return len(self._challenges)
    
    def setup_challenge_database(self, challenge: Challenge, db_path: str) -> None:
        """Set up a database for a challenge with its schema and initial data.
        
        Args:
            challenge: Challenge object
            db_path: Path to database file
        """
        # Remove existing database if it exists
        if Path(db_path).exists():
            Path(db_path).unlink()
        
        conn = sqlite3.connect(db_path)
        try:
            # Create tables from schema
            for table_name, create_sql in challenge.initial_schema.items():
                conn.execute(create_sql)
            
            # Insert initial data
            for data_entry in challenge.initial_data:
                table = data_entry['table']
                rows = data_entry['data']
                
                if not rows:
                    continue
                
                # Get column names from first row
                first_row = rows[0]
                num_cols = len(first_row)
                placeholders = ','.join(['?'] * num_cols)
                insert_sql = f'INSERT INTO {table} VALUES ({placeholders})'
                
                conn.executemany(insert_sql, rows)
            
            conn.commit()
        finally:
            conn.close()
