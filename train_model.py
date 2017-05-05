from model import tflearn_model
import os
import cv2
import json
import numpy as np

config = json.loads(open("config.json", 'r').read())

MODEL_NAME = config['model_name']

train_path = os.path.join('data', config['save_dir'], 'cropped')

_, _, image_names = next(os.walk(train_path))

X = (np.array([cv2.imread(os.path.join(train_path, image_name), cv2.IMREAD_GRAYSCALE) for image_name in image_names])
       .reshape(-1, 200, 66, 1))

print(len(X))

y = np.load('y_train.npy')

if len(image_names) != len(y):
    print("this is bad", len(image_names), len(y))

X_train, y_train, X_test, y_test = X[:-500], y[:-500], X[-500:], y[-500:]

model = tflearn_model()

model.fit({'input': X_train}, {'targets': y_train}, n_epoch=10, batch_size=128,
          validation_set=({'input': X_test}, {'targets': y_test}),
          validation_batch_size=64, snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

model.save(config['model_save_name'])
