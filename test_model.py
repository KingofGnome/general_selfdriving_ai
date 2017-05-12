from screenshot import Screenshoter
from model import tflearn_model
from time import sleep
from pyvjoy import VJoyDevice
import cv2
import json
import os

config = json.loads(open("config.json", 'r').read())

print("Starting!")
sleep(3)

model = tflearn_model()
model.load(os.path.join('data', config['save_dir'], 'model', config['model_save_name']))

device = VJoyDevice(1)
center = 0x7FFF // 2
device.data.wAxisX = center
device.data.wAxisY = center
device.data.wAxisZ = center
device.data.wAxisXRot = center
device.data.wAxisYRot = center
device.data.wAxisZRot = center
device.data.lButtons = 0

device.update()

screenshoter = Screenshoter(config['window_name'])

while True:
    image = screenshoter.grab_screenshot()
    image = cv2.resize(image[:][200:464], (200, 66))
    prediction = model.predict([image.reshape(200, 66, 3)])[0]

    device.data.wAxisX = int(((prediction[0] / 2) + 0.5) * 32767) # Evil floating point bit level hacking
    device.data.wAxisZRot = int(((((prediction[1] * -1) / 2) + 0.5) * 32767)) # What the fuck
    print('Steer: {}, Throttle: {}'.format(*prediction))
    device.update()
    sleep(0.05)