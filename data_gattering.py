from input import Gamepad
from screenshot import Screenshoter
import time
import cv2
import os
import json
import numpy as np

class DataGatterer:
    def __init__(self, config):
        self.last_run_time = time.time() + 5 # Takes 5 seconds to start
        self.frametime = 1/config['fps']
        self.gamepad = Gamepad(0)
        self.screenshoter = Screenshoter(config['window_name'])
        self.data_path = os.path.join("data", config['save_dir'])
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
            os.makedirs(os.path.join(self.data_path, 'raw'))
            os.makedirs(os.path.join(self.data_path, 'cropped'))
        self.data_path = os.path.join(self.data_path, 'raw')

        _, _, filenames = next(os.walk(self.data_path))

        if filenames:
            self.image_id = max(int(name.split(".")[0]) for name in filenames) + 1
        else:
            self.image_id = 0

        if os.path.isfile("y_train.npy"):
            self.y = list(np.load("y_train.npy"))
        else:
            self.y = []



    def run(self):
        if time.time() - self.last_run_time > self.frametime:
            self.last_run_time = time.time()
            screen = self.screenshoter.grab_screenshot()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(self.data_path, str(self.image_id) + ".jpg"), screen)
            print(os.path.join(self.data_path, str(self.image_id) + ".jpg"))
            self.image_id += 1
            self.gamepad.update_data()
            self.y.append((self.gamepad.get_steer(), self.gamepad.get_acceleration()))

    def save_y(self):
        np.save("y_train.npy", self.y)


if __name__ == "__main__":
    config = json.loads(open('config.json', 'r').read())
    gatterer = DataGatterer(config)
    runtime = 600 #Run for 60 seconds,
    init_time = time.time()
    end_time = init_time + runtime
    print("Starting data gathering")
    while time.time() < end_time:
        gatterer.run()
    print("Finished!, got {} samples".format(len(gatterer.y)))
    gatterer.save_y()
