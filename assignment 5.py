POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}

def score(text):
    """+1 per positive word, -1 per negative word; a preceding negator flips it."""
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    for i, w in enumerate(words):
        if w in POSITIVE:
            value = 1
        elif w in NEGATIVE:
            value = -1
        else:
            value = 0
        # flip the sign if the previous word is a negator
        if i > 0 and words[i - 1] in NEGATORS:
            value = -value
        total += value
    return total

def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"

for c in ["Roads are clean and the bus was fast.",
          "Smoke from the factory, air is bad.",
          "The staff were not helpful.",
          "Not bad, service improved."]:
    print(f"{label(c):8} | {c}")
            import re
from collections import Counter

STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "and", "of", "in",
             "to", "it", "this", "that", "for", "on", "with", "from", "at"}

def summarise(text, k=2):
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"[a-z']+", text.lower())
    freq = Counter(w for w in words if w not in STOPWORDS)

    def sentence_score(s):
        return sum(freq
" for w in re.findall(r"[a-z']+", s.lower())
                   if w not in STOPWORDS)

    ranked = sorted(sentences, key=sentence_score, reverse=True)[:k]
    # keep original order
    return ". ".join(s for s in sentences if s in ranked) + "."

def first_k(text, k=2):
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    return ". ".join(sentences[:k]) + "."

# --- agreement with your own manual labels (replace with your 50 complaints) ---
complaints = [
    ("Roads are clean and the bus was fast.", "positive"),
    ("Smoke from the factory, air is bad.", "negative"),
    ("The staff were not helpful.", "negative"),
    ("Not bad, service improved.", "positive"),
    ("Water supply is slow and dirty.", "negative"),
    ("Helpful staff and fast response.", "positive"),
    ("Not very clean.", "negative"),
    ("Oh great, the bus never came.", "negative"),
    ("The park is good but the toilets are broken.", "neutral"),
    ("Street lights are not broken anymore.", "positive"),
]

agree = sum(1 for text, mine in complaints if label(text) == mine)
print(f"Agreement: {agree}/{len(complaints)} = {agree/len(complaints):.0%}")

long_text = ("Smoke from the factory fills the street. The smoke is bad every "
             "morning. Children cough. The factory should stop the smoke.")
print("Frequency summary:", summarise(long_text, 2))
print("First-k summary  :", first_k(long_text, 2))
import sqlite3, time, random

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
data = [(f"S{random.randint(1, 100)}", f"2026-{m:02d}-{d:02d}", random.uniform(10, 200))
        for m in range(1, 13) for d in range(1, 29) for _ in range(300)]
con.executemany("INSERT INTO aq VALUES (?, ?, ?)", data)
con.commit()

def timed_query():
    t = time.perf_counter()
    for _ in range(200):
        con.execute("SELECT AVG(pm25) FROM aq WHERE station = ? AND day = ?",
                    ("S5", "2026-10-10")).fetchone()
    return time.perf_counter() - t

before = timed_query()
con.execute("CREATE INDEX idx_station_day ON aq (station, day)")
after = timed_query()

print(f"Before index: {before:.4f}s")
print(f"After index : {after:.4f}s")
print(f"Speed-up    : {before/after:.1f}x")
con.close()
