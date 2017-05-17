from screenshot import Screenshoter
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

"""
If i import both people will need to have both installed, maybe a try; except would
be more pythonic?
"""
if config['output_type'] == "pyxinput":
    device = __import__("pyxinput_output").PYXInputController()
else:
    device = __import__("vjoy_output").PyVjoyController()


screenshoter = Screenshoter(config['window_name'])

while True:
    image = screenshoter.grab_screenshot()
    image = cv2.resize(image[:][200:464], (200, 66))
    prediction = model.predict([image.reshape(200, 66, 3)])[0]
    device.update(prediction)
    print('Steer: {}, Throttle: {}'.format(*prediction))