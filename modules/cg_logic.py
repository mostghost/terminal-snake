class CGLogic:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

        self.snake = [((int(x / 2), y - 1), "N-N"), ((int(x / 2), y - 2), "N-N")]
        self.snake_length = 6
        self.position_x = int(x / 2)
        self.position_y = y - 2
        self.direction = "N"
        self.prev_direction = "N"

    def update(self, inp: str):

        print(f"Input!:{inp}")

        if inp:
            self._change_direction(inp)

        self._move_snake()

        return self.snake

    def _change_direction(self, inp: str):
        match inp:
            case "W":
                if self.direction == "S":
                    return None
                else:
                    self.prev_direction = self.direction
                    self.direction = "N"
            case "A":
                if self.direction == "E":
                    return None
                else:
                    self.prev_direction = self.direction
                    self.direction = "W"
            case "S":
                if self.direction == "N":
                    return None
                else:
                    self.prev_direction = self.direction
                    self.direction = "S"
            case "D":
                if self.direction == "W":
                    return None
                else:
                    self.prev_direction = self.direction
                    self.direction = "E"

    def _move_snake(self):
        match self.direction:
            case "N":
                self.position_y -= 1
            case "S":
                self.position_y += 1
            case "W":
                self.position_x -= 1
            case "E":
                self.position_x += 1

        self.snake.append(
            (
                (self.position_x, self.position_y),
                (f"{self.direction}-{self.prev_direction}"),
            ),
        )

        if len(self.snake) > self.snake_length:
            self.snake.pop(0)
