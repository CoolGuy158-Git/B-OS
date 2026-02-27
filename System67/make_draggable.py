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

def make_draggable_btn(btn):
    def start_drag(event):
        btn.startX = event.x
        btn.startY = event.y

    def on_drag(event):
        new_x = btn.winfo_x() + (event.x - btn.startX)
        new_y = btn.winfo_y() + (event.y - btn.startY)

        btn.place(x=new_x, y=new_y)

    btn.bind("<Button-1>", start_drag)
    btn.bind("<B1-Motion>", on_drag)



