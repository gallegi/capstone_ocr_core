#%%
import glob
import os

import chart_studio
import numpy as np
from plotly.graph_objs import *
import cv2
import plotly.express as px
from sklearn.metrics import confusion_matrix, precision_recall_curve
from tqdm import tqdm

from Entities.Evaluator import Evaluator
from Entities.Box import Box
from Entities.Image import Image
from Entities.Predict import Predict
import json_tricks as json
LABEL_SOURCE = 'data/japanese/'
json_paths = glob.glob('data/ocr_results_techchain_japanese/*.json')



def read_label(path):
    predicts = []
    try:
        label_lines = open(path).read().split('\n')[:-1]
    except:
        return  None
    for line in label_lines:
        label = line.split(',')

        text = ','.join(label[8:])
        numbers = [int(x) for x in label[:7]]
        numbers = np.array(numbers)

        xmin = numbers[0]
        ymin = numbers[1]
        xmax = numbers[2]
        ymax = numbers[5]

        box = Box(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        predict = Predict(box=box, text=text, confidence=1)
        predicts.append(predict)
    return predicts


def read_data(path):
    data = json.loads(open(path, encoding='utf-8').read())
    time_predict = data['time']
    predicts = []
    lines = data['output']['pages'][0]['textlines']
    for line in lines:
        polys = line['polys']
        xmin = polys[0][0]
        ymin = polys[0][1]
        xmax = polys[1][0]
        ymax = polys[3][1]
        box = Box(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

        predict = Predict(box=box, text=line['text'], confidence=line['confidence'], time_predict=time_predict)
        predicts.append(predict)
    w = data['output']['pages'][0]['width']
    h = data['output']['pages'][0]['height']
    return predicts,w,h

for json_path in json_paths:
    predicts, w, h = read_data(json_path)
    image_name = json_path.split(os.sep)[-1].split('.')[0]
    image = Image(LABEL_SOURCE + '/{}.jpeg'.format(image_name))
    for predict in predicts:
        image.draw_predict(predict)
    image.show()
cv2.imwrite('sample.png',image.mat)