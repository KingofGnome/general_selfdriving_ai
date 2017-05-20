from input_data.screen import ScreenGrabber
from model import tflearn_model
from time import sleep
import cv2
import json
import os



config = json.loads(open("config.json", 'r').read())

print("Starting!")
sleep(3)

model = tflearn_model()
model.load(os.path.join('data', config['save_dir'], 'model', config['model_save_name']))

if config['output_type'] == "pyxinput":
    try:
        from output.pyxinput import PYXInputController
    except ImportError:
        print("Failed to import PYXInputController, make sure you have everything set-up correctly")

    device = PYXInputController()
else:
    try:
        from output.vjoy import PyVjoyController
    except ImportError:
        print("Failed to import PYXInputController, make sure you have everything set-up correctly")

    device = PyVjoyController()


image_grabber = ScreenGrabber(config['window_name'])

while True:
    image = image_grabber.grab()
    image = cv2.resize(image[:][200:464], (200, 66))
    prediction = model.predict([image.reshape(200, 66, 3)])[0]
    device.update(prediction)
    print('Steer: {}, Throttle: {}'.format(*prediction))