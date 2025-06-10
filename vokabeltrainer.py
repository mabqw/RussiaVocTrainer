import streamlit as st
import random
import json
import os
from gtts import gTTS

# ---------------------------
# Speicherpfad definieren
# ---------------------------
SAVE_FILE = "trainer_data.json"

# ---------------------------
# Funktionen zur Datenspeicherung
# ---------------------------
def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "progress": {
                "correct_answers": 0,
                "total_attempts": 0,
                "streak": 0,
                "best_streak": 0
            },
            "learned_words": {},
            "settings": {
                "max_words": 10
            }
        }

def save_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------------------------
# Audiofunktion
# ---------------------------
def play_audio(text, lang="ru"):
    tts = gTTS(text, lang=lang)
    tts.save("audio.mp3")
    audio_file = open("audio.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

# ---------------------------
# Vokabelliste
# ---------------------------
vocab = [
    {"ru": "и", "de": "and"},
    {"ru": "в", "de": "in"},
    {"ru": "не", "de": "not"},
    {"ru": "он", "de": "he"},
    {"ru": "на", "de": "on, at"},
    {"ru": "я", "de": "I"},
    {"ru": "что", "de": "what, that"},
    {"ru": "тот", "de": "that"},
    {"ru": "быть", "de": "to be"},
    {"ru": "с", "de": "with"},
    {"ru": "а", "de": "but"},
    {"ru": "весь", "de": "all"},
    {"ru": "это", "de": "this, it"},
    {"ru": "как", "de": "how, like"},
    {"ru": "она", "de": "she"},
    {"ru": "по", "de": "along, by, according to"},
    {"ru": "но", "de": "but"},
    {"ru": "они", "de": "they"},
    {"ru": "к", "de": "to"},
    {"ru": "у", "de": "at, by"},
    {"ru": "ты", "de": "you (informal)"},
    {"ru": "из", "de": "from, out of"},
    {"ru": "мы", "de": "we"},
    {"ru": "за", "de": "behind, for"},
    {"ru": "вы", "de": "you (formal or plural)"},
    {"ru": "так", "de": "so, thus"},
    {"ru": "же", "de": "same, also"},
    {"ru": "от", "de": "from, of"},
    {"ru": "сказать", "de": "to say"},
    {"ru": "этот", "de": "this"},
    {"ru": "который", "de": "which, who"},
    {"ru": "мочь", "de": "can, to be able"},
    {"ru": "человек", "de": "person"}
]

# ---------------------------
# Hilfsfunktionen
# ---------------------------
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
if "data" not in st.session_state:
    st.session_state.data = load_data()

if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.mode = "Eingabe"
    st.session_state.selected_choice = None

# ---------------------------
# UI: Einstellungen
# ---------------------------
st.title("🇷🇺 Russisch-Vokabeltrainer")
st.sidebar.title("Einstellungen")
num_cards = st.sidebar.slider("Wie viele Vokabeln lernen?", 5, len(vocab), st.session_state.data["settings"].get("max_words", 10))
mode = st.sidebar.radio("Lernmodus", ["Eingabe", "Multiple Choice"])
from_lang = st.sidebar.radio("Was wird gezeigt?", ["🇷🇺 Russisch", "🇩🇪 Deutsch"])

st.session_state.data["settings"]["max_words"] = num_cards
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

if mode == "Eingabe":
    user_input = st.text_input("Übersetzung eingeben:")
    if st.button("Prüfen"):
        st.session_state.data["progress"]["total_attempts"] += 1
        if user_input.strip().lower() == target_word.lower():
            st.success("✅ Richtig!")
            st.session_state.data["progress"]["correct_answers"] += 1
            st.session_state.data["progress"]["streak"] += 1
        else:
            st.error(f"❌ Falsch. Richtig wäre: {target_word}")
            st.session_state.data["progress"]["streak"] = 0
        st.session_state.data["progress"]["best_streak"] = max(
            st.session_state.data["progress"]["best_streak"],
            st.session_state.data["progress"]["streak"]
        )
        st.session_state.index += 1
        save_data(st.session_state.data)
        st.rerun()

elif mode == "Multiple Choice":
    correct_answer = target_word
    if "choices" not in st.session_state or st.session_state.get("last_index") != st.session_state.index:
        st.session_state.choices = get_random_choices(correct_answer, vocab_subset, target)
        st.session_state.last_index = st.session_state.index
        st.session_state.selected_choice = None

    st.session_state.selected_choice = st.radio(
        "Wähle die richtige Übersetzung:",
        st.session_state.choices,
        index=st.session_state.choices.index(st.session_state.selected_choice)
        if st.session_state.selected_choice in st.session_state.choices else 0,
        key="radio_choice"
    )

    if st.button("Antwort prüfen"):
        st.session_state.data["progress"]["total_attempts"] += 1
        if st.session_state.selected_choice == correct_answer:
            st.success("✅ Richtig!")
            st.session_state.data["progress"]["correct_answers"] += 1
            st.session_state.data["progress"]["streak"] += 1
        else:
            st.error(f"❌ Falsch. Richtig wäre: {correct_answer}")
            st.session_state.data["progress"]["streak"] = 0

        st.session_state.data["progress"]["best_streak"] = max(
            st.session_state.data["progress"]["best_streak"],
            st.session_state.data["progress"]["streak"]
        )

        st.session_state.index += 1
        st.session_state.pop("choices", None)
        st.session_state.pop("selected_choice", None)
        save_data(st.session_state.data)
        st.rerun()

# ---------------------------
# Fortschrittsanzeige
# ---------------------------
p = st.session_state.data["progress"]
st.sidebar.markdown(f"**Fortschritt**: {p['correct_answers']}/{p['total_attempts']} korrekt")
st.sidebar.markdown(f"🔥 Streak: {p['streak']}")
st.sidebar.markdown(f"🏆 Rekord: {p['best_streak']}")
