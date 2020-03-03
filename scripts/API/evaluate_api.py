import glob
import json
import os

import cv2
import csv
import numpy as np
import requests
from tqdm import tqdm
import editdistance

image_names = glob.glob('test images/*')

def evaluate_api():
    sum_distance = 0
    list_acc = []
    for image_path in tqdm(image_names):
        image_name = image_path.split(os.sep)[-1].split('.')[0]

        original_text = ''.join(open('test labels/{}.txt'.format(image_name), 'r').readlines())
        original_text = ''.join(original_text.split())


        data = json.loads(open('test results/{}.json'.format(image_name)).read())
        temp = data['output']['pages'][0]['textlines']

        temp_string = ''
        for word in temp:
            text = word['text']
            temp_string = temp_string + text
        temp_string =''.join(temp_string.split())


        accuracy = 1 - editdistance.eval(original_text, temp_string) / max(len(original_text), len(temp_string))
        sum_distance = sum_distance + accuracy
        list_acc.append({'image_no' : image_name , 'acc' : accuracy})

    return list_acc, sum_distance


def average_acc(sum_distance):
    return sum_distance / len(image_names)

def write_to_csv(list_acc):
    cnt = 1
    with open('evaluated.csv', 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Image", "Accuracy"])
        for images in list_acc:
            writer.writerow([cnt, images['image_no'], images['acc']])
            cnt += 1



list_acc, sum_distance = evaluate_api()
write_to_csv(list_acc)
print("Average accuracy of this API: ", average_acc(sum_distance))

