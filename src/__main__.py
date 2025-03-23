import tkinter as tk

from src.widget.knob import Knob
from src.widget.etch import Etch
from src.widget.dragable import ShakeableWidget
from src.support.circle import circle_saw_polygon

SIZE_REDUCTION = 1.5
ETCH_RED = "#FF3737"
ETCH_GREY = "#C0C0C0"
ETCH_PAD = 125 / SIZE_REDUCTION
ETCH_STEPS = 2 / SIZE_REDUCTION
ETCH_WIDTH = 1000 / SIZE_REDUCTION
ETCH_HEIGHT = 600 / SIZE_REDUCTION
KNOB_OUTER = 150 / SIZE_REDUCTION
KNOB_INNER = 140 / SIZE_REDUCTION


def main(root: tk.Tk | None = None) -> int:
    if root is None:
        root = tk.Tk()
    try:
        etch(root)
        root.mainloop()
    except KeyboardInterrupt:
        pass
    return 0

def etch(root: tk.Tk | None = None) -> int:
    knob_polygon = circle_saw_polygon(KNOB_OUTER, KNOB_INNER)

    root.title("Etch A Sketch")
    root.configure(background=ETCH_RED)

    etch_width = ETCH_WIDTH
    etch_height = ETCH_HEIGHT
    etch = Etch(
        root,
        background=ETCH_GREY,
        width=etch_width,
        height=etch_height,
    )
    etch.move_steps = ETCH_STEPS
    etch.grid(column=1, row=1, sticky=tk.N + tk.E + tk.S + tk.W, padx=(0, 0), pady=(ETCH_PAD, 0))

    # horizontal
    knob_left = Knob(root, knob_polygon, background=ETCH_RED, border=0, highlightthickness=0)
    knob_left.event_increase = "<<KnobLeftIncrease>>"
    knob_left.event_decrease = "<<KnobLeftDecrease>>"
    knob_left.itemconfigure(knob_left.polygon_id, fill="white", outline="black", smooth=1)
    knob_left.grid(column=0, row=2, sticky=tk.N + tk.E + tk.S + tk.W, padx=(5, 0), pady=(0, 5))
    root.bind(knob_left.event_increase, etch.move_right)
    root.bind(knob_left.event_decrease, etch.move_left)

    # vertical
    knob_right = Knob(root, knob_polygon, background=ETCH_RED, border=0, highlightthickness=0)
    knob_right.event_increase = "<<KnobRightIncrease>>"
    knob_right.event_decrease = "<<KnobRightDecrease>>"
    knob_right.itemconfigure(knob_left.polygon_id, fill="white", outline="black", smooth=1)
    knob_right.grid(column=3, row=2, sticky=tk.N + tk.E + tk.S + tk.W, padx=(0, 5), pady=(0, 5))
    root.bind(knob_right.event_increase, etch.move_up)
    root.bind(knob_right.event_decrease, etch.move_down)

    shake = ShakeableWidget(etch)
    root.bind(shake.event_shake, etch.reset)
    root.bind('<Escape>', lambda e: root.destroy())
    # root.wm_attributes('-type', 'splash')

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
