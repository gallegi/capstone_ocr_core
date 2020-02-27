import cv2
import requests
from tqdm import tqdm
import os
import glob

IMAGE_PATH = 'data/0325updated.task1train(626p)'
URL = 'http://app.gotai.ml/ocr/call/predict'
OUTPUT_PATH = 'data/ocr_results_techchain/'

image_names = glob.glob(IMAGE_PATH + '/*.jpg')
for image_path in tqdm(image_names):
    files = {'input': open(image_path, 'rb')}
    res = requests.post(URL, files=files,
                        data={'kv_model': '', 'ocr_model': 'jp', 'linecut_model': 'craft_tiny', 'alignment': 'true'})
    text = res.content.decode()
    open(OUTPUT_PATH + '/{}.json'.format(image_path.split(os.sep)[-1].split('.')[0]), 'w').write(text)
