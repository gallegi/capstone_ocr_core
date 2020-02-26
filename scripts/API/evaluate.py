import glob
import json
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

LABEL_SOURCE = 'data/0325updated.task1train(626p)/'
json_paths = glob.glob('data/ocr_results_techchain/*.json')
IOU_THRESH_HOLD = .5


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

    return predicts


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


ious = []
y_trues = []
y_preds = []
for json_path in tqdm(json_paths):
    image_name = json_path.split(os.sep)[-1].split('.')[0]
    label_path = LABEL_SOURCE + '/{}.txt'.format(image_name)

    image = Image(LABEL_SOURCE + '/{}.jpg'.format(image_name))
    labels = read_label(label_path)

    predicts = read_data(json_path)

    # ### DRAW LABEL
    # for label in labels:
    #     image.draw_predict(label,box_color=(0,255,0))
    #
    # ## DRAW PREDICT
    # for predict in predicts:
    #     image.draw_predict(predict,box_color=(0,0,255))

    h, w, c = image.mat.shape

    blank_label = Image(image=np.zeros(shape=(h, w)))
    blank_predict = Image(image=np.zeros(shape=(h, w)))
    for predict in predicts:
        blank_predict.draw_box(predict.box, color=1)
    for label in labels:
        blank_label.draw_box(label.box, color=1)

    IOU = Evaluator.compute_iou(blank_label.mat, blank_predict.mat)
    ious.append(IOU)
    y_true, y_pred = compute_acc_box(predicts, labels)
    y_trues += list(y_true)
    y_preds += list(y_pred)



MEAN_IOU = np.array(ious).mean()
image.put_text('IOU : {}'.format(MEAN_IOU))
print('MEAN IOU : {}'.format(MEAN_IOU))

y_preds = np.array(y_preds)
y_trues = np.array(y_trues)
_y_preds = y_preds >= IOU_THRESH_HOLD
tn, fp, fn, tp = confusion_matrix(y_trues, _y_preds).ravel()
precision = tp/(tp+fp)
recall = tp/(tp+fn)

image.draw_boxes([x.box for x in predicts], color=(0, 255, 0))
image.draw_boxes([x.box for x in labels], color=(0, 0, 255))
image.put_text('Precision : {}'.format(precision))
image.put_text('Recall : {}'.format(recall))
print('p : {} , r {}'.format(precision,recall))
Evaluator.draw_PR_cureve(y_pred=y_preds, y_true=y_trues, iou_min_threshold=IOU_THRESH_HOLD)
# image.show(wait_key=0)
cv2.imwrite('test.png', image.mat)