from modules import cg_input
from modules import cg_logic
from modules import cg_display

import time
import sys
import termios
import fcntl


class MainLoop:

    def __init__(self):
        # We're making a copy of the original terminal settings for restoring.
        # The input method on linux must mess with the terminal to work.

        self.fd = sys.stdin.fileno()
        self.old_term = termios.tcgetattr(self.fd)
        self.old_flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)

        self.x = 30  # Minimum 22 because of border formatting
        self.y = 15

        self.input_manager = cg_input.CGInput()
        self.logic_manager = cg_logic.CGLogic(self.x, self.y)
        self.display_manager = cg_display.CGDisplay(self.x, self.y)

        self.TARGET_FPS = 60
        self.TARGET_DURATION = 1.0 / self.TARGET_FPS

        self.dead = False
        self.reset = False

        self.game_clock = 0

        self.delta_set()  # Just to initialize it, it won't actually be used here.

    def delta_set(self):
        self.delta_start = time.time()

    def delta_end(self):
        delta_end = time.time()

        delta_elapsed = delta_end - self.delta_start
        delta_frame = self.TARGET_DURATION - delta_elapsed

        if delta_frame > 0:
            time.sleep(delta_frame)

    def run(self):
        try:
            while True:

                self.game_clock += 1

                self.delta_set()

                inp = self.input_manager.update()

                # Some special exceptions should get handled by the game client:
                if inp == "O":
                    sys.exit()

                if inp == "R":
                    self.reset = True
                    self.dead = False

                if inp == "X":
                    self.display_manager.toggle_clear()

                if self.reset:
                    if inp in ["B", "V", "N", "M"]:
                        self.logic_manager.reset()
                        self.display_manager.reset()
                        self.logic_manager.set_gamespeed(inp)
                        self.reset = False
                        continue

                    self.display_manager.render("NewGame")
                    self.delta_end()
                    continue

                snake, head, fruit, dead = self.logic_manager.update(
                    inp, self.game_clock
                )

                if dead:
                    self.dead = True

                if self.dead:
                    self.display_manager.dead_update(dead)
                else:
                    self.display_manager.update(snake, head, fruit)

                self.display_manager.render("Normal")

                self.delta_end()

        finally:
            termios.tcsetattr(self.fd, termios.TCSANOW, self.old_term)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.old_flags)


loop = MainLoop()

loop.run()
