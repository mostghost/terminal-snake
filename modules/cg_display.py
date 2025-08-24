import os
import sys
import copy


class CGDisplay:

    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.real_x = self.grid_x * 2

        self.screen_clear = True

        self.prefix = []
        self.suffix = []
        self.suffix_newgame = []
        self._create_prefix()
        self._create_suffix()
        self._create_suffix_newgame()

        self.reset()

    def reset(self):
        self.grid = []
        self.rendered = []
        self.dead_grid = False
        self.death_counter = 0
        self.death_pos = (0, 0)

    def toggle_clear(self):
        self.screen_clear = not self.screen_clear

    def update(self, snake: list, head: tuple, fruit: tuple):

        self._create_grid()

        self._place_snake(snake)

        self._place_head(head)

        if fruit != (-1, -1):
            self._place_fruit(fruit)

        self._place_tail(snake[0])

    def dead_update(self, dead: tuple):

        if dead:
            self.death_pos = dead

        if self.death_counter < 5:
            self._dead_explosion(dead)
            self.death_counter += 1
            self.grid = copy.deepcopy(self.dead_grid)
        else:
            return

    def render(self, type: str):
        self.rendered = []

        self._append_border()

        self._append_suffix(type)

        if self.screen_clear:
            os.system("clear")

        sys.stdout.write("\n".join(self.rendered) + "\n")

    def _create_grid(self):
        self.grid = [["  " for x in range(self.grid_x)] for x in range(self.grid_y)]

    def _place_snake(self, snake: list):
        for position, direction_type in snake:
            x = position[0]
            y = position[1]

            # Note that direction type may be a little confusing - "N-W" does not
            # mean northwest, it means "coming from the west, we're going north"
            # So ("CURRENT-PREVIOUS").
            match direction_type:

                case "N-N":
                    self.grid[y][x] = "││"
                case "N-W":
                    self.grid[y][x] = "╘╧"
                case "N-E":
                    self.grid[y][x] = "╧╛"

                case "W-W":
                    self.grid[y][x] = "══"
                case "W-N":
                    self.grid[y][x] = "╤╕"
                case "W-S":
                    self.grid[y][x] = "╧╛"

                case "S-S":
                    self.grid[y][x] = "││"
                case "S-W":
                    self.grid[y][x] = "╒╤"
                case "S-E":
                    self.grid[y][x] = "╤╕"

                case "E-E":
                    self.grid[y][x] = "══"
                case "E-N":
                    self.grid[y][x] = "╒╤"
                case "E-S":
                    self.grid[y][x] = "╘╧"

    def _place_head(self, head):

        x = head[0][0]
        y = head[0][1]
        direction = head[1]

        match direction:
            case "N":
                self.grid[y][x] = "╒╕"
            case "W":
                self.grid[y][x] = "━═"
            case "S":
                self.grid[y][x] = "╘╛"
            case "E":
                self.grid[y][x] = "═━"

    def _place_tail(self, tail):
        x = tail[0][0]
        y = tail[0][1]
        direction = tail[1][0]

        match direction:
            case "N":
                self.grid[y][x] = "└┘"
            case "W":
                self.grid[y][x] = "═╴"
            case "S":
                self.grid[y][x] = "┌┐"
            case "E":
                self.grid[y][x] = "╶═"

    def _append_border(self):

        self.rendered.extend(self.prefix)

        for line in self.grid[:4]:
            self.rendered.append("│ │" + "".join(line) + "│  ")

        self.rendered.append("╰─┤" + "".join(self.grid[4]) + "│  ")

        self.rendered.append("  │" + "".join(self.grid[5]) + "│  ")

        self.rendered.append("  │" + "".join(self.grid[6]) + "├─╮")

        for line in self.grid[7:]:
            self.rendered.append("  │" + "".join(line) + "│ │")

    def _append_suffix(self, type: str):
        if type == "Normal":
            self.rendered.extend(self.suffix)
        elif type == "NewGame":
            self.rendered.extend(self.suffix_newgame)

    def _create_prefix(self):

        a_l = "╭────────────────────╮"
        b_l = "│ F L A T    W O R M │"
        c_l = "│ ┌──────────────────┴"

        self.prefix.append(a_l + " " * (self.grid_x - len(a_l) + 3))
        self.prefix.append(b_l + " " * (self.grid_x - len(b_l) + 3))
        self.prefix.append(c_l + ("─" * ((self.real_x - len(c_l) + 3))) + "╮  ")

    def _create_suffix(self):

        half_real = int(self.real_x / 2)

        self.suffix.append(
            "  ╰" + ("─" * (half_real - 1)) + "┬" + ("─" * (half_real) + "┘ │")
        )

        final_lines = [
            "Reset - R",
            "Move - WASD",
            "Toggle Screen Clear - X",
            "Quit - O",
        ]

        for line in final_lines:
            self.suffix.append(
                "   "
                + " " * (half_real - 1)
                + "│"
                + " " * (half_real - len(line) + 1)
                + line
                + " │"
            )

        self.suffix.append(
            "   " + (" " * (half_real - 1)) + "╰" + ("─" * (half_real) + "──╯")
        )

    def _create_suffix_newgame(self):

        half_real = int(self.real_x / 2)

        self.suffix_newgame.append(
            "  ╰" + ("─" * (half_real - 1)) + "┬" + ("─" * (half_real) + "┘ │")
        )

        final_lines = [
            "Slow - V",
            "Normal - B",
            "Fast - N",
            "Faster - M",
        ]

        for line in final_lines:
            self.suffix_newgame.append(
                "   "
                + " " * (half_real - 1)
                + "│"
                + " " * (half_real - len(line) + 1)
                + line
                + " │"
            )

        self.suffix_newgame.append(
            "   " + (" " * (half_real - 1)) + "╰" + ("─" * (half_real) + "──╯")
        )

    def _dead_explosion(self, dead):
        death_token = "░░"

        if not self.dead_grid:
            self.dead_grid = copy.deepcopy(self.grid)

            x = dead[0]
            y = dead[1]

            self.dead_grid[y][x] = death_token
            self.grid = copy.deepcopy(self.dead_grid)
            return

        old_grid = copy.deepcopy(self.dead_grid)

        for y, line in enumerate(old_grid):
            for x, _ in enumerate(line):
                neighbours = self._dead_get_surrounding(x, y, old_grid)

                if death_token in neighbours:
                    self.dead_grid[y][x] = death_token

    def _dead_get_surrounding(self, x, y, old_grid):

        height = self.grid_y
        width = self.grid_x

        surrounding = []

        for dy in [-1, 0, 1]:
            new_y = y + dy
            if 0 <= new_y < height:
                for dx in [-1, 0, 1]:
                    new_x = x + dx
                    if 0 <= new_x < width:
                        # Exclude the middle block:
                        if not (dx == 0 and dy == 0):
                            surrounding.append(old_grid[new_y][new_x])

        return surrounding

    def _place_fruit(self, fruit):

        x = fruit[0]
        y = fruit[1]

        self.grid[y][x] = "❴❵"

