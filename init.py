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

        self.TARGET_FPS = 8
        self.TARGET_DURATION = 1.0 / self.TARGET_FPS

    def run(self):
        try:
            while True:
                delta_start = time.time()

                inp = self.input_manager.update()
                # One special exception as soon as we get input:
                if inp == "O":
                    sys.exit()

                snake = self.logic_manager.update(inp)

                self.display_manager.update(snake)

                delta_end = time.time()

                delta_elapsed = delta_end - delta_start
                delta_frame = self.TARGET_DURATION - delta_elapsed

                if delta_frame > 0:
                    time.sleep(delta_frame)

        finally:
            termios.tcsetattr(self.fd, termios.TCSANOW, self.old_term)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.old_flags)
            print("Goodbye.")


loop = MainLoop()

loop.run()
