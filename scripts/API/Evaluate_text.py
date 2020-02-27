# %%
import glob
import os
import matplotlib.pyplot as plt
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
import editdistance

LABEL_SOURCE = 'data/0325updated.task1train(626p)/'
json_paths = glob.glob('data/ocr_results_techchain/*.json')
IOU_THRESH_HOLD = 0.9

LOWER = False

def read_label(path):
    predicts = []
    try:
        label_lines = open(path).read().split('\n')[:-1]
    except:
        return None
    for line in label_lines:
        label = line.split(',')

        text = ','.join(label[8:])

        if LOWER :
            text = text.lower()
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
        text = line['text']
        if LOWER:
            text = text.lower()
        predict = Predict(box=box, text=text, confidence=line['confidence'], time_predict=time_predict)
        predicts.append(predict)
    w = data['output']['pages'][0]['width']
    h = data['output']['pages'][0]['height']
    return predicts, w, h


def compute_acc_box(predicts, labels, image):
    editdistances = []
    overlap_areas = []
    overlaps = []


    for predict in predicts:
        for label in labels:
            overlap_area = predict.box.compute_overlap(label.box)
            if overlap_area > 0:
                overlap_areas.append(overlap_area)

    for predict in predicts:
        max_predict_iou = 0
        for label in labels:
            max_predict_iou = max(max_predict_iou, label.box.compute_compute_iou(predict.box))
            if max_predict_iou >= IOU_THRESH_HOLD:
                overlaps.append((predict, label))
                break

    for predict, label in overlaps:
        edit_distance = 1 - editdistance.eval(predict.text, label.text) / max(len(predict.text), len(label.text))
        editdistances.append(edit_distance)
        # print(predict.text, label.text)
        # image.draw_box(predict.box, color=(0, 255, 0))
        # image.draw_box(label.box, color=(0, 0, 255))

    #     image.put_text('{}'.format(edit_distance), x=predict.box.xmin, y=predict.box.ymin)
    #     image.show(wait_key=0)
    #
    # image.show()
    #

    # predict_text = ''.join([predict.text for predict in predicts])
    # label_text = ''.join([label.text for label in labels])
    # edit_distance = 1-editdistance.eval(label_text, predict_text) / max(len(predict_text), len(label_text))
    # editdistances.append(edit_distance)
    return editdistances


ious = []
y_trues = np.array([])
y_preds = np.array([])
list_editdistances = []
# data = json.loads(open('data.json').read())
# json_paths = json_paths[:10]

for json_path in tqdm(json_paths):
    image_name = json_path.split(os.sep)[-1].split('.')[0]
    label_path = LABEL_SOURCE + '/{}.txt'.format(image_name)

    image = Image(LABEL_SOURCE + '/{}.jpg'.format(image_name))
    labels = read_label(label_path)
    if labels is None:
        continue

    predicts, w, h = read_data(json_path)
    blank_label = Image(image=np.zeros(shape=(h, w)))
    blank_predict = Image(image=np.zeros(shape=(h, w)))
    for predict in predicts:
        blank_predict.draw_box(predict.box, color=1)
    for label in labels:
        blank_label.draw_box(label.box, color=1)
    _editdistance = compute_acc_box(predicts, labels, image=image)
    list_editdistances += _editdistance
    # list_editdistances.append(np.array(_editdistance).mean())
    # print(editdistances)

list_editdistances = np.array(list_editdistances)
print('IOU THRESH HOLD : {} \t MEAN Edit distance : {}'.format(IOU_THRESH_HOLD, list_editdistances.mean()))
# %%
z = np.array([ious, list_editdistances])
z = np.sort(z, 1)
plt.plot(z[1], z[0], color='b')
# plt.plot(z[2],z[0],color='g')

Legend = plt.legend(('Mean edit distance', 'Mean IOU'), frameon=True, loc='best')
Legend.get_frame().set_edgecolor('k')

plt.xlabel('distance %')
plt.ylabel('IOU %')
plt.title('Evaluate speed - Model tiếng anh')
plt.show()

# %%
max(ious)
