from __future__ import annotations
import board
import neopixel
import time
from typing import Tuple

# https://circuitpython.readthedocs.io/projects/neopixel/en/latest/


class Leds():
    def __init__(self, num: int = 60) -> Leds:
        self.pixels_num: int = num
        self.pixels = neopixel.NeoPixel(board.D18, num)
        self.current_rgb : Tuple(int, int, int)= (0, 0, 0)
        self.__reset_anim()

    def __reset_anim(self):
        self.is_animation_running = False
        self.stop_anim = False

    def stop_animation(self) -> None:
        if self.is_animation_running == True:
            self.stop_anim = True

    def all_off(self) -> None:
        self.all_on((0, 0, 0))

    def all_on(self, rgb: Tuple[int, int, int]) -> None:
        self.current_rgb = rgb
        self.pixels.fill(rgb)

    def pixel_on(self, i: int, rgb):
        self.pixels[i] = rgb

    def _next_fade(self, col: int, t_col: int, step: int) -> int:
        if col > t_col:
            return min(step, col - t_col)
        elif col < t_col:
            return -min(step, t_col - col)
        else:
            return 0

    def fade_to(self, rgb: Tuple[int, int, int] = (0, 0, 0), speed: float = 0.1, step: int = 1) -> None:
        target = [t for t in rgb]
        reached = False
        self.is_animation_running = True
        while not self.stop_anim and not reached:
            c_rgb = [c for c in self.current_rgb]
            nxt = [
                c_rgb[i] - self._next_fade(c_rgb[i], target[i], step) for i in range(3)]

            if nxt[0] == target[0] and nxt[1] == target[1] and nxt[2] == target[2]:
                reached = True
            self.current_rgb = tuple(nxt)

            self.all_on(self.current_rgb)
            time.sleep(speed)
        
        # Animation stopped, reset stop
        self.__reset_anim()


if __name__ == '__main__':
    try:
        leds = Leds()

        leds.all_on((0, 0, 0))
        time.sleep(2)
        while True:
            leds.fade_to(step=2, rgb=(255, 0, 0))
            leds.fade_to(step=2, rgb=(0, 255, 0))
            leds.fade_to(step=2, rgb=(0, 0, 255))

        leds.all_off()
    except KeyboardInterrupt:
        print("ctrl + c:")
    finally:
        leds.all_off()
