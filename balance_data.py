import numpy as np
import os
import json

config = json.loads(open("config.json", 'r').read())

data_path = os.path.join('data', config['save_dir'])

_, _, filenames = next(os.walk(data_path))

for filename in filenames:
    data = np.load(data_path, filename)
    steer = np.array([data for data in data[:, 0]])[:, 0]
    above_pointone = np.where(np.abs(steer) > 0.1)