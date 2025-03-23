import tkinter as tk
from itertools import count

class ShakeableWidget:
    _start_x: int = 0
    _start_y: int = 0
    _prev_x: int = 0
    _prev_y: int = 0
    shake_amount: int = 250

    def __init__(self, widget: tk.Misc) -> None:
        self.widget = widget
        self._drag_count = count()
        self.event_shake = '<<WindowShaken>>'
        self.widget.bind("<ButtonPress-1>", self.__start_drag)
        self.widget.bind("<B1-Motion>", self.__drag_window)

    def __start_drag(self, event: tk.Event):
        """the point where the window is clicked"""
        self._drag_count = count()
        self._start_x = event.x
        self._start_y = event.y

    def __drag_window(self, event: tk.Event):
        dx = event.x - self._start_x
        dy = event.y - self._start_y
        new_x = self.widget.master.winfo_x() + dx
        new_y = self.widget.master.winfo_y() + dy
        self.widget.master.geometry(f"+{new_x}+{new_y}")
        if next(self._drag_count) >= self.shake_amount:
            self.widget.master.event_generate(self.event_shake)
            self._drag_count = count()



if __name__ == "__main__":
    root = tk.Tk()
    sw = ShakeableWidget(root)
    root.bind(sw.event_shake, lambda e: print('shaken') )
    root.mainloop()
