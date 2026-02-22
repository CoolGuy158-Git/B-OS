import os
import tkinter as tk
from custommsgbox import show
from System67.make_draggable import make_draggable

BOS_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ALLOWED_ROOT = os.path.join(BOS_ROOT, "User")

app = tk.Toplevel()
app.geometry("600x400")
app.title("FileLand")
app.overrideredirect(True)
app.attributes("-alpha", 0.95)
title_bar = tk.Frame(app, bg="gray", height=20)
title_bar.pack(side="top", fill="x")
close_btn = tk.Button(title_bar, text="✕", bg="#ff4d4d", fg="white", bd=0, command=app.destroy)
close_btn.pack(side="right", padx=5)
make_draggable(app, handle=title_bar)

current_path = ALLOWED_ROOT
path_frame = tk.Frame(app)
path_frame.pack(fill="x")
path_label = tk.Label(path_frame, text=current_path)
path_label.pack(side="left", padx=5)
def go_up():
    global current_path
    parent = os.path.dirname(current_path)
    if os.path.commonpath([ALLOWED_ROOT, parent]) == ALLOWED_ROOT:
        current_path = parent
        load_files()
    else:
        show("Info", "Access denied! You can’t leave your User folder.")
tk.Button(path_frame, text="Up", command=go_up).pack(side="right", padx=5)

file_listbox = tk.Listbox(app)
file_listbox.pack(fill="both", expand=True)

def load_files():
    file_listbox.delete(0, tk.END)
    try:
        for item in os.listdir(current_path):
            file_listbox.insert(tk.END, item)
    except PermissionError:
        show("Info","Permission denied!")
    path_label.config(text=current_path)

def open_item(event):
    global current_path
    selection = file_listbox.get(file_listbox.curselection())
    full_path = os.path.join(current_path, selection)

    if os.path.commonpath([ALLOWED_ROOT, full_path]) != ALLOWED_ROOT:
        show("Info","Access denied! You can’t leave your User folder.")
        return

    if os.path.isdir(full_path):
        current_path = full_path
        load_files()
    else:
        try:
            os.startfile(full_path)
        except Exception as e:
            show("Error", f"Can't open file: {e}", bg_color='red')
file_listbox.bind("<Double-1>", open_item)
load_files()
app.update_idletasks()
width = app.winfo_width()
height = app.winfo_height()
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2)
app.geometry(f"{width}x{height}+{x}+{y}")
app.mainloop()
