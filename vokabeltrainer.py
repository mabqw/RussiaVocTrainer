# Updated version for mobile use and improved audio playback using playsound
import random
import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
from playsound import playsound
import os
import tempfile

# --- Data: 100 common Russian words with English translations ---
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

# --- App Class ---
class VocabTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Russisch Vokabeltrainer")
        self.limit = 10
        self.streak = 0
        self.record_streak = 0
        self.current_index = 0
        self.mode = tk.StringVar(value="input")
        self.cards = random.sample(vocab, self.limit)
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Wie viele Karten möchtest du lernen? (max 100)").pack()
        self.entry_limit = tk.Entry(self.root)
        self.entry_limit.insert(0, "10")
        self.entry_limit.pack()
        tk.Button(self.root, text="Start", command=self.start).pack(pady=10)

    def start(self):
        try:
            self.limit = min(100, int(self.entry_limit.get()))
            self.cards = random.sample(vocab, self.limit)
            self.current_index = 0
            self.streak = 0
            self.init_learning_ui()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben.")

    def init_learning_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.word_label = tk.Label(self.root, text="", font=("Arial", 20))
        self.word_label.pack(pady=10)

        self.entry_answer = tk.Entry(self.root, font=("Arial", 14))
        self.entry_answer.pack()

        self.choice_buttons = [tk.Button(self.root, text="", command=lambda i=i: self.check_choice(i)) for i in range(4)]
        for btn in self.choice_buttons:
            btn.pack(pady=2)

        self.check_btn = tk.Button(self.root, text="Antwort prüfen", command=self.check_input)
        self.check_btn.pack(pady=5)

        self.sound_btn = tk.Button(self.root, text="🔊 Aussprache", command=self.play_audio)
        self.sound_btn.pack(pady=5)

        self.mode_switch = tk.Button(self.root, text="Modus wechseln", command=self.switch_mode)
        self.mode_switch.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Streak: 0 | Rekord: 0")
        self.status_label.pack(pady=10)

        self.show_card()

    def switch_mode(self):
        self.mode.set("choice" if self.mode.get() == "input" else "input")
        self.show_card()

    def show_card(self):
        ru, de = self.cards[self.current_index]
        self.word_label.config(text=ru)
        self.entry_answer.delete(0, tk.END)
        self.status_label.config(text=f"Streak: {self.streak} | Rekord: {self.record_streak}")

        if self.mode.get() == "choice":
            correct = de
            options = [correct] + [d for _, d in random.sample(vocab, 3) if d != correct]
            options = random.sample(options, k=4)
            for i, btn in enumerate(self.choice_buttons):
                btn.config(text=options[i], state=tk.NORMAL)
            self.entry_answer.pack_forget()
            self.check_btn.pack_forget()
            for btn in self.choice_buttons:
                btn.pack()
        else:
            for btn in self.choice_buttons:
                btn.pack_forget()
            self.entry_answer.pack()
            self.check_btn.pack()

    def check_input(self):
        ru, de = self.cards[self.current_index]
        user_input = self.entry_answer.get().strip().lower()
        if user_input in [d.strip().lower() for d in de.split(",")]:
            self.streak += 1
            self.record_streak = max(self.record_streak, self.streak)
        else:
            messagebox.showinfo("Falsch", f"Richtige Antwort: {de}")
            self.streak = 0
        self.next_card()

    def check_choice(self, i):
        ru, de = self.cards[self.current_index]
        if self.choice_buttons[i]['text'] == de:
            self.streak += 1
            self.record_streak = max(self.record_streak, self.streak)
        else:
            messagebox.showinfo("Falsch", f"Richtige Antwort: {de}")
            self.streak = 0
        self.next_card()

    def next_card(self):
        self.current_index += 1
        if self.current_index >= len(self.cards):
            messagebox.showinfo("Fertig", f"Du hast alle {self.limit} Karten geübt!")
            self.root.destroy()
        else:
            self.show_card()

    def play_audio(self):
        ru, _ = self.cards[self.current_index]
        tts = gTTS(text=ru, lang='ru')
        filename = "temp_audio.mp3"
        tts.save(filename)
        os.system(f"start {filename}" if os.name == "nt" else f"afplay {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabTrainerApp(root)
    root.mainloop()