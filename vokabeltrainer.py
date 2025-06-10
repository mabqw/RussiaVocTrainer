import streamlit as st
import random
import json
import os
from gtts import gTTS

# ---------------------------
# Laden der Vokabeln
# ---------------------------
vocab = [
    ("и", "and"), ("в", "in"), ("не", "not"), ("он", "he"), ("на", "on, at"),
    ("я", "I"), ("что", "what, that"), ("тот", "that"), ("быть", "to be"),
    ("с", "with"), ("а", "but"), ("весь", "all"), ("это", "this, it"),
    ("как", "how, like"), ("она", "she"), ("по", "along, by, according to"),
    ("но", "but"), ("они", "they"), ("к", "to"), ("у", "at, by"),
    ("ты", "you (informal)"), ("из", "from, out of"), ("мы", "we"),
    ("за", "behind, for"), ("вы", "you (formal or plural)"), ("так", "so, thus"),
    ("же", "same, also"), ("от", "from, of"), ("сказать", "to say"),
    ("этот", "this"), ("который", "which, who"), ("мочь", "can, to be able"),
    ("человек", "person"), ("о", "about"), ("один", "one"), ("ещё", "still, yet"),
    ("бы", "would"), ("такой", "such"), ("только", "only"), ("себя", "oneself"),
    ("своё", "one's own"), ("какой", "what kind, which"), ("когда", "when"),
    ("уже", "already"), ("для", "for"), ("вот", "here is, there is"),
    ("кто", "who"), ("да", "yes"), ("говорить", "to speak, say"),
    ("год", "year"), ("знать", "to know"), ("мой", "my"), ("до", "until, before"),
    ("или", "or"), ("если", "if"), ("время", "time"), ("рука", "hand"),
    ("нет", "no, not"), ("самый", "most, the very"), ("ни", "neither, nor"),
    ("стать", "to become"), ("большой", "big"), ("даже", "even"),
    ("другой", "other"), ("наш", "our"), ("под", "under"), ("где", "where"),
    ("дело", "matter, affair"), ("есть", "to be, to have (there is)"),
    ("хорошо", "well, good"), ("надо", "need to"), ("тогда", "then"),
    ("сейчас", "now"), ("сам", "self"), ("чтобы", "in order to, so that"),
    ("раз", "time, once"), ("два", "two"), ("там", "there"), ("чем", "than"),
    ("глаз", "eye"), ("жизнь", "life"), ("первый", "first"), ("день", "day"),
    ("тут", "here"), ("во", "in (variant of 'в')"), ("ничего", "nothing"),
    ("потом", "then, later"), ("очень", "very"), ("со", "with (variant of 'с')"),
    ("хотеть", "to want"), ("лицо", "face"), ("после", "after"),
    ("новый", "new"), ("без", "without"), ("говорить", "to speak"),
    ("ходить", "to go (by foot, regularly)"), ("думать", "to think"),
    ("спросить", "to ask"), ("видеть", "to see"), ("стоять", "to stand")
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
current_word = vocab_subset[st.session_state.index % len(vocab_subset)]

source = "ru" if from_lang == "🇷🇺 Russisch" else "de"
target = "de" if source == "ru" else "ru"

st.markdown(f"### {current_word[source]}")
if st.button("🔊 Aussprache anhören"):
    play_audio(current_word[source], lang=source)

user_input = ""
correct = current_word[target]

if st.session_state.mode == "Eingabe":
    user_input = st.text_input("Übersetzung eingeben:")
    if st.button("Prüfen"):
        st.session_state.total += 1
        if user_input.strip().lower() == correct.lower():
            st.success("✅ Richtig!")
            st.session_state.correct += 1
            st.session_state.streak += 1
            st.session_state.best_streak = max(st.session_state.streak, st.session_state.best_streak)
        else:
            st.error(f"❌ Falsch. Richtig wäre: {correct}")
            st.session_state.streak = 0
        st.session_state.index += 1
        st.experimental_rerun()

elif st.session_state.mode == "Multiple Choice":
    choices = get_random_choices(correct, vocab_subset, target)
    answer = st.radio("Wähle die richtige Übersetzung:", choices)
    if st.button("Antwort prüfen"):
        st.session_state.total += 1
        if answer == correct:
            st.success("✅ Richtig!")
            st.session_state.correct += 1
            st.session_state.streak += 1
            st.session_state.best_streak = max(st.session_state.streak, st.session_state.best_streak)
        else:
            st.error(f"❌ Falsch. Richtig wäre: {correct}")
            st.session_state.streak = 0
        st.session_state.index += 1
        st.experimental_rerun()

# ---------------------------
# Fortschrittsanzeige
# ---------------------------
st.sidebar.markdown(f"**Fortschritt**: {st.session_state.correct}/{st.session_state.total} korrekt")
st.sidebar.markdown(f"🔥 Streak: {st.session_state.streak}")
st.sidebar.markdown(f"🏆 Rekord: {st.session_state.best_streak}")
