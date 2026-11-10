# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Intended Use

VibeFinder suggests the top 5 songs from a small catalog that best match a user's favorite genre, favorite mood, and target energy level. It also explains each pick in plain words.

It assumes the user can describe their taste with one genre, one mood, and one energy number. It is built for classroom exploration. It is **not** meant for real users or a real music app.

**Not intended for:** making decisions about real people, replacing a real streaming service, judging what music is "good", or any use where a wrong suggestion could cause harm.

---

## 3. How the Model Works

Every song gets points. The songs with the most points win.

- **+2.0 points** if the song's genre is the user's favorite genre.
- **+1.0 point** if the song's mood is the user's favorite mood.
- **Up to +1.0 point for energy.** The closer the song's energy is to what the user wants, the more points. A song that matches exactly gets 1.0. A song that is as far away as possible gets 0. Higher energy is *not* automatically better. Closer is better.

The top 5 scores are shown, with a list of reasons such as "genre match (+2.0)". The maximum possible score is 4.0.

I changed the starter logic by filling in the empty functions. I also added a `--experiment` switch that shifts the weights so I could test how sensitive the system is.

---

## 4. Data

- **20 songs** in `data/songs.csv`. The starter had 10. I added 10 more.
- **Genres:** pop, indie pop, lofi, rock, ambient, jazz, synthwave, r&b, country, hip hop, edm, classical, metal, latin, folk, blues, reggae. Lofi has 3 songs and pop has 2. Every other genre has 1.
- **Moods:** happy, chill, intense, relaxed, moody, focused, romantic, nostalgic, confident, euphoric, serene, angry, joyful, melancholy, sad.
- **Numbers per song:** energy, tempo, valence, danceability, acousticness (all 0 to 1 except tempo).
- **Missing:** lyrics, language, artist popularity, release year, and anything about what real listeners do. Twenty songs is far too small to represent real taste. The labels were also picked by hand, so they reflect my opinions.

---

## 5. Strengths

- It works well for users whose taste matches a well-covered genre, like **lofi** or **rock**. The top results for "Chill Lofi" and "Deep Intense Rock" matched my intuition right away.
- Rewarding *closeness* in energy works. A chill listener is not handed loud songs just because they have high energy numbers.
- The reasons list makes every result easy to check. I could see exactly why each song was ranked.
- When the genre isn't in the catalog (k-pop), it falls back to mood and energy and still gives sensible happy, mid-high energy songs.

---

## 6. Limitations and Bias

The system over-trusts genre. A genre match is worth 2.0 points, which is twice a mood match and more than the whole energy score. That means a song in the right genre can beat a song that is a much better match for the mood and energy. The clearest example is **Gym Hero**, an intense workout pop song. It keeps showing up for "happy pop" listeners because it gets the full +2.0 for being pop and loses almost nothing on energy. A happy pop fan probably wanted something sunnier. The catalog makes this worse: most genres have just one song, so users of those genres get one good result and then a list sorted only by energy. Finally, labels must match exactly, so "indie pop" gets no credit for being close to "pop".

---

## 7. Evaluation

**Profiles tested (7):** Default Pop/Happy, High-Energy Pop, Chill Lofi, Deep Intense Rock, plus three edge cases: Conflicting (blues + sad + energy 0.9), Unknown genre (k-pop), and Mid-everything (folk + relaxed + energy 0.5). I looked for whether the top pick made sense and whether the same song kept showing up everywhere.

### Terminal output (top 5 per profile)

**Default Pop/Happy**

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

**High-Energy Pop**

```
Profile: High-Energy Pop  {'genre': 'pop', 'mood': 'intense', 'energy': 0.9}
1. Gym Hero by Max Pulse  [pop/intense]
   Score: 3.97 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.93 vs target 0.90 (+0.97)
2. Sunrise City by Neon Echo  [pop/happy]
   Score: 2.92 / 4.00
     - genre match (+2.0)
     - energy 0.82 vs target 0.90 (+0.92)
3. Storm Runner by Voltline  [rock/intense]
   Score: 1.99 / 4.00
     - mood match (+1.0)
     - energy 0.91 vs target 0.90 (+0.99)
4. Neon Pulse by Kiko Strobe  [edm/euphoric]
   Score: 0.94 / 4.00
     - energy 0.96 vs target 0.90 (+0.94)
5. Burn the Map by Ashgrid  [metal/angry]
   Score: 0.93 / 4.00
     - energy 0.97 vs target 0.90 (+0.93)
```

**Chill Lofi**

```
Profile: Chill Lofi  {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
1. Library Rain by Paper Lanterns  [lofi/chill]
   Score: 4.00 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.35 vs target 0.35 (+1.00)
2. Midnight Coding by LoRoom  [lofi/chill]
   Score: 3.93 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.42 vs target 0.35 (+0.93)
3. Focus Flow by LoRoom  [lofi/focused]
   Score: 2.95 / 4.00
     - genre match (+2.0)
     - energy 0.40 vs target 0.35 (+0.95)
4. Spacewalk Thoughts by Orbit Bloom  [ambient/chill]
   Score: 1.93 / 4.00
     - mood match (+1.0)
     - energy 0.28 vs target 0.35 (+0.93)
5. Coffee Shop Stories by Slow Stereo  [jazz/relaxed]
   Score: 0.98 / 4.00
     - energy 0.37 vs target 0.35 (+0.98)
```

**Deep Intense Rock**

```
Profile: Deep Intense Rock  {'genre': 'rock', 'mood': 'intense', 'energy': 0.92}
1. Storm Runner by Voltline  [rock/intense]
   Score: 3.99 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.91 vs target 0.92 (+0.99)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 1.99 / 4.00
     - mood match (+1.0)
     - energy 0.93 vs target 0.92 (+0.99)
3. Neon Pulse by Kiko Strobe  [edm/euphoric]
   Score: 0.96 / 4.00
     - energy 0.96 vs target 0.92 (+0.96)
4. Burn the Map by Ashgrid  [metal/angry]
   Score: 0.95 / 4.00
     - energy 0.97 vs target 0.92 (+0.95)
5. Sunrise City by Neon Echo  [pop/happy]
   Score: 0.90 / 4.00
     - energy 0.82 vs target 0.92 (+0.90)
```

**Conflicting: high energy + sad**

```
Profile: Conflicting: high energy + sad  {'genre': 'blues', 'mood': 'sad', 'energy': 0.9}
1. Blue Monday Groove by The Brass Notes  [blues/sad]
   Score: 3.48 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.38 vs target 0.90 (+0.48)
2. Storm Runner by Voltline  [rock/intense]
   Score: 0.99 / 4.00
     - energy 0.91 vs target 0.90 (+0.99)
3. Gym Hero by Max Pulse  [pop/intense]
   Score: 0.97 / 4.00
     - energy 0.93 vs target 0.90 (+0.97)
4. Neon Pulse by Kiko Strobe  [edm/euphoric]
   Score: 0.94 / 4.00
     - energy 0.96 vs target 0.90 (+0.94)
5. Burn the Map by Ashgrid  [metal/angry]
   Score: 0.93 / 4.00
     - energy 0.97 vs target 0.90 (+0.93)
```

**Unknown genre (k-pop)**

```
Profile: Unknown genre (k-pop)  {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7}
1. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 1.94 / 4.00
     - mood match (+1.0)
     - energy 0.76 vs target 0.70 (+0.94)
2. Sunrise City by Neon Echo  [pop/happy]
   Score: 1.88 / 4.00
     - mood match (+1.0)
     - energy 0.82 vs target 0.70 (+0.88)
3. Night Drive Loop by Neon Echo  [synthwave/moody]
   Score: 0.95 / 4.00
     - energy 0.75 vs target 0.70 (+0.95)
4. Concrete Crown by Tre Valdez  [hip hop/confident]
   Score: 0.92 / 4.00
     - energy 0.78 vs target 0.70 (+0.92)
5. Salt & Sunday by Marisol Vega  [latin/joyful]
   Score: 0.90 / 4.00
     - energy 0.80 vs target 0.70 (+0.90)
```

**Mid-everything**

```
Profile: Mid-everything  {'genre': 'folk', 'mood': 'relaxed', 'energy': 0.5}
1. Porch Light Folk by Willow Creek  [folk/melancholy]
   Score: 2.80 / 4.00
     - genre match (+2.0)
     - energy 0.30 vs target 0.50 (+0.80)
2. Island Drift by Coral Tide  [reggae/relaxed]
   Score: 1.95 / 4.00
     - mood match (+1.0)
     - energy 0.55 vs target 0.50 (+0.95)
3. Coffee Shop Stories by Slow Stereo  [jazz/relaxed]
   Score: 1.87 / 4.00
     - mood match (+1.0)
     - energy 0.37 vs target 0.50 (+0.87)
4. Dust Road Home by Hollow Pines  [country/nostalgic]
   Score: 0.98 / 4.00
     - energy 0.48 vs target 0.50 (+0.98)
5. Velvet Hours by Sable June  [r&b/romantic]
   Score: 0.95 / 4.00
     - energy 0.55 vs target 0.50 (+0.95)
```

### What surprised me

- **Gym Hero** appears for both "Default Pop/Happy" (#2) and "High-Energy Pop" (#1). For the second profile that is correct. For the first, it is a loud workout song showing up for someone who just wants happy pop. In plain words: the system sees "pop" and "high energy" and stops thinking. It does not know the song is about sweating at the gym, not smiling in the sun.
- For the **conflicting** profile (sad but high energy), the system picked the one sad blues song and then dropped straight to loud songs that were not sad at all. There is no song that is both, so the system just splits the difference badly.
- The **k-pop** profile had no genre match for any song, so the best score was only 1.94 out of 4. The system still returned results, but it gave no sign that it was guessing.

### Why Gym Hero ranks #2 for Default Pop/Happy

Sunrise City is #1 because it matches on genre (+2.0), mood (+1.0) and has nearly the same energy (+0.98). Gym Hero gets +2.0 for being pop and +0.87 for energy (0.93 vs 0.80), but no mood points. That adds to 2.87. The next best song, Rooftop Lights, matches the mood but not the genre label, so it only gets 1.96. Because the genre bonus is so big, Gym Hero beats a song that is a better emotional match.

### Profile-pair comparisons

- **Default Pop/Happy vs High-Energy Pop:** Both pick pop songs first, but the order flips. Happy wants Sunrise City on top. Intense wants Gym Hero on top. That makes sense, because the only difference is the mood (happy vs intense) and the energy target (0.8 vs 0.9). Rock and EDM songs also show up for the high-energy user, which is right for someone who wants intensity.
- **Default Pop/Happy vs Chill Lofi:** Almost no overlap. Pop/happy returns bright, mid-high energy songs. Lofi returns quiet, acoustic songs like Library Rain and Midnight Coding. These two users want opposite things, and the system treats them that way.
- **Chill Lofi vs Deep Intense Rock:** Complete opposites. Lofi's top 5 sits at energy 0.28 to 0.42, rock's top 5 sits at 0.82 to 0.97. The system correctly separates "calm study music" from "loud and aggressive".
- **High-Energy Pop vs Deep Intense Rock:** They share Gym Hero and Storm Runner (both intense, both high energy), but swap order based on genre. Pop users get Gym Hero first, rock users get Storm Runner first. That is the genre weight doing exactly what it was designed to do.
- **Deep Intense Rock vs Conflicting (blues/sad/0.9):** Both want very high energy, so after the top pick both lists fill up with loud songs like Gym Hero and Burn the Map. The #1 differs: Storm Runner (a real match) vs Blue Monday Groove (a low-energy song that wins on genre and mood alone, with a weak 0.48 energy score). The genre and mood bonuses can overpower the energy request.
- **Chill Lofi vs Mid-everything (folk/relaxed/0.5):** Both are calm users, but Mid-everything has only one folk song, so after "Porch Light Folk" the list is made of relaxed songs from other genres like reggae and jazz. Lofi has three songs in its genre, so it gets a full, focused list. This shows the dataset is uneven, not that the logic is different.

### Experiment: weight shift

I halved the genre weight (2.0 to 1.0) and doubled the energy weight (1.0 to 2.0). Gym Hero fell from #2 to #3 for the Default profile, which felt more right. In the Mid-everything profile, the folk song dropped from #1 to #3 because its energy was off. So the change made results different, and for happy pop and relaxed folk arguably better. The math stays valid: the max score is still 4.0, since 1.0 + 1.0 + 2.0 = 4.0. Full details are in the README.

---

## 8. Future Work

- Score more features: valence, danceability, acousticness, and tempo, so "vibe" is more than three numbers.
- Treat similar labels as partially matching (for example, "indie pop" is close to "pop", "chill" is close to "relaxed").
- Add a diversity rule so the top 5 does not contain several songs from the same artist or genre.
- Let users give more than one favorite genre or mood.
- Tell the user when no song matched well, instead of presenting weak results with confidence.

---

## 9. Personal Reflection

My biggest learning moment was the weight experiment. I did not add any songs or any new rules, but when I changed two numbers the top 5 lists changed. That showed me that a recommender is not neutral: whoever picks the weights is deciding what "good" means.

AI tools helped me move quickly. They explained collaborative vs content-based filtering, suggested the closeness formula for energy (1 - abs(gap)), and helped me draft the code and tests. But I had to double-check them. The first version of my experiment flag had a broken string, and I only caught it by actually running the program. I also checked scores by hand for specific songs, because a number that looks plausible can still be wrong.

What surprised me most is how real a simple system can feel. With only three rules, "Chill Lofi" gives a believable study playlist. It is easy to forget that nothing is being understood: the program is just adding up points. That also helped me see why real recommendation apps can feel smart while still making weird choices, like Gym Hero for happy pop fans.

If I extended this project, I would add the unused features (valence, danceability, acousticness), use partial credit for similar genres and moods, add a diversity penalty, and grow the catalog to a few hundred songs so that no genre depends on a single track.
