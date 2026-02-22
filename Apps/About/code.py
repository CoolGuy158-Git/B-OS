import tkinter as tk
import platform
import psutil
import time
import os
import system
from System67.make_draggable import make_draggable
from PIL import Image, ImageTk

app = tk.Toplevel()
app.geometry("500x500")
app.attributes("-alpha", 0.9)
app.overrideredirect(True)
title_bar = tk.Frame(app, bg="#333333", height=25)
title_bar.pack(side="top", fill="x")
tk.Label(title_bar, text="About", bg="#333333", fg="gray", font=("Arial", 10)).pack(side="left", padx=5)
close_btn = tk.Button(title_bar, text="✕", bg="#ff4d4d", fg="white", bd=0, command=app.destroy)
close_btn.pack(side="right", padx=5)
make_draggable(app, handle=title_bar)


def format_uptime():
    uptime_seconds = int(time.time() - system.boot_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

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

image = Image.open(r"System67/mainlogo.ico")
photo = ImageTk.PhotoImage(image)

label = tk.Label(app, image=photo)
label.image = photo
label.pack()

infotxt = tk.Label(app, text=info)
infotxt.pack(side="top", fill="x")

app.mainloop()



