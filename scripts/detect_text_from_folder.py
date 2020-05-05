import glob
import os
import sys
import cv2
import pandas as pd
from ar_markers import detect_markers
sys.path.append('src')
import matplotlib.pyplot as plt
from tqdm import tqdm
import detection
import recognition
import tools
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

# config = ConfigProto()
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)

data_source = r'C:\Users\Binh Bum\Downloads\Photos/'
detector = detection.Detector()

image_paths = glob.glob('{}/images/*'.format(data_source))
count = 0
detected_boxes = []
image_names = []
for image_path in tqdm(image_paths):
    image_name = image_path.split(os.sep)[-1]
    # image = tools.read(image_path)
    image = cv2.imread(image_path)
    markers = detect_markers(image)
    marker_contours = [marker.contours for marker in markers]
    for contour in marker_contours:
        image = cv2.drawContours(image,[contour],0,(255,255,255),-1)
    boxes = detector.detect(images=[image])[0]
    for box in boxes:
        detected_boxes.append(list(box.flatten()) + list(box.mean(axis=0)))
        image_names.append(image_name)


df = pd.DataFrame(columns=['x1','y1','x2','y2','x3','y3','x4','y4','x_mean','y_mean'],data=detected_boxes)
df['image_name'] = image_names
df.to_excel('sample.xlsx',index=False)