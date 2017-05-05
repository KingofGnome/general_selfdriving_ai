import cv2
import os
import json
from tqdm import tqdm

config = json.loads(open("config.json", 'r').read())

data_path = os.path.join('data', config['save_dir'])
raw_images = os.path.join(data_path, 'raw')
save_dir = os.path.join(data_path, 'cropped')

_, _, image_names = next(os.walk(raw_images))
_, _, already_done = next(os.walk(save_dir))

image_names = set(image_names) - set(already_done)

for image_name in tqdm(image_names):
    img = cv2.imread(os.path.join(raw_images, image_name),0)
    img = cv2.resize(img[:][200:464], (200, 66))
    cv2.imwrite(os.path.join(save_dir, image_name), img)