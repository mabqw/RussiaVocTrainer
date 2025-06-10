import streamlit as st
import random
from gtts import gTTS

# ---------------------------
# Vokabelliste (Beispiel, 10 Wörter)
# ---------------------------
vocab = [
    {"ru": "привет", "de": "hallo"},
    {"ru": "пока", "de": "tschüss"},
    {"ru": "спасибо", "de": "danke"},
    {"ru": "да", "de": "ja"},
    {"ru": "нет", "de": "nein"},
    {"ru": "пожалуйста", "de": "bitte"},
    {"ru": "доброе утро", "de": "guten Morgen"},
    {"ru": "добрый вечер", "de": "guten Abend"},
    {"ru": "извините", "de": "Entschuldigung"},
    {"ru": "как дела?", "de": "wie geht's?"}
]

# ---------------------------
# Hilfsfunktionen
# ---------------------------
def play_audio(text, lang="ru"):
    tts = gTTS(text, lang=lang)
    tts.save("audio.mp3")
    audio_file = open("audio.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

def get_random_choices(correct, all_words, key):
    choices = [correct]
    while len(choices) < 4:
        word = random.choice(all_words)[key]
        if word not in choices:
            choices.append(word)
    random.shuffle(choices)
    return choices

# ---------------------------
# Session State
# ---------------------------
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.mode = "Eingabe"

# ---------------------------
# UI: Einstellungen
# ---------------------------
st.title("🇷🇺 Russisch-Vokabeltrainer")
st.sidebar.title("Einstellungen")
num_cards = st.sidebar.slider("Wie viele Vokabeln lernen?", 5, len(vocab), 10)
mode = st.sidebar.radio("Lernmodus", ["Eingabe", "Multiple Choice"])
from_lang = st.sidebar.radio("Was wird gezeigt?", ["🇷🇺 Russisch", "🇩🇪 Deutsch"])
st.session_state.mode = mode

# ---------------------------
# Lernlogik
# ---------------------------
vocab_subset = vocab[:num_cards]
current_index = st.session_state.index % len(vocab_subset)
current_word = vocab_subset[current_index]

source = "ru" if from_lang == "🇷🇺 Russisch" else "de"
target = "de" if source == "ru" else "ru"

source_word = current_word.get(source, "[FEHLT]")
target_word = current_word.get(target, "[FEHLT]")

st.markdown(f"### {source_word}")
if st.button("🔊 Aussprache anhören"):
    play_audio(source_word, lang=source)

if st.session_state.mode == "Eingabe":
    user_input = st.text_input("Übersetzung eingeben:")
    if st.button("Prüfen"):
        st.session_state.total += 1
        if user_input.strip().lower() == target_word.lower():
            st.success("✅ Richtig!")
            st.session_state.correct += 1
            st.session_state.streak += 1
            st.session_state.best_streak = max(st.session_state.streak, st.session_state.best_streak)
        else:
            st.error(f"❌ Falsch. Richtig wäre: {target_word}")
            st.session_state.streak = 0
        st.session_state.index += 1
        st.experimental_rerun()

elif st.session_state.mode == "Multiple Choice":
    choices = get_random_choices(target_word, vocab_subset, target)
    answer = st.radio("Wähle die richtige Übersetzung:", choices)
    if st.button("Antwort prüfen"):
        st.session_state.total += 1
        if answer == target_word:
            st.success("✅ Richtig!")
            st.session_state.correct += 1
            st.session_state.streak += 1
            st.session_state.best_streak = max(st.session_state.streak, st.session_state.best_streak)
        else:
            st.error(f"❌ Falsch. Richtig wäre: {target_word}")
            st.session_state.streak = 0
        st.session_state.index += 1
        st.experimental_rerun()

# ---------------------------
# Fortschrittsanzeige
# ---------------------------
st.sidebar.markdown(f"**Fortschritt**: {st.session_state.correct}/{st.session_state.total} korrekt")
st.sidebar.markdown(f"🔥 Streak: {st.session_state.streak}")
st.sidebar.markdown(f"🏆 Rekord: {st.session_state.best_streak}")
