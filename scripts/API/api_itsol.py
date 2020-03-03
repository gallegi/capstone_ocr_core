import glob
import json
import os

import cv2
import numpy as np
import requests
from tqdm import tqdm

image_names = glob.glob('test images/*')


def crawl():
    url = 'http://app.gotai.ml/ocr/call/predict'

    for image_path in tqdm(image_names):
        files = {'input': open(image_path, 'rb')}
        res = requests.post(url, files=files, data={'ocr_model': 'jp'})
        text = res.content.decode()
        open('test results/{}.json'.format(image_path.split(os.sep)[-1].split('.')[0]), 'w').write(text)


def show():
    for image_path in tqdm(image_names):
        image_name = image_path.split(os.sep)[-1].split('.')[0]
        mat = cv2.imread(image_path)

        data = json.loads(open('test results/{}.json'.format(image_name)).read())
        h, w, c = mat.shape

        temp = data['output']['pages'][0]['textlines']

        for word in temp:
            text = word['text']
            box = word['polys']

            points = []
            for point in box:
                points.append([int(point[0] * w), int(point[1] * h)])
            contours = np.array([points])
            cv2.drawContours(mat, contours, -1, (0, 255, 0), 2)

            rect = cv2.boundingRect(contours[0])
            x, y, _w, _h = rect
            print(_w, _h)

        # cv2.imshow('mat',mat)
        # cv2.waitKey(0)
        # print(data)


def convert2labelme():
    for image_path in tqdm(image_names):
        labelme = {}
        image_name = image_path.split(os.sep)[-1]
        mat = cv2.imread(image_path)

        data = json.loads(open('test results/{}.json'.format(image_name.split('.')[0])).read())
        h, w, c = mat.shape

        labelme["version"] = "3.16.7"
        labelme["flags"] = {}
        labelme["shapes"] = []
        labelme['lineColor'] = [0, 255, 0, 128]
        labelme['fillColor'] = [255, 0, 0, 128]

        # data['predictions'] = []
        labelme['imageData'] = None
        labelme['imagePath'] = image_name
        labelme['imageHeight'] = h
        labelme['imageWidth'] = w

        temp = data['output']['pages'][0]['textlines']
        # temp2 = temp['pages']
        # temp3 = temp2[0]
        # temp4 = temp3['textlines']
        # temp5 = temp4[0]
        # temp6 = temp5['text']
        # print(temp)

        for word in temp:
            text = word['text']
            box = word['polys']

            points = []
            for point in box:
                points.append([int(point[0] * w), int(point[1] * h)])

            labelme['shapes'].append(
                {'label': text, 'line_color': None, 'fill_color': None, 'points': points,
                 'shape_type': 'polygon', 'flags': {}})

        with open('data/bills/{}.json'.format(image_name.split('.')[0]), 'w') as f:
            json.dump(labelme, f)


crawl()
# convert2labelme()
show()
