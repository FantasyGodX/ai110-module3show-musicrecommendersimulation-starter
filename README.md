# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a small, CLI-first music recommender called **VibeFinder 1.0**. It reads a 20-song catalog from a CSV file, compares every song to a user's "taste profile" (favorite genre, favorite mood, and target energy), and prints the top 5 matches along with the reasons each song scored the way it did.

---

## How The System Works

### How real-world recommenders work

Big platforms like Spotify and YouTube mix two main ideas:

- **Collaborative filtering** predicts what you'll like based on *other people's behavior*. If many users who liked the same songs as you also loved a track you haven't heard, it gets recommended to you. It needs lots of users, but it doesn't need to know anything about the music itself.
- **Content-based filtering** predicts what you'll like based on *the attributes of the songs* (tempo, energy, mood, genre, acousticness). If you keep playing high-energy, upbeat tracks, it finds more tracks with similar attributes. It works for brand-new songs with no listening history.

The data behind these systems includes explicit signals (likes, saves, playlist adds), implicit signals (plays, skips, replays, how long you listened, time of day), and song attributes (genre, mood, tempo, energy, valence, audio analysis). Skips and replays are often more useful than likes because users produce far more of them.

**My version is purely content-based.** There are no other users, so there's nothing to collaborate with. It prioritizes matching the *vibe* of a song to what the user says they want: genre first, then mood, then how close the song's energy is to the user's target energy.

### Features used

**`Song`**: `id`, `title`, `artist`, `genre`, `mood`, `energy` (0-1), `tempo_bpm`, `valence` (0-1), `danceability` (0-1), `acousticness` (0-1). The scorer only uses genre, mood, and energy in version 1; the rest are loaded so they can be added later.

**`UserProfile`** (a dict in `main.py`): `genre` (favorite genre), `mood` (favorite mood), `energy` (target energy, 0-1), and optionally `likes_acoustic`.

### Algorithm Recipe

For each song the score is the sum of:

| Rule | Points |
|------|--------|
| Genre matches the user's favorite genre | **+2.0** |
| Mood matches the user's favorite mood | **+1.0** |
| Energy similarity: `1.0 * (1 - abs(song.energy - user.energy))` | **0.0 to +1.0** |

Maximum score is 4.0. Energy uses *closeness* rather than "higher is better": a user who wants 0.4 energy should not be rewarded for a 0.95 song. Genre is worth more than mood because genre is a stronger boundary: people will skip a metal track on a jazz playlist even if the mood label fits, whereas mood overlaps more between genres.

**Scoring Rule vs. Ranking Rule.** The scoring rule judges *one* song in isolation and returns a number plus reasons. The ranking rule runs the scoring rule over the *whole catalog*, sorts, and keeps the top K. You need both: a score alone doesn't tell you what to show, and a sort without a score has nothing to sort by.

### Data flow

```
User prefs (genre, mood, energy)
        |
        v
For each song in songs.csv:  score_song() -> (score, reasons)
        |
        v
Sort all (song, score, reasons) by score, descending
        |
        v
Top K recommendations printed with explanations
```

### Expected biases

- **Genre dominates.** With +2.0 for genre, a mediocre song in the right genre can outrank a perfect mood/energy match in a different genre.
- **Tiny catalog.** Most genres have just one song, so a user whose favorite genre is "metal" gets one genre match and then essentially energy-ranked filler.
- **Exact-match labels.** "indie pop" gets no credit for being close to "pop", and "chill" gets no credit for being close to "relaxed".
- **Ignored features.** Tempo, valence, danceability, and acousticness don't affect the score yet.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



