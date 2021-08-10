import board
import neopixel
import time


class Leds():
    def __init__(self, num=60):
        self.pixels_num = num
        #TODO update to work with keyboard and screen
        self.pixels = neopixel.NeoPixel(board.D18, num)
        
        self.current_rgb = (0, 0, 0)

    def all_off(self):
        self.all_on((0, 0, 0))

    def all_on(self, rgb):
        self.current_rgb = rgb
        self.pixels.fill(rgb)

    def pixel_on(self, i, rgb):
        self.pixels[i] = rgb

    def _next_fade(self, col, t_col, step):
        if col > t_col:
            return min(step, col - t_col)
        elif col < t_col:
            return -min(step, t_col - col)
        else:
            return 0
        
    def fade_to(self, rgb=(0, 0, 0), speed=0.1, step=1):
        target = [t for t in rgb]
        reached = False
        while not reached:
            c_rgb = [c for c in self.current_rgb]
            nxt = [c_rgb[i] - self._next_fade(c_rgb[i], target[i], step) for i in range(3)]
            
            if nxt[0] == target[0] and nxt[1] == target[1] and nxt[2] == target[2]:
               reached = True 
            self.current_rgb = tuple(nxt)
            
            self.all_on(self.current_rgb)
            time.sleep(speed)


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
