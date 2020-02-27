#%%
import glob
import json_tricks as json
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
import matplotlib.pyplot as plt

LABEL_SOURCE = 'data/0325updated.task1train(626p)/'
json_paths = glob.glob('data/ocr_results_techchain/*.json')
IOU_THRESH_HOLD = .3


def read_label(path):
    predicts = []
    label_lines = open(path).read().split('\n')[:-1]
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
    return predicts,w,h,data['time']


def compute_acc_box(predicts, labels, image=None):
    y_true = []
    y_pred = []

    boxes = [x.box for x in predicts + labels]  # Union box
    overlap_boxes = []
    for predict in predicts:
        max_predict_iou = 0
        for label in labels:
            max_predict_iou = max(max_predict_iou, label.box.compute_overlap(predict.box))
        if max_predict_iou >= IOU_THRESH_HOLD:
            overlap_boxes.append(predict.box)

    for box in overlap_boxes:
        boxes.remove(box)

    for box in boxes:
        max_predict_iou = 0
        index = None
        for i, predict in enumerate(predicts):
            _iou = box.compute_overlap(predict.box)
            if _iou > max_predict_iou:
                index = i
                max_predict_iou = _iou
        y_pred.append(max_predict_iou)
        if index is not None:
            del predicts[index]

        max_label_iou = 0
        index = None
        for i, label in enumerate(labels):
            _iou = box.compute_overlap(label.box)
            if _iou > max_predict_iou:
                index = i
                max_label_iou = _iou
    y_true.append(max_label_iou)
    if index is not None:
        del labels[index]

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    y_true = y_true >= IOU_THRESH_HOLD
    # y_pred = y_pred >= IOU_THRESH_HOLD

    return y_true, y_pred

#%%

data = json.loads(open('data.json').read())

times = []
areas = []
total_requests = []
total_chars = []
ious= []
#%%
for json_path in tqdm(json_paths):
    image_name = json_path.split(os.sep)[-1].split('.')[0]
    if image_name not in data:
        continue
    iou = data[image_name]['iou']

    label_path = LABEL_SOURCE + '/{}.txt'.format(image_name)
    labels,w,h,time = read_data(json_path)
    area = w*h / 1e7
    areas.append(area)
    times.append(time)
    count_chars = sum([len(x.text) for x in labels])
    total_requests.append(len(total_requests))
    total_chars.append(count_chars)
    ious.append(iou)
#%%
counts = range(0,len(json_path))
print(np.array(times).mean())

z = np.array([times,total_chars,total_requests,ious])
z = np.sort(z,1)
plt.plot(z[2],z[0],color='b')
# plt.plot(z[2],z[0],color='g')

# Legend = plt.legend(('characters', 'boxes'), frameon=True, loc='best')
# Legend.get_frame().set_edgecolor('k')

plt.xlabel('Count candidate boxes')
plt.ylabel('Time (s)')
plt.title('Evaluate speed - Model tiếng anh')
plt.show()

#%%
max(ious)
