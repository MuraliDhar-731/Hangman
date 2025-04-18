import random
import pandas as pd

def select_word_by_difficulty(difficulty):
    try:
        df = pd.read_csv("data/dummy_dataset.csv")
        filtered = df[df["difficulty"].str.lower() == difficulty.lower()]
        return random.choice(filtered["word"].tolist())
    except:
        fallback = {
            "easy": ["cat", "book", "dog"],
            "medium": ["python", "jungle", "rocket"],
            "hard": ["xylophone", "microscope", "quantum"]
        }
        return random.choice(fallback[difficulty.lower()])
