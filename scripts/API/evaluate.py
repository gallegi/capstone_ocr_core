import glob
import json
import os

import cv2

LABEL_PATH = 'data/0325updated.task1train(626p)/'
json_paths = glob.glob('data/ocr_results_techchain/*.json')


for json_path in json_paths:
    image_name = json_path.split(os.sep)[-1].split('.')[0]
    mat = cv2.imread(LABEL_PATH+'/{}.jpg'.format(image_name))
    
    data = json.loads(open(json_path,encoding='utf-8').read())

