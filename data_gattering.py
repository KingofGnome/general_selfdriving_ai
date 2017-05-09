from input import Gamepad
from screenshot import Screenshoter
import time
import cv2
import os
import json
import pygame
import sys
import numpy as np

class DataGatherer:
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
    gatterer = DataGatherer(config)
    if(len(sys.argv) != 2):
        print("Usage: python data_gattering.py seconds_to_run")
    runtime = int(sys.argv[1])
    init_time = time.time()
    end_time = init_time + runtime
    print("Gattering data for {} seconds".format(runtime))
    while time.time() < end_time:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            print("Paused!")
            pause_init = time.time()
            time.sleep(0.5)
            while not pygame.key.get_pressed()[pygame.K_p]:
                time.sleep(0.1)
            print("Unpaused!")
            end_time += time.time() - pause_init
        if keys[pygame.K_e]:
            print("Stopping early!")
            break

        gatterer.run()
    print("Finished!, got {} samples".format(len(gatterer.y)))
    gatterer.save_y()
