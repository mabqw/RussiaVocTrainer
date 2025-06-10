import streamlit as st
import random
from gtts import gTTS
import matplotlib.pyplot as plt
import pandas as pd
import os
import json

# ---------------------------
# Konstante für Datei zur Fortschrittsspeicherung
# ---------------------------
PROGRESS_FILE = "progress.json"

# ---------------------------
# Vokabelliste (Beispiel, 10+ Wörter – hier vollständig)
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
    {"ru": "человек", "de": "person"},
    {"ru": "о", "de": "about"},
    {"ru": "один", "de": "one"},
    {"ru": "ещё", "de": "still, yet"},
    {"ru": "бы", "de": "would"},
    {"ru": "такой", "de": "such"},
    {"ru": "только", "de": "only"},
    {"ru": "себя", "de": "oneself"},
    {"ru": "своё", "de": "one’s own"},
    {"ru": "какой", "de": "what kind, which"},
    {"ru": "когда", "de": "when"},
    {"ru": "уже", "de": "already"},
    {"ru": "для", "de": "for"},
    {"ru": "вот", "de": "here is, there is"},
    {"ru": "кто", "de": "who"},
    {"ru": "да", "de": "yes"},
    {"ru": "говорить", "de": "to speak, say"},
    {"ru": "год", "de": "year"},
    {"ru": "знать", "de": "to know"},
    {"ru": "мой", "de": "my"},
    {"ru": "до", "de": "until, before"},
    {"ru": "или", "de": "or"},
    {"ru": "если", "de": "if"},
    {"ru": "время", "de": "time"},
    {"ru": "рука", "de": "hand"},
    {"ru": "нет", "de": "no, not"},
    {"ru": "самый", "de": "most, the very"},
    {"ru": "ни", "de": "neither, nor"},
    {"ru": "стать", "de": "to become"},
    {"ru": "большой", "de": "big"},
    {"ru": "даже", "de": "even"},
    {"ru": "другой", "de": "other"},
    {"ru": "наш", "de": "our"},
    {"ru": "под", "de": "under"},
    {"ru": "где", "de": "where"},
    {"ru": "дело", "de": "matter, affair"},
    {"ru": "есть", "de": "to be, to have (there is)"},
    {"ru": "хорошо", "de": "well, good"},
    {"ru": "надо", "de": "need to"},
    {"ru": "тогда", "de": "then"},
    {"ru": "сейчас", "de": "now"},
    {"ru": "сам", "de": "self"},
    {"ru": "чтобы", "de": "in order to, so that"},
    {"ru": "раз", "de": "time, once"},
    {"ru": "два", "de": "two"},
    {"ru": "там", "de": "there"},
    {"ru": "чем", "de": "than"},
    {"ru": "глаз", "de": "eye"},
    {"ru": "жизнь", "de": "life"},
    {"ru": "первый", "de": "first"},
    {"ru": "день", "de": "day"},
    {"ru": "тут", "de": "here"},
    {"ru": "во", "de": "in (variant of 'в')"},
    {"ru": "ничего", "de": "nothing"},
    {"ru": "потом", "de": "then, later"},
    {"ru": "очень", "de": "very"},
    {"ru": "со", "de": "with (variant of 'с')"},
    {"ru": "хотеть", "de": "to want"},
    {"ru": "лицо", "de": "face"},
    {"ru": "после", "de": "after"},
    {"ru": "новый", "de": "new"},
    {"ru": "без", "de": "without"},
    {"ru": "говорить", "de": "to speak"},
    {"ru": "ходить", "de": "to go (by foot, regularly)"},
    {"ru": "думать", "de": "to think"},
    {"ru": "спросить", "de": "to ask"},
    {"ru": "видеть", "de": "to see"},
    {"ru": "стоять", "de": "to stand"}
]

# ---------------------------
# Hilfsfunktionen
# ---------------------------

def play_audio(text, lang="ru"):
    """Gibt das gesprochene Wort wieder."""
    tts = gTTS(text, lang=lang)
    tts.save("audio.mp3")
    with open("audio.mp3", "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/mp3")


def get_random_choices(correct, all_words, key):
    """Erstellt Multiple‑Choice‑Antworten."""
    choices = [correct]
    while len(choices) < 4:
        word = random.choice(all_words)[key]
        if word not in choices:
            choices.append(word)
    random.shuffle(choices)
    return choices


def load_progress():
    """Lädt gespeicherten Fortschritt aus Datei."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.update(data)
        except (json.JSONDecodeError, IOError):
            pass  # Bei Fehlern neu starten


def save_progress():
    """Speichert aktuellen Fortschritt in Datei."""
    keys = [
        "index",
        "correct",
        "total",
        "streak",
        "best_streak",
        "history",
    ]
    data = {k: st.session_state.get(k, 0) for k in keys}
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError:
        st.warning("⚠️ Fortschritt konnte nicht gespeichert werden.")

# ---------------------------
# Session State Initialisieren & Progress Laden
# ---------------------------
if "initialized" not in st.session_state:
    # Standardwerte setzen
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.history = []

    # Bereits vorhandenen Fortschritt laden
    load_progress()
    st.session_state.initialized = True

# ---------------------------
# UI: Einstellungen
# ---------------------------
st.title("🇷🇺 Russisch-Vokabeltrainer")

st.sidebar.title("Einstellungen")
num_cards = st.sidebar.slider("Wie viele Vokabeln lernen?", 5, len(vocab), 10)
mode = st.sidebar.radio("Lernmodus", ["Eingabe", "Multiple Choice"])
from_lang = st.sidebar.radio("Was wird gezeigt?", ["🇷🇺 Russisch", "English"])

if st.sidebar.button("🔄 Statistik zurücksetzen"):
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.history = []
    save_progress()
    st.rerun()

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
        st.session_state.total += 1
        is_correct = user_input.strip().lower() == target_word.lower()
        if is_correct:
            st.success("✅ Richtig!")
            st.session_state.correct += 1
            st.session_state.streak += 1
            st.session_state.best_streak = max(
                st.session_state.streak, st.session_state.best_streak
            )
        else:
            st.error(f"❌ Falsch. Richtig wäre: {target_word}")
            st.session_state.streak = 0

        st.session_state.history.append(
            {"Frage": source_word, "Antwort": user_input, "Korrekt": is_correct}
        )
        st.session_state.index += 1
        save_progress()
        st.rerun()

elif mode == "Multiple Choice":
    correct_answer = current_word[target]

    if (
        "choices" not in st.session_state
        or st.session_state.get("last_index") != st.session_state.index
    ):
        choices = get_random_choices(correct_answer, vocab_subset, target)
        st.session_state.choices = choices
        st.session_state.selected_choice = None
        st.session_state.last_index = st.session_state.index

    try:
        default_index = st.session_state.choices.index(st.session_state.selected_choice)
    except (ValueError, TypeError):
        default_index = 0

    selected = st.radio(
        "Wähle die richtige Übersetzung:",
        st.session_state.choices,
        index=default_index,
        key="radio_choice",
    )
    st.session_state.selected_choice = selected

    if st.button("Antwort prüfen"):
        st.session_state.total += 1
        is_correct = st.session_state.selected_choice == correct_answer

        if is_correct:
            st.success("✅ Richtig!")
            st.session_state.correct += 1
            st.session_state.streak += 1
            st.session_state.best_streak = max(
                st.session_state.streak, st.session_state.best_streak
            )
        else:
            st.error(f"❌ Falsch. Richtig wäre: {correct_answer}")
            st.session_state.streak = 0

        st.session_state.history.append(
            {
                "Frage": source_word,
                "Antwort": st.session_state.selected_choice,
                "Korrekt": is_correct,
            }
        )
        st.session_state.index += 1
        st.session_state.pop("choices", None)
        st.session_state.pop("selected_choice", None)
        save_progress()
        st.rerun()

# ---------------------------
# Fortschritt & Statistik
# ---------------------------
st.sidebar.markdown(
    f"**Fortschritt**: {st.session_state.correct}/{st.session_state.total} korrekt"
)
st.sidebar.markdown(f"🔥 Streak: {st.session_state.streak}")
st.sidebar.markdown(f"🏆 Rekord: {st.session_state.best_streak}")

if st.sidebar.checkbox("📈 Fortschrittsgraph anzeigen") and st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    df["Gesamt"] = df.index + 1
    df["Richtig"] = df["Korrekt"].cumsum()

    fig, ax = plt.subplots()
    ax.plot(df["Gesamt"], df["Richtig"], marker="o")
    ax.set_xlabel("Gesamtversuche")
    ax.set_ylabel("Richtige Antworten")
    ax.set_title("Lernfortschritt")
    st.sidebar.pyplot(fig)

# ---------------------------
# Vokabel-Tabelle in Sidebar
# ---------------------------
if st.sidebar.checkbox("📚 Vokabeltabelle anzeigen"):
    st.sidebar.dataframe(pd.DataFrame(vocab_subset))
