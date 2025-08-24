import os
import sys


class CGDisplay:

    def __init__(self):
        self.grid_x = 25
        self.grid_y = 15
        self.real_x = self.grid_x * 2

        self.grid = []
        self.rendered = []

    def update(self):
        self._create_grid()

        self._place_snake()

        self._append_border()

        os.system("clear")

        sys.stdout.write("\n".join(self.rendered) + "\n")

    def _create_grid(self):
        self.grid = [["  " for x in range(self.grid_x)] for x in range(self.grid_y)]

    def _place_snake(self):
        pass

    def _append_border(self):

        self.rendered = []

        a_l = "╭───────────────╮"
        b_l = "│ S  N  A  K  E │"
        c_l = "│ ┌─────────────┴"

        self.rendered.append(a_l + " " * (self.grid_x - len(a_l) + 3))
        self.rendered.append(b_l + " " * (self.grid_x - len(b_l) + 3))
        self.rendered.append(c_l + ("─" * ((self.real_x - len(c_l) + 3))) + "╮  ")

        for line in self.grid[:4]:
            self.rendered.append("│ │" + "".join(line) + "│  ")

        self.rendered.append("╰─┤" + "".join(self.grid[4]) + "│  ")

        self.rendered.append("  │" + "".join(self.grid[5]) + "│  ")

        self.rendered.append("  │" + "".join(self.grid[6]) + "├─╮")

        for line in self.grid[7:]:
            self.rendered.append("  │" + "".join(line) + "│ │")

        half_real = int(self.real_x / 2)

        self.rendered.append(
            "  ╰" + ("─" * (half_real - 1)) + "┬" + ("─" * (half_real) + "┘ │")
        )

        final_lines = [
            "Reset - R",
            "Move - WASD",
            "Toggle Screen Clear - X",
            "Quit - O",
        ]

        for line in final_lines:
            self.rendered.append(
                "   "
                + " " * (half_real - 1)
                + "│"
                + " " * (half_real - len(line) + 1)
                + line
                + " │"
            )

        self.rendered.append(
            "   " + (" " * (half_real - 1)) + "╰" + ("─" * (half_real) + "──╯")
        )