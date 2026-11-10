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

Default "pop/happy" profile (`python -m src.main`):

```
Profile: Default Pop/Happy  {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 3.98 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.80 (+0.98)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 2.87 / 4.00
     - genre match (+2.0)
     - energy 0.93 vs target 0.80 (+0.87)
3. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 1.96 / 4.00
     - mood match (+1.0)
     - energy 0.76 vs target 0.80 (+0.96)
4. Salt & Sunday by Marisol Vega  [latin/joyful]
   Score: 1.00 / 4.00
     - energy 0.80 vs target 0.80 (+1.00)
5. Concrete Crown by Tre Valdez  [hip hop/confident]
   Score: 0.98 / 4.00
     - energy 0.78 vs target 0.80 (+0.98)
```

The runner prints results for 7 profiles. See `model_card.md` for the rest.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Experiment: weight shift

I halved the genre weight (2.0 -> 1.0) and doubled the energy weight (1.0 -> 2.0), so the max score stays 4.0. Run it with `python -m src.main --experiment`.

What changed:

- **Default Pop/Happy:** "Gym Hero" (pop/intense) dropped from #2 to #3. "Rooftop Lights" (indie pop/happy) moved up to #2. That feels more right for a happy listener.
- **Mid-everything (folk/relaxed/0.5):** the folk song "Porch Light Folk" fell from #1 to #3 because its energy (0.30) is far from 0.5. Two "relaxed" songs closer in energy took over.
- **Conflicting (blues/sad/0.9):** the top song's score fell from 3.48 to 2.96 because the energy mismatch now hurts twice as much.
- **Chill Lofi / Deep Rock:** top picks did not change.

Verdict: the experiment made results *different*, and for pop/happy and folk/relaxed arguably *better*, because the system stopped treating genre as a wall. It also made it slightly easier for loud songs from the wrong genre to sneak in for the conflicting profile. Neither setting is "right"; it depends on whether the user cares more about genre or about feel.

Other things I tried while testing: a genre that isn't in the catalog (`k-pop`), and a conflicting profile (high energy + sad).

---

## Limitations and Risks

- The catalog is tiny (20 songs). Most genres have exactly one song, so after the genre match the list fills up with songs ranked only by energy.
- Genre and mood are exact-string matches. "indie pop" gets no credit for pop, and "relaxed" gets no credit for "chill".
- Tempo, valence, danceability, and acousticness are loaded but never scored.
- A strong genre match can bury better mood/energy matches. Gym Hero (pop, intense) shows up for "happy pop" fans just because it is pop and loud.
- It has no idea what the user has already heard, and it has no other users to learn from.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this showed me that a recommender is really just two small ideas: score one item, then sort everything by score. The "intelligence" is in the weights I picked, and those are my opinions. When I doubled the energy weight, the top songs changed without any new data, which means the person who sets the weights quietly decides what a "good" recommendation is. The reasons list was the most useful part: seeing "genre match (+2.0)" made it easy to spot why a song was ranked where it was.

Bias shows up in the data and the rules. Mine only knows 20 songs and one label per genre, so someone who likes k-pop or metal gets worse results than someone who likes pop or lofi. In a real product the same thing would happen at scale: whoever is well represented in the data gets better recommendations. See [the model card](model_card.md) for the full write-up.
