from model import tflearn_model
from tensorflow.python.framework.errors import NotFoundError
import os
import json
import numpy as np

#Do it if you have enough memory
LOAD_DATA_INTO_MEMORY = False

N_EPOCH = 5

config = json.loads(open("config.json", 'r').read())

MODEL_NAME = config['model_name']

data_path = os.path.join('data', config['save_dir'])

*_, file_names = next(os.walk(data_path))

num_files = len(file_names)

model = tflearn_model()

try:
    model.load(config['model_save_name'])
    print("Loaded previous trained model!")
except NotFoundError:
    print("No previously trained model found, starting from scratch")

if(LOAD_DATA_INTO_MEMORY):
    all_data = [np.load(os.path.join(data_path, str(i) + ".npy")) for i in range(num_files)]

for epoch in range(N_EPOCH):
    print("Running epoch ", epoch)
    for i in range(num_files):
        if (LOAD_DATA_INTO_MEMORY):
            data = all_data[i]
        else:
            data = np.load(os.path.join(data_path, str(i) + ".npy"))

        print(len(data))

        X = np.array([image for image in data[:, 1]]).reshape(-1, 200, 66, 1)

        y = np.array([data for data in data[:, 0]])

        X_train, y_train, X_test, y_test = X[:-100], y[:-100], X[-100:], y[-100:]

        model.fit({'input': X_train}, {'targets': y_train}, n_epoch=1, batch_size=128,
                  validation_set=({'input': X_test}, {'targets': y_test}),
                  validation_batch_size=64, snapshot_step=500, show_metric=True, run_id=MODEL_NAME)


model.save(config['model_save_name'])
