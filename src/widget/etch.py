from typing import NamedTuple, SupportsFloat
import tkinter as tk


class Stylus(NamedTuple):
    x: float = 0
    y: float = 0


class Etch(tk.Canvas):
    move_steps: SupportsFloat = 1  # Movement increment in pixels
    line_size: int = 2
    line_color: str = "black"
    dot_size: int = 2
    dot_color: str = "black"

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # Initial position
        self.width, self.height = float(self.cget("width")), float(self.cget("height"))
        self.stylus = Stylus(self.width / 2, self.height / 2)

        # Create initial dot
        self.dot_id = self.__create_dot()

    def __create_dot(self) -> int | str:
        return self.create_oval(
            self.stylus.x - self.dot_size,
            self.stylus.y - self.dot_size,
            self.stylus.x + self.dot_size,
            self.stylus.y + self.dot_size,
            fill="black",
            outline="",
        )

    def move(self, dx: int, dy: int, steps: SupportsFloat | None = None) -> None:
        if steps is None:
            steps = self.move_steps

        # Draw line from previous position to new position
        new_stylus = Stylus(self.stylus.x + dx * steps, self.stylus.y + dy * steps)

        if 0 < new_stylus.x < self.width and 0 < new_stylus.y < self.height:
            self.create_line(
                self.stylus.x, self.stylus.y, new_stylus.x, new_stylus.y, fill=self.line_color, width=self.line_size
            )
            # Update position and move dot
            self.stylus = new_stylus
            self.coords(
                self.dot_id,
                self.stylus.x - self.dot_size,
                self.stylus.y - self.dot_size,
                self.stylus.x + self.dot_size,
                self.stylus.y + self.dot_size,
            )

    def move_left(self, *args, steps: SupportsFloat | None = None) -> None:
        self.move(-1, 0, steps)

    def move_right(self, *args, steps: SupportsFloat | None = None) -> None:
        self.move(1, 0, steps)

    def move_up(self, *args, steps: SupportsFloat | None = None) -> None:
        self.move(0, -1, steps)

    def move_down(self, *args, steps: SupportsFloat | None = None) -> None:
        self.move(0, 1, steps)

    def reset(self, *args) -> None:
        self.delete("all")
        self.dot_id = self.__create_dot()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Arrow Key Drawing")
    canvas = Etch(root, bg="white", width=400, height=400)
    # Bind arrow keys
    canvas.bind("<Left>", canvas.move_left)
    canvas.bind("<Right>", canvas.move_right)
    canvas.bind("<Up>", canvas.move_up)
    canvas.bind("<Down>", canvas.move_down)
    canvas.focus_set()

    canvas.pack(pady=20, padx=20)

    root.mainloop()
