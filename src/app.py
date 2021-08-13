from flask import Flask, request, send_from_directory
from rgb import Leds
import threading
from flask_cors import CORS
import time

app = Flask(__name__, static_folder='frontend',)
CORS(app)
leds = Leds()
leds.all_on((0, 0, 0))

lamp_t = None


class LampController(threading.Thread):
    def __init__(self, leds, anim, *args, **kwargs):
        super(LampController, self).__init__(*args, **kwargs)
        self.leds = leds
        self.anim = anim

    def run(self):
        print(threading.current_thread(), 'start {}'.format(self.anim['type']))
        step = 2 if 'step' not in self.anim or self.anim['step'] is None else self.anim['step']
        speed = 0.1 if 'speed' not in self.anim or self.anim['speed'] is None else self.anim['speed']
        if 'rgb' in self.anim and self.anim['rgb'] is not None:
            self.leds.fade_to(step=step, rgb=self.anim['rgb'], speed=speed)
        print(threading.current_thread(), 'done')


@app.route("/leds", methods=['POST', 'GET'])
def set_leds():
    global lamp_t, leds
    if request.method == 'POST':
        if lamp_t is not None:
            leds.stop_animation()
            lamp_t.join()
            lamp_t = None

        leds_config = request.get_json()
        if 'rgb' in leds_config:
            rgb_config = tuple(leds_config['rgb'])
            leds.all_on(rgb_config)

    return {'error': None, 'rgb': leds.current_rgb}


@app.route("/stop", methods=['POST'])
def stop_leds():
    global lamp_t, leds
    if lamp_t is not None:
        leds.stop_animation()
        lamp_t.join()
        lamp_t = None
        


    return {'error': None, 'rgb': leds.current_rgb}
@app.route("/leds/fade-to", methods=['POST'])
def fade_to():
    global lamp_t, leds
    if lamp_t is not None:
        leds.stop_animation()
        lamp_t.join()
        lamp_t = None

    leds_config = request.get_json()
    if 'rgb' in leds_config:
        # todo add validation
        rgb_config = tuple(leds_config['rgb'])

        
        speed = 5
        
        if 'speed' in rgb_config:
            speed = rgb_config['speed']

        step = speed

        anim = {'type': 'fade', 'rgb': rgb_config, 'step': step, 'speed': 0.1}

        print('start fade with ', anim)

        lamp_t = LampController(leds=leds, anim=anim, name="controller")
        lamp_t.start()
        return {'error': None, 'rgb': rgb_config}

    return {'error': None, 'rgb': None}

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('frontend/static', path)

if __name__ == '__main__':
    try:

        app.run(host='0.0.0.0', port=80, debug=True)

    except KeyboardInterrupt:
        print("Manual Interruption")
        exit(1)
    finally:
        leds.all_off()
