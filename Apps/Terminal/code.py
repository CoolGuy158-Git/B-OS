import tkinter as ctk
import re
from System67.make_draggable import make_draggable
import platform
import psutil
import os
import time
import system

def format_uptime():
    uptime_seconds = int(time.time() - system.boot_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def run_commands(cmd):
    user_text = cmd.strip().lower()

    if user_text == "help":
        with open(r"Apps\Terminal\help.txt", "r") as f:
            return f.read()

    if user_text == "bver":
        logo = "\n".join([
            "                                      ",
            "  ▀███▀▀▀██▄        ▄▄█▀▀██▄  ▄█▀▀▀█▄█",
            "    ██    ██      ▄██▀    ▀██▄██    ▀█",
            "    ██    ██      ██▀      ▀█████▄",
            "    ██▀▀▀█▄▄ ████ ██        ██ ▀█████▄",
            "    ██    ▀█      ██▄      ▄██     ▀██",
            "    ██    ▄█      ▀██▄    ▄██▀█     ██",
            "  ▄████████         ▀▀████▀▀ █▀█████▀",
        ])
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info().rss / (1024 * 1024)

        ram = psutil.virtual_memory()
        used_ram = ram.used / (1024 * 1024)
        total_ram = ram.total / (1024 * 1024)

        uptime_str = format_uptime()

        info = f"""
OS: B-OS v1.0.0
Kernel: Python {platform.python_version()}
Uptime: {uptime_str}
Shell: Python
Resolution: {app.winfo_screenwidth()}x{app.winfo_screenheight()}
DE: BootOS-Desktop V2 (Tkinter)
Memory (Process): {process_memory:.2f} MB
System RAM: {used_ram:.0f} MB / {total_ram:.0f} MB
"""
        return logo + "\n\n" + info

    return "Unknown command"

def remove_ansi(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def on_enter(event=None):
    cmd = command_input.get()
    if cmd.strip() == "":
        return

    output_text.configure(state="normal")
    output_text.insert("end", f"> {cmd}\n")

    if cmd.strip().lower() == "bver":
        def refresh_bver():
            result = run_commands("bver")
            clean_result = remove_ansi(result or "")
            output_text.insert("end", clean_result + "\n")
            output_text.see("end")
            app.after(1000, refresh_bver)

        refresh_bver()
    else:
        result = run_commands(cmd)
        clean_result = remove_ansi(result or "")
        output_text.insert("end", clean_result + "\n")
        output_text.see("end")

    output_text.configure(state="disabled")
    command_input.delete(0, "end")

    if 'instruction' in globals():
        instruction.destroy()

app = ctk.Toplevel()
app.geometry("900x600")
app.title("Terminal")
app.attributes("-alpha", 0.9)
app.overrideredirect(True)

title_bar = ctk.Frame(app, bg="#333333", height=25)
title_bar.pack(side="top", fill="x")

ctk.Label(title_bar, text="Terminal", bg="#333333", fg="gray", font=("Arial", 10)).pack(side="left", padx=5)
close_btn = ctk.Button(title_bar, text="✕", bg="#ff4d4d", fg="white", bd=0, command=app.destroy)
close_btn.pack(side="right", padx=5)
make_draggable(app, handle=title_bar)

output_text = ctk.Text(app)
output_text.pack(fill="both", expand=True)

instruction = ctk.Label(app, text="Type a command and press Enter")
instruction.pack(fill="x")

command_input = ctk.Entry(app)
command_input.pack(fill="x")
command_input.bind("<Return>", on_enter)

app.update_idletasks()
width = app.winfo_width()
height = app.winfo_height()
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2)
app.geometry(f"{width}x{height}+{x}+{y}")

app.mainloop()
