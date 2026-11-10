"""Command line runner for the Music Recommender Simulation."""

import sys

from src import recommender
from src.recommender import load_songs, recommend_songs

PROFILES = {
    "Default Pop/Happy": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "High-Energy Pop": {"genre": "pop", "mood": "intense", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    # Adversarial / edge-case profiles
    "Conflicting: high energy + sad": {"genre": "blues", "mood": "sad", "energy": 0.9},
    "Unknown genre (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
    "Mid-everything": {"genre": "folk", "mood": "relaxed", "energy": 0.5},
}


def print_recommendations(name: str, prefs: dict, songs: list, k: int = 5) -> None:
    """Print a formatted top-k list for one profile."""
    print("=" * 64)
    print(f"Profile: {name}  {prefs}")
    print("=" * 64)
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k), 1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}/{song['mood']}]")
        print(f"   Score: {score:.2f} / 4.00")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    if "--experiment" in sys.argv:
        # Weight shift: half the genre weight, double the energy weight.
        recommender.WEIGHTS.update({"genre": 1.0, "energy": 2.0})
        print("EXPERIMENT: genre weight 2.0 -> 1.0, energy weight 1.0 -> 2.0 (max score 4.0)\n")
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")
    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
