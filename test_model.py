from pyvjoy import VJoyDevice
from screenshot import Screenshoter
from model import tflearn_model
from time import sleep
import cv2
import json

config = json.loads(open("config.json", 'r').read())


device = VJoyDevice(1)
center = 0x7FFF // 2
device.data.wAxisX = center
device.data.wAxisY = center
device.data.wAxisZ = center
device.data.wAxisXRot = center
device.data.wAxisYRot = center
device.update()

print("Starting!")
sleep(3)

model = tflearn_model()
model.load(config['model_save_name'])

screenshoter = Screenshoter(config['window_name'])

while True:
    image = screenshoter.grab_screenshot()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image[:][200:464], (200, 66))
    prediction = model.predict([image.reshape(200, 66, 1)])
    print(prediction)