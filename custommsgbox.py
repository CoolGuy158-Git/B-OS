import tkinter as tk
import pygame
def show(title, msg, width=300, height=150, bg_color="gray",
         fg_color="black", play_sound=True):

    if play_sound:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(r"System67\soundeffects\info.mp3")
        pygame.mixer.music.play()

    popup = tk.Toplevel()
    popup.overrideredirect(True)
    popup.configure(bg="gray")
    popup.attributes("-alpha", 0.7)

    border_size = 1
    border_color = "white"

    border = tk.Frame(popup, bg=border_color)
    border.pack(fill="both", expand=True)

    content = tk.Frame(border, bg=bg_color)
    content.pack(padx=border_size, pady=border_size)

    tk.Label(content, text=msg, fg=fg_color, bg=bg_color,
             font=("Arial", 12)).pack(pady=20)

    tk.Button(content, text="OK", command=popup.destroy,
              fg=fg_color, bg="gray").pack(pady=10)

    popup.update_idletasks()

    width = popup.winfo_width()
    height = popup.winfo_height()

    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)

    popup.geometry(f"+{x}+{y}")
    popup.grab_set()
