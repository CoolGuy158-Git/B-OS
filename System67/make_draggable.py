def make_draggable(win, handle):
    def start_drag(event):
        handle.startX = event.x
        handle.startY = event.y

    def on_drag(event):
        x = win.winfo_x() + event.x - handle.startX
        y = win.winfo_y() + event.y - handle.startY
        win.geometry(f"+{x}+{y}")

    handle.bind("<Button-1>", start_drag)
    handle.bind("<B1-Motion>", on_drag)


