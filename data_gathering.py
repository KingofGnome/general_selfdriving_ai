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
        self.last_run_time = time.time()
        self.frametime = 1/config['fps']
        self.gamepad = Gamepad(config['input_type'])
        self.screenshoter = Screenshoter(config['window_name'])
        self.data_path = os.path.join("data", config['save_dir'])
        self.samples = 0
        self.max_samples = config['max_samples_per_file']
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)

        *_, file_names = next(os.walk(self.data_path))

        if file_names:
            self.fileid = max(int(filename.split(".")[0]) for filename in file_names)
        else:
            self.fileid = 0

        if os.path.isfile(os.path.join(self.data_path, str(self.fileid) + ".npy")):
            self.y = list(np.load(os.path.join(self.data_path, str(self.fileid) + ".npy")))
            self.samples = len(self.y)
            if self.samples >= self.max_samples:
                self.fileid += 1
                self.y = []
                self.samples = 0
        else:
            self.y = []

        print("Finished init, waiting 5 seconds before starting to get data")
        time.sleep(5)

    def run(self):
        if time.time() - self.last_run_time > self.frametime:
            self.last_run_time = time.time()
            self.gamepad.update_data()
            screen = self.screenshoter.grab_screenshot() # TODO: Screenshot the right area to remove the need of cropping
            screen = cv2.resize(screen[:][200:464], (200, 66))
            self.y.append([[self.gamepad.get_steer(), self.gamepad.get_acceleration()], screen])
            self.samples += 1
            print("Got sample!")

            if self.samples >= self.max_samples: # Just to make sure
                print("Saving!")
                self.save_y()
                self.fileid += 1
                self.y = []
                self.samples = 0

    def save_y(self):
        np.save(os.path.join(self.data_path, str(self.fileid) + ".npy"), self.y)


#  TODO: Fix pausing and early stopping
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Usage: python data_gathering.py seconds_to_run")

    config = json.loads(open('config.json', 'r').read())
    gatherer = DataGatherer(config)
    runtime = int(sys.argv[1])
    init_time = time.time()
    end_time = init_time + runtime
    print("Gathering data for {} seconds".format(runtime))
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

        gatherer.run()
    print("Finished!, got {} samples".format(len(gatherer.y)))
    gatherer.save_y()
