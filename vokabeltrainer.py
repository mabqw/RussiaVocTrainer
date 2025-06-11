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
# Vokabelliste (vollständig, mit "en" statt "de")
# ---------------------------
vocab = [
    {"ru": "и", "en": "and"},
    {"ru": "в", "en": "in"},
    {"ru": "не", "en": "not"},
    {"ru": "он", "en": "he"},
    {"ru": "на", "en": "on, at"},
    {"ru": "я", "en": "I"},
    {"ru": "что", "en": "what, that"},
    {"ru": "тот", "en": "that"},
    {"ru": "быть", "en": "to be"},
    {"ru": "с", "en": "with"},
    {"ru": "а", "en": "but"},
    {"ru": "весь", "en": "all"},
    {"ru": "это", "en": "this, it"},
    {"ru": "как", "en": "how, like"},
    {"ru": "она", "en": "she"},
    {"ru": "по", "en": "along, by, according to"},
    {"ru": "но", "en": "but"},
    {"ru": "они", "en": "they"},
    {"ru": "к", "en": "to"},
    {"ru": "у", "en": "at, by"},
    {"ru": "ты", "en": "you (informal)"},
    {"ru": "из", "en": "from, out of"},
    {"ru": "мы", "en": "we"},
    {"ru": "за", "en": "behind, for"},
    {"ru": "вы", "en": "you (formal or plural)"},
    {"ru": "так", "en": "so, thus"},
    {"ru": "же", "en": "same, also"},
    {"ru": "от", "en": "from, of"},
    {"ru": "сказать", "en": "to say"},
    {"ru": "этот", "en": "this"},
    {"ru": "который", "en": "which, who"},
    {"ru": "мочь", "en": "can, to be able"},
    {"ru": "человек", "en": "person"},
    {"ru": "о", "en": "about"},
    {"ru": "один", "en": "one"},
    {"ru": "ещё", "en": "still, yet"},
    {"ru": "бы", "en": "would"},
    {"ru": "такой", "en": "such"},
    {"ru": "только", "en": "only"},
    {"ru": "себя", "en": "oneself"},
    {"ru": "своё", "en": "one’s own"},
    {"ru": "какой", "en": "what kind, which"},
    {"ru": "когда", "en": "when"},
    {"ru": "уже", "en": "already"},
    {"ru": "для", "en": "for"},
    {"ru": "вот", "en": "here is, there is"},
    {"ru": "кто", "en": "who"},
    {"ru": "да", "en": "yes"},
    {"ru": "говорить", "en": "to speak, say"},
    {"ru": "год", "en": "year"},
    {"ru": "знать", "en": "to know"},
    {"ru": "мой", "en": "my"},
    {"ru": "до", "en": "until, before"},
    {"ru": "или", "en": "or"},
    {"ru": "если", "en": "if"},
    {"ru": "время", "en": "time"},
    {"ru": "рука", "en": "hand"},
    {"ru": "нет", "en": "no, not"},
    {"ru": "самый", "en": "most, the very"},
    {"ru": "ни", "en": "neither, nor"},
    {"ru": "стать", "en": "to become"},
    {"ru": "большой", "en": "big"},
    {"ru": "даже", "en": "even"},
    {"ru": "другой", "en": "other"},
    {"ru": "наш", "en": "our"},
    {"ru": "под", "en": "under"},
    {"ru": "где", "en": "where"},
    {"ru": "дело", "en": "matter, affair"},
    {"ru": "есть", "en": "to be, to have (there is)"},
    {"ru": "хорошо", "en": "well, good"},
    {"ru": "надо", "en": "need to"},
    {"ru": "тогда", "en": "then"},
    {"ru": "сейчас", "en": "now"},
    {"ru": "сам", "en": "self"},
    {"ru": "чтобы", "en": "in order to, so that"},
    {"ru": "раз", "en": "time, once"},
    {"ru": "два", "en": "two"},
    {"ru": "там", "en": "there"},
    {"ru": "чем", "en": "than"},
    {"ru": "глаз", "en": "eye"},
    {"ru": "жизнь", "en": "life"},
    {"ru": "первый", "en": "first"},
    {"ru": "день", "en": "day"},
    {"ru": "тут", "en": "here"},
    {"ru": "во", "en": "in (variant of 'в')"},
    {"ru": "ничего", "en": "nothing"},
    {"ru": "потом", "en": "then, later"},
    {"ru": "очень", "en": "very"},
    {"ru": "со", "en": "with (variant of 'с')"},
    {"ru": "хотеть", "en": "to want"},
    {"ru": "лицо", "en": "face"},
    {"ru": "после", "en": "after"},
    {"ru": "новый", "en": "new"},
    {"ru": "без", "en": "without"},
    {"ru": "говорить", "en": "to speak"},
    {"ru": "ходить", "en": "to go (by foot, regularly)"},
    {"ru": "думать", "en": "to think"},
    {"ru": "спросить", "en": "to ask"},
    {"ru": "видеть", "en": "to see"},
    {"ru": "стоять", "en": "to stand"}
]
# ---------------------------
# Hilfsfunktionen
# ---------------------------

def play_audio(text, lang="ru"):
    tts = gTTS(text, lang=lang)
    tts.save("audio.mp3")
    with open("audio.mp3", "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/mp3")

def get_random_choices(correct, all_words, key):
    choices = [correct]
    while len(choices) < 4:
        word = random.choice(all_words)[key]
        if word not in choices:
            choices.append(word)
    random.shuffle(choices)
    return choices

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.update(data)
        except (json.JSONDecodeError, IOError):
            pass

def save_progress():
    keys = ["index", "correct", "total", "streak", "best_streak", "history"]
    data = {k: st.session_state.get(k, 0) for k in keys}
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError:
        st.warning("⚠️ Fortschritt konnte nicht gespeichert werden.")

# ---------------------------
# Session State
# ---------------------------
if "initialized" not in st.session_state:
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.history = []
    load_progress()
    st.session_state.initialized = True

# ---------------------------
# UI: Einstellungen
# ---------------------------
st.title("🇷🇺 Russisch-Vokabeltrainer")

st.sidebar.title("Einstellungen")
num_cards = st.sidebar.slider("Wie viele Vokabeln lernen?", 5, len(vocab), 10)
mode = st.sidebar.radio("Lernmodus", ["Eingabe", "Multiple Choice"])
from_lang = st.sidebar.radio("Was wird gezeigt?", ["🇷🇺 Russisch", "🇬🇧 Englisch"])

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

source = "ru" if from_lang == "🇷🇺 Russisch" else "en"
target = "en" if source == "ru" else "ru"

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
        choices = get_random_choices(current_word, vocab_subset, target)
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
