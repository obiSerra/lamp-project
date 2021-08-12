from flask import Flask, request
from rgb import Leds
import threading

app = Flask(__name__)
leds = Leds()
leds.all_on((0, 0, 0))

@app.route("/leds", methods=['POST'])
def set_leds():
    leds.stop_animation()
    leds_config = request.get_json()
    if 'rgb' in leds_config:
        #todo add validation
        rgb_config = tuple(leds_config['rgb'])
        leds.all_on(rgb_config)

    return {'error': None, 'rgb': rgb_config}

@app.route("/leds/fade-to", methods=['POST'])
def fade_to():
    leds.stop_animation()
    leds_config = request.get_json()
    if 'fade' in leds_config:
        #todo add validation

        fade = leds_config['fade']

        step = 1
        speed = 0.1

        if 'rgb' not in fade:
            return {'error': 'missing RGB', 'rgb': None}

        rgb_config = tuple(fade['rgb'])
        if 'step' in fade:
            step = fade['step']
        if 'speed' in fade:
            speed = fade['speed']

        leds.fade_to(rgb=rgb_config, step=step, speed=speed)

    return {'error': None, 'rgb': rgb_config}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    try:
        
        app.run(host='0.0.0.0', port=80, debug=True)

    except KeyboardInterrupt:
        print("Manual Interruption")
        exit(1)
    finally:
        leds.all_off()
