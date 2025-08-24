import sys


class CGLogic:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

        self.snake = [((int(x / 2), y - 1), "N-N"), ((int(x / 2), y - 2), "N-N")]
        self.snake_length = 6
        self.position_x = int(x / 2)
        self.position_y = y - 3
        self.direction = "N"
        self.prev_direction = "N"
        self.update_direction = "N"
        self.counter = 0
        self.head = ((self.position_x, self.position_y), "N")

    def update(self, inp: str):

        self.head = ((self.position_x, self.position_y), self.direction)

        if inp:
            self._change_direction(inp)

        if self.counter == 10:

            self.prev_direction = self.direction
            self.direction = self.update_direction

            self._move_snake()

            self.counter = 0

        else:
            self.counter += 1

        dead = self._check_death()

        return self.snake, self.head, dead

    def _change_direction(self, inp: str):
        match inp:
            case "W":
                if self.direction == "S":
                    return None
                else:
                    self.update_direction = "N"
            case "A":
                if self.direction == "E":
                    return None
                else:
                    self.update_direction = "W"
            case "S":
                if self.direction == "N":
                    return None
                else:
                    self.update_direction = "S"
            case "D":
                if self.direction == "W":
                    return None
                else:
                    self.update_direction = "E"

    def _move_snake(self):

        self.snake.append(
            (
                (self.position_x, self.position_y),
                (f"{self.direction}-{self.prev_direction}"),
            ),
        )

        match self.direction:
            case "N":
                self.position_y -= 1
            case "S":
                self.position_y += 1
            case "W":
                self.position_x -= 1
            case "E":
                self.position_x += 1

        if len(self.snake) > self.snake_length:
            self.snake.pop(0)

    def _check_death(self):
        dead = False

        if self.position_x <= -1 or self.position_x == (self.grid_x):
            x = max(0, min(self.position_x, self.grid_x - 1))  # Clamps to acceptable range
            dead = (x, self.position_y)
        if self.position_y <= -1 or self.position_y == (self.grid_y):
            y = max(0, min(self.position_y, self.grid_y - 1))
            dead = (self.position_x, y)

        locations, _ = zip(*self.snake)
        current = (self.position_x, self.position_y)
        if current in locations:
            dead = (self.position_x, self.position_y)

        return dead
