from typing import SupportsFloat
import cmath
import math
import tkinter as tk

from src.support.circle import Circle


class Knob(tk.Canvas):
    steps = 3
    _angle: int = 0

    def __init__(
        self,
        master: tk.Tk,
        polygon: list[tuple[int, int]],
        *args,
        enable_mousewheel: bool = True,
        **kwargs,
    ) -> None:
        self.polygon = polygon
        self.area = Circle(self.polygon)
        self.width = self.area.radius * 2
        self.height = self.area.radius * 2

        # initiate the Canvas
        super().__init__(master, *args, width=self.width, height=self.height, **kwargs)

        self.event_increase = "<<KnobIncrease>>"
        self.event_decrease = "<<KnobDecrease>>"

        self.polygon_id = self.create_polygon(self.polygon)

        # Event bindings
        self.last_angle = 0
        self.bind("<B1-Motion>", self.__rotate)

        if bool(enable_mousewheel):
            self.bind("<MouseWheel>", self.__mouse_wheel)  # with Windows
            self.bind("<Button-4>", self.__mouse_wheel)  # scroll-up with Linux
            self.bind("<Button-5>", self.__mouse_wheel)  # scroll-down with Linux

    def __mouse_wheel(self, event: tk.Event) -> None:
        """respond to Linux or Windows MouseWheel event"""
        if not self.area.contains((event.x, event.y)):
            return None  # early return

        if event.num == 4 or event.delta == 120:
            self.angle_increase()
        elif event.num == 5 or event.delta == -120:
            self.angle_decrease()

    def _update_angle(self) -> None:
        c_angle = cmath.exp(self.angle * 1j * cmath.pi / 180)
        c_offset = complex(*self.area.center)
        new_coordinates = []
        for x, y in self.polygon:
            c_value = c_angle * (complex(x, y) - c_offset) + c_offset
            new_coordinates.append(c_value.real)
            new_coordinates.append(c_value.imag)
        # update item with new coordinates
        self.coords(self.polygon_id, new_coordinates)

    def __rotate(self, event):
        """Handle mouse drag rotation"""
        if not self.area.contains((event.x, event.y)):
            return None  # early return

        dx = event.x - self.area.x
        dy = event.y - self.area.y
        current_angle = math.atan2(dy, dx)  # Calculate angle from center to mouse
        self.angle = math.degrees(current_angle)

        # Calculate the change in angle
        delta_angle = current_angle - self.last_angle or 0
        self.last_angle = current_angle

        # Normalize the delta_angle to be between -pi and pi
        if delta_angle > math.pi:
            delta_angle -= math.tau
        elif delta_angle < -math.pi:
            delta_angle += math.tau

        self.angle_increase() if delta_angle > 0 else self.angle_decrease()

    @property
    def angle(self) -> int:
        """change to move the knob"""
        return self._angle

    @angle.setter
    def angle(self, value: int) -> None:
        self._angle = int(value)
        self._update_angle()

    @angle.deleter
    def angle(self) -> None:
        self._angle = 0
        self._update_angle()

    def angle_increase(self, steps: SupportsFloat | None = None):
        self.angle += self.steps if steps is None else float(steps)
        self.master.event_generate(self.event_increase)

    def angle_decrease(self, steps: SupportsFloat | None = None):
        self.angle -= self.steps if steps is None else float(steps)
        self.master.event_generate(self.event_decrease)


if __name__ == "__main__":
    from src.support.circle import circle_saw_polygon

    polygon = circle_saw_polygon(100, 95)

    root = tk.Tk()
    root.configure(background="red")

    knob_ud = Knob(root, polygon, bg="green", borderwidth=0)
    knob_ud.itemconfigure(knob_ud.polygon_id, smooth=1, fill="white", outline="black")

    knob_ud.pack()
    knob_lr = Knob(root, polygon)
    knob_lr.itemconfigure(knob_lr.polygon_id, smooth=1, fill="pink", outline="black")
    knob_lr.pack()

    root.bind(knob_ud.event_increase, lambda e: knob_lr.angle_increase())
    root.bind(knob_ud.event_decrease, lambda e: knob_lr.angle_decrease())

    root.mainloop()

    # c = count()
    #
    # root = tk.Tk()
    # # knob = tk.Button()
    #
    # knob = Knob(root, polygon, polygon_opts={"fill": "white", "outline": "black"})
    # knob.pack()
    #
    # root.bind(knob.event_increase, lambda e: print("increase", next(c)))
    # root.bind(knob.event_decrease, lambda e: print("decrease", next(c)))
    # root.mainloop()
