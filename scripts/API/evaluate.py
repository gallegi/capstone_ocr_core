import glob
import json
import os
import numpy as np
import cv2
from sklearn.metrics import confusion_matrix
from Entities.Evaluator import Evaluator
from Entities.Box import Box
from Entities.Image import Image
from Entities.Predict import Predict

LABEL_SOURCE = 'data/0325updated.task1train(626p)/'
json_paths = glob.glob('data/ocr_results_techchain/*.json')
IOU_THRESH_HOLD = 0.5


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


def compute_acc_box(predicts, labels):
    y_true = []
    y_label = []

    boxes = [] #Union box

    for predict in predicts:
        max_predict


    false_positive = np.array(false_positive)
    false_positive = (false_positive > IOU_THRESH_HOLD).astype(int)

    true_positive = sum(true_positive)
    false_positive = sum(false_positive)

    precision = true_positive/(true_positive+false_positive)
    recall = true_positive/(true_positive+false_negative)



for json_path in json_paths:
    image_name = json_path.split(os.sep)[-1].split('.')[0]
    label_path = LABEL_SOURCE + '/{}.txt'.format(image_name)

    image = Image(LABEL_SOURCE + '/{}.jpg'.format(image_name))
    labels = read_label(label_path)

    predicts = read_data(json_path)

    ### DRAW LABEL
    # for label in labels:
    #     image.draw_predict(label)

    ### DRAW PREDICT
    # for predict in predicts:
    #     image.draw_predict(predict)

    h, w, c = image.mat.shape

    blank_label = Image(image=np.zeros(shape=(h, w)))
    blank_predict = Image(image=np.zeros(shape=(h, w)))
    for predict in predicts:
        blank_predict.draw_box(predict.box, color=1)
    for label in labels:
        blank_label.draw_box(label.box, color=1)

    MEAN_IOU = Evaluator.compute_iou(blank_label.mat, blank_predict.mat)
    print(MEAN_IOU)

    image.show()
