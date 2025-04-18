def initialize_game(word, max_lives=6):
    return {
        "word": word.lower(),
        "masked_word": ["_" for _ in word],
        "guessed": [],
        "lives": max_lives,
        "won": False,
        "lost": False
    }

def update_game_state(game, letter):
    if letter in game["guessed"] or game["won"] or game["lost"]:
        return

    game["guessed"].append(letter)

    if letter in game["word"]:
        for i, c in enumerate(game["word"]):
            if c == letter:
                game["masked_word"][i] = c
    else:
        game["lives"] -= 1

    if "_" not in game["masked_word"]:
        game["won"] = True
    elif game["lives"] <= 0:
        game["lost"] = True
