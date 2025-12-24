import tkinter as tk
from tkinter import font
import random
import sys
import os

try:
    import pygame
    AUDIO_ENABLED = True
except ImportError:
    AUDIO_ENABLED = False
    print("Pygame not found. Audio disabled.")

try:
    import winsound
except ImportError:
    winsound = None

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CoffeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compatibility Check vFinal")
        
        self.root.attributes('-fullscreen', True)
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.bg_color = '#0f0f1a'
        self.root.configure(bg=self.bg_color)

        self.yes_sound = None
        if AUDIO_ENABLED:
            self.init_audio()

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.particles = []
        self.sequence_step = 0
        self.is_intro = True 
        
        self.no_messages = ["Σίγουρα;", "Γλιστράει!", "Πιάσε με!", "Λάθος!", "Σχεδόν...", "Δοκίμασε το πράσινο!", "Ουπσ!"]

        self.setup_ui()
        self.animate_bg()
        self.run_sequence()

    def init_audio(self):
        try:
            pygame.mixer.init()
            music_path = resource_path("song.wav") 
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            
            sfx_path = resource_path("yay.wav") 
            if os.path.exists(sfx_path):
                self.yes_sound = pygame.mixer.Sound(sfx_path)
                self.yes_sound.set_volume(0.6)
        except Exception:
            pass

    def setup_ui(self):
        self.code_font = font.Font(family="Consolas", size=18)
        self.question_font = font.Font(family="Helvetica", size=32, weight="bold")
        self.btn_font = font.Font(family="Verdana", size=18, weight="bold")
        
        self.label = self.canvas.create_text(
            self.width/2, self.height/2 - 50, 
            text="", 
            fill="#00ffcc", 
            font=self.code_font, 
            width=self.width - 100, 
            justify="center"
        )
        
        self.btn_yes = tk.Button(
            self.root, 
            text="ΝΑΙ, ΠΑΜΕ! ☕", 
            font=self.btn_font, 
            bg="#00e676", 
            fg="white", 
            activebackground="#00c853", 
            relief="flat",
            cursor="hand2",
            command=self.on_yes,
            padx=40, pady=20
        )
        
        self.btn_no = tk.Button(
            self.root, 
            text="Μπαα...", 
            font=self.btn_font, 
            bg="#ff3366", 
            fg="white", 
            activebackground="#d50000",
            relief="flat",
            cursor="hand2",
            padx=30, pady=20
        )
        
        self.btn_no.bind("<Enter>", self.teleport_no)

    def type_text(self, text, index=0):
        if index == 0:
            self.canvas.itemconfig(self.label, text="")
        
        current_text = self.canvas.itemcget(self.label, "text")
        if index < len(text):
            self.canvas.itemconfig(self.label, text=current_text + text[index])
            self.root.after(30, lambda: self.type_text(text, index + 1))
        else:
            delay = 2500
            self.root.after(delay, self.next_sequence_step)

    def run_sequence(self):
        self.messages = [
            "Initializing Neural Network...",
            "Φόρτωση modules επικοινωνίας...",
            "Ανίχνευση κοινής αίσθησης του χιούμορ...",
            "Υπολογισμός ιδανικού σεναρίου...",
            "SUCCESS: MATCH FOUND.",
            "Πρόταση συστήματος: Καφές & Κουβέντα."
        ]
        if self.sequence_step < len(self.messages):
            self.type_text(self.messages[self.sequence_step])
        else:
            self.reveal()

    def next_sequence_step(self):
        self.sequence_step += 1
        current_list = self.messages if self.is_intro else self.final_messages

        if self.sequence_step < len(current_list):
            self.type_text(current_list[self.sequence_step])
        else:
            if self.is_intro:
                self.reveal()
            else:
                self.root.after(100, self.shutdown_app)

    def shutdown_app(self):
        if winsound:
            winsound.MessageBeep(winsound.MB_OK)
        self.root.destroy()

    def reveal(self):
        final_text = "Αν σου κάνει κέφι, πάμε για έναν καφέ κάποια μέρα.\nΑν όχι, όλα καλά 🙂;"
        self.canvas.itemconfig(self.label, text=final_text, fill="white", font=self.question_font)
        self.canvas.create_window(self.width/2 - 150, self.height/2 + 150, window=self.btn_yes)
        self.canvas.create_window(self.width/2 + 150, self.height/2 + 150, window=self.btn_no)
        self.pulse_yes_button()

    def pulse_yes_button(self, state=True):
        try:
            if self.btn_yes.winfo_exists():
                new_bg = "#00e676" if state else "#00c853"
                self.btn_yes.config(bg=new_bg)
                self.root.after(600, lambda: self.pulse_yes_button(not state))
        except:
            pass

    def teleport_no(self, event):
        pad = 100 
        new_x = random.randint(pad, self.width - pad)
        new_y = random.randint(pad, self.height - pad)
        self.btn_no.place(x=new_x, y=new_y)
        self.btn_no.lift()
        new_msg = random.choice(self.no_messages)
        self.btn_no.config(text=new_msg)

    def on_yes(self):
        if AUDIO_ENABLED and self.yes_sound:
            self.yes_sound.play()
            
        self.btn_no.destroy()
        self.btn_yes.destroy()
        self.spawn_confetti(300) 

        self.final_messages = [
            "Έκανες την σωστή επιλογή!",  
            "Τώρα πηγαινέ πες το μου.", 
            "Γιατί δεν ξέρω αν πατησές ναι ακόμα...",
            "Α ναι και μην το ξεχάσω...",
            "Ο καφές κερασμένος☕.",
            "Θα σε περιμένω.",
            "...",
            "...",
            "...",
            "Ακομα εδώ Είσαι?",
            "..."
        ]

        self.is_intro = False
        self.sequence_step = 0
        self.canvas.itemconfig(self.label, text="", font=self.code_font, fill="#00ffcc") 
        self.type_text(self.final_messages[0])

    def spawn_confetti(self, amount):
        for _ in range(amount):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(5, 15)
            color = random.choice(['#ffd700', '#00e676', '#ff4081', '#ffffff'])
            speed = random.uniform(2, 6)
            p = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.particles.append([p, speed])

    def animate_bg(self):
        if len(self.particles) < 200:
            x = random.randint(0, self.width)
            y = self.height + 10
            size = random.randint(2, 6)
            speed = random.uniform(0.5, 2)
            color = random.choice(["#0606ad", "#0BA90B", "#cc0c0c", "#d90fa7","#0c99cc","#a15c07","#5c0ccc"]) 
            p = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.particles.append([p, speed])

        for p in self.particles:
            self.canvas.move(p[0], 0, -p[1])
            pos = self.canvas.coords(p[0])
            if not pos or pos[1] < -20: 
                self.canvas.delete(p[0])
                self.particles.remove(p)

        self.root.after(20, self.animate_bg)

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeApp(root)
    root.mainloop()