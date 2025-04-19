def initialize_game(word, max_lives=6):
    return {
        "word": word.lower(),
        "masked_word": ["_" for _ in word],
        "guessed": [],
        "lives": max_lives,
        "won": False,
        "lost": False,
        "last_feedback": ""
    }

def update_game_state(game, guess):
    guess = guess.lower()

    if game["won"] or game["lost"]:
        return

    game["guessed"].append(guess)

    if guess == game["word"]:
        game["masked_word"] = list(game["word"])
        game["won"] = True
        game["last_feedback"] = "🟩" * len(guess)
        return

    # Feedback emoji logic
    feedback = []
    target = list(game["word"])
    used = [False] * len(target)

    # First pass: correct positions
    for i in range(len(guess)):
        if i < len(target) and guess[i] == target[i]:
            feedback.append("🟩")
            used[i] = True
        else:
            feedback.append(None)

    # Second pass: check for misplaced letters
    for i in range(len(guess)):
        if feedback[i] is not None:
            continue
        if guess[i] in target:
            for j in range(len(target)):
                if not used[j] and guess[i] == target[j]:
                    feedback[i] = "🟨"
                    used[j] = True
                    break
        if feedback[i] is None:
            feedback[i] = "⬛"

    # Reveal correct-position letters only
    for i in range(len(game["word"])):
        if i < len(guess) and game["word"][i] == guess[i]:
            game["masked_word"][i] = guess[i]

    game["last_feedback"] = "".join(feedback)
    game["lives"] -= 1

    if game["lives"] <= 0:
        game["lost"] = True
    elif "".join(game["masked_word"]) == game["word"]:
        game["won"] = True
