import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Scoring weights (the "Algorithm Recipe"). Tweak these to run experiments.
WEIGHTS = {"genre": 2.0, "mood": 1.0, "energy": 1.0}


@dataclass
class Song:
    """A song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """A user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user prefs; return (score, list of reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += WEIGHTS["genre"]
        reasons.append(f"genre match (+{WEIGHTS['genre']:.1f})")

    if song["mood"] == user_prefs.get("mood"):
        score += WEIGHTS["mood"]
        reasons.append(f"mood match (+{WEIGHTS['mood']:.1f})")

    if "energy" in user_prefs:
        gap = abs(song["energy"] - user_prefs["energy"])
        points = WEIGHTS["energy"] * (1.0 - gap)
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    # sorted() returns a new list and leaves the original catalog order alone
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


class Recommender:
    """Object-oriented wrapper around the scoring logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        """Convert a UserProfile into the dict format score_song expects."""
        return {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user."""
        prefs = self._prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, s.__dict__)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain in plain text why a song scored the way it did."""
        score, reasons = score_song(self._prefs(user), song.__dict__)
        return f"Score {score:.2f}: " + "; ".join(reasons)
