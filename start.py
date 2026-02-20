import sys
import tkinter as tk
from PIL import Image, ImageTk
from custommsgbox import show
import subprocess
import pygame
import hashlib
import os
root = tk.Tk()
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.destroy())
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(r"System67\soundeffects\startup.mp3")
pygame.mixer.music.play()
bg_img = Image.open(r"System67\bgimages\Lockscreen.PNG")
bg_img = bg_img.resize((screen_width, screen_height), Image.LANCZOS)
bg_final = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_final)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
user_img = Image.open(r"System67\user.png").resize((100, 100))
user_final = ImageTk.PhotoImage(user_img)
label = tk.Label(root, image=user_final)
label.place(relx=0.5, rely=0.5, anchor="center", y=-150)
tk.Label(root, text="User", fg="white", bg="black").place(relx=0.5, rely=0.5, anchor="center", y=-60)
passwd_entry = tk.Entry(root, show="*")
passwd_entry.place(relx=0.5, rely=0.5, anchor="center", y=-40)
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

first_attempt = None
confirming = False
def show_password():
    passwd_entry.config(show="")
    root.after(500, lambda: passwd_entry.config(show="*"))

show_btn = tk.Button(root, text="👁", command=show_password, bg="gray", fg="white")
show_btn.place(relx=0.559, rely=0.5, anchor="center", y=-40)

def enter_pass():
    global first_attempt, confirming
    passwd = passwd_entry.get()
    if len(str(passwd)) <= 6:
        show("Oops", "Password must be longer than 6 chars", bg_color='yellow')
        return
    if not passwd:
        show("Oops", "Enter a password first!", bg_color='yellow')
        return
    if not os.path.exists("password.txt"):
        if not confirming:
            first_attempt = passwd
            confirming = True
            passwd_entry.delete(0, tk.END)
            show("Info", "Enter password again to confirm", bg_color='yellow')
        else:
            if passwd == first_attempt:
                hashed = hash_pass(passwd)
                with open("password.txt", "w") as f:
                    f.write(hashed)
                show("Success", "Password saved! Logging in...", bg_color='green')
                subprocess.Popen([sys.executable, "homescreen.py"])
                root.after(3000, root.destroy)
            else:
                show("Remake Passwd", "Passwords do not match! Start over.", bg_color='red')
            first_attempt = None
            confirming = False
            passwd_entry.delete(0, tk.END)
        return
    with open("password.txt", "r") as f:
        saved_hash = f.read()
    if hash_pass(passwd) == saved_hash:
        pygame.mixer.music.load(r"System67\soundeffects\correct.mp3")
        subprocess.Popen([sys.executable, "homescreen.py"])
        pygame.mixer.music.play()
        root.after(3000, root.destroy)
    else:
        show("Wrong", "Password incorrect!", bg_color='red')
    passwd_entry.delete(0, tk.END)
tk.Button(root, text="Enter", command=enter_pass).place(relx=0.5, rely=0.5, anchor="center", y=0)
def enter_pass_event(event):
    enter_pass()
passwd_entry.bind("<Return>", enter_pass_event)
root.mainloop()
