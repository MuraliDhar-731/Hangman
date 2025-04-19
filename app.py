import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from streamlit.components.v1 import html

from game.hangman_logic import initialize_game, update_game_state
from game.word_selector import select_word_by_difficulty
from game.timer import start_timer, stop_timer

st.set_page_config(page_title="WordBlitzML", layout="centered")
st.title("🎯 WordBlitzML – Full-Word ML Guessing Game")

# Session state
if "game_state" not in st.session_state:
    st.session_state.game_state = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "stats" not in st.session_state:
    st.session_state.stats = {
        "wins": 0,
        "losses": 0,
        "games": 0,
        "streak": 0,
        "best_time": None
    }
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# Select difficulty
difficulty = st.selectbox("Choose Difficulty", ["Easy", "Medium", "Hard"])

# Start new game
if st.button("🎮 Start New Game"):
    word = select_word_by_difficulty(difficulty)
    st.session_state.game_state = initialize_game(word)
    st.session_state.start_time = start_timer()

# Game UI
if st.session_state.game_state:
    game = st.session_state.game_state
    masked = " ".join(game["masked_word"])
    st.subheader(f"Word: {masked}")
    st.markdown(f"🧠 Difficulty: **{difficulty}**")
    st.markdown(f"❤️ Lives Left: **{game['lives']}**")
    st.markdown(f"🔡 Guesses: `{', '.join(game['guessed'])}`")

    # Input full word
    guess = st.text_input("Guess the full word:", max_chars=len(game["word"]), key="guess_input")

    if guess:
        update_game_state(game, guess)
        st.rerun()

    if "last_feedback" in game and game["last_feedback"]:
        st.markdown(f"🧩 Feedback: `{game['last_feedback']}`")

    # --- WIN ---
    if game["won"]:
        st.balloons()
        duration = stop_timer(st.session_state.start_time)
        st.success(f"🏆 You guessed it! The word was `{game['word']}`")
        st.markdown(f"⏱️ **Time Taken**: `{duration:.2f}` minutes")
        st.session_state.stats["wins"] += 1
        st.session_state.stats["games"] += 1
        st.session_state.stats["streak"] += 1

        # Best time update
        best_time = st.session_state.stats["best_time"]
        if best_time is None or duration < best_time:
            st.session_state.stats["best_time"] = duration
            st.success(f"🥇 New Record! Fastest time: `{duration:.2f}` minutes")

        # Leaderboard input
        name = st.text_input("Enter your name for the leaderboard:", max_chars=20, key="lb_name")
        if name:
            st.session_state.leaderboard.append({
                "name": name,
                "time": duration,
                "date": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            st.session_state.leaderboard = sorted(
                st.session_state.leaderboard, key=lambda x: x["time"]
            )[:5]
            st.success("✅ Added to leaderboard!")

        st.session_state.game_state = None

    # --- LOSS ---
    elif game["lost"]:
        duration = stop_timer(st.session_state.start_time)
        st.error(f"💥 You lost! The word was `{game['word']}`")
        st.markdown(f"⏱️ **Time Taken**: `{duration:.2f}` minutes")
        st.session_state.stats["losses"] += 1
        st.session_state.stats["games"] += 1
        st.session_state.stats["streak"] = 0
        st.session_state.game_state = None

# 📊 Dashboard
with st.expander("📊 View Win/Loss Dashboard"):
    stats = st.session_state.stats
    win_rate = (stats["wins"] / stats["games"] * 100) if stats["games"] > 0 else 0
    st.markdown(f"✅ **Wins**: {stats['wins']}")
    st.markdown(f"❌ **Losses**: {stats['losses']}")
    st.markdown(f"🎮 **Games Played**: {stats['games']}")
    st.markdown(f"🔥 **Current Streak**: {stats['streak']}")
    st.markdown(f"📈 **Win Rate**: `{win_rate:.1f}%`")
    if stats["best_time"] is not None:
        st.markdown(f"🥇 **Fastest Win Time**: `{stats['best_time']:.2f}` minutes")

    wins = stats["wins"]
    losses = stats["losses"]
    if wins == 0 and losses == 0:
        st.info("📊 Play a few games to generate the chart.")
    elif wins > 0 and losses > 0:
        fig, ax = plt.subplots()
        ax.pie([wins, losses], labels=["Wins", "Losses"],
               colors=["#00cc44", "#ff4d4d"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    elif wins > 0:
        st.success(f"🎉 All games won! Total wins: {wins}")
    elif losses > 0:
        st.error(f"😢 All games lost! Total losses: {losses}")

# 🏆 Leaderboard
if st.session_state.leaderboard:
    st.markdown("### 🏆 Local Leaderboard (Top 5 Fastest Wins)")
    for i, entry in enumerate(st.session_state.leaderboard, 1):
        st.markdown(f"{i}. `{entry['name']}` — ⏱️ `{entry['time']:.2f}` min — 📅 {entry['date']}")

# 🔄 Reset
if st.button("🔄 Reset Stats & Leaderboard"):
    st.session_state.stats = {
        "wins": 0, "losses": 0, "games": 0, "streak": 0, "best_time": None
    }
    st.session_state.leaderboard = []
    st.success("✅ Stats and leaderboard reset!")
