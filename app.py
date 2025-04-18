import streamlit as st
import random
import time
from game.hangman_logic import initialize_game, update_game_state
from game.word_selector import select_word_by_difficulty
from game.timer import start_timer, stop_timer

st.set_page_config(page_title="ML Hangman", layout="centered")
st.title("🎯 ML Word Predictor Game (Hangman Style)")

if "game_state" not in st.session_state:
    st.session_state.game_state = None

if "start_time" not in st.session_state:
    st.session_state.start_time = None

difficulty = st.selectbox("Choose Difficulty", ["Easy", "Medium", "Hard"])

if st.button("🎮 Start New Game"):
    word = select_word_by_difficulty(difficulty)
    st.session_state.game_state = initialize_game(word)
    st.session_state.start_time = start_timer()

if st.session_state.game_state:
    game = st.session_state.game_state
    masked_word = " ".join(game["masked_word"])
    st.subheader(f"Word: {masked_word}")
    st.markdown(f"🧠 Difficulty: **{difficulty}**")
    st.markdown(f"❤️ Lives Left: **{game['lives']}**")
    st.markdown(f"🔠 Guessed Letters: `{', '.join(game['guessed'])}`")

    guess = st.text_input("Your Guess (1 letter):", max_chars=1)

    if guess:
        update_game_state(st.session_state.game_state, guess.lower())
        st.rerun()

    if game["won"]:
        duration = stop_timer(st.session_state.start_time)
        st.success(f"🎉 You guessed the word: `{game['word']}`")
        st.info(f"⏱️ Time played: {duration:.2f} minutes")
        st.session_state.game_state = None

    elif game["lost"]:
        duration = stop_timer(st.session_state.start_time)
        st.error(f"💥 You lost! The word was: `{game['word']}`")
        st.info(f"⏱️ Time played: {duration:.2f} minutes")
        st.session_state.game_state = None
