import tkinter as tk
from PIL import ImageTk, Image
import os
import runpy
from PIL.ImageFile import ImageFile
import time

root = tk.Tk()
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.destroy())
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

bg_img = Image.open(r"System67\bgimages\Homescreen.PNG")
bg_img = bg_img.resize((screen_width, screen_height), Image.LANCZOS)
bg_final = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_final)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

apps_folder = os.path.abspath("Apps")
x_offset, y_offset = 20, 20
for app_name in os.listdir(apps_folder):
    app_path = os.path.join(apps_folder, app_name)
    if os.path.isdir(app_path):
        icon_path = os.path.join(app_path, "icon.png")
        code_path = os.path.join(app_path, "code.py")
        icon = Image.open(icon_path)
        icon: ImageFile = icon.resize((64, 64))
        icon_tk = ImageTk.PhotoImage(icon)
        btn = tk.Button(root, image=icon_tk, command=lambda p=code_path: runpy.run_path(p))
        btn.image = icon_tk
        btn.place(x=x_offset, y=y_offset)
        y_offset += 90

taskbar_height = 40
taskbar = tk.Frame(root, bg="#C0C0C0", height=taskbar_height)
taskbar.pack(side="bottom", fill="x")

clock_label = tk.Label(taskbar, text="", bg="#C0C0C0", fg="black", font=("Courier New", 14))
clock_label.pack(side="right", padx=5, pady=5)

def update_clock(label):
    label.config(text=time.strftime("%H:%M:%S"))
    label.after(1000, update_clock, label)

update_clock(clock_label)

def start_menu():
    if hasattr(start_menu, "menu") and start_menu.menu.winfo_exists():
        start_menu.menu.destroy()

    menu_width, menu_height = 150, 50
    menu = tk.Frame(root, bg="lightgray", width=menu_width, height=menu_height, borderwidth=2, relief="ridge")
    start_menu.menu = menu

    start_x = startbutton.winfo_x()
    start_y = root.winfo_height() - taskbar_height - menu_height
    menu.place(x=start_x, y=start_y)

    shut_down = tk.Button(menu, text="Shutdown", command=root.destroy)
    shut_down.pack(fill="both", expand=True)

    def close_menu(event):
        if start_menu.menu.winfo_exists():
            x1 = start_menu.menu.winfo_rootx()
            y1 = start_menu.menu.winfo_rooty()
            x2 = x1 + start_menu.menu.winfo_width()
            y2 = y1 + start_menu.menu.winfo_height()
            if not (x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2):
                start_menu.menu.destroy()
                root.unbind("<Button-1>", close_menu_id)

    close_menu_id = root.bind("<Button-1>", close_menu)

icon_path = os.path.abspath(r"System67\logo.ico")

icon = Image.open(icon_path)
icon = icon.resize((35, 35))
start_icon = ImageTk.PhotoImage(icon)

startbutton = tk.Button(
    taskbar,
    image=start_icon,
    bg="#C0C0C0",
    bd=1,
    command=start_menu
)
startbutton.image = start_icon
startbutton.pack(side="left", padx=5, pady=5)

root.mainloop()
