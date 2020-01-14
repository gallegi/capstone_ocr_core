import glob
import os
import string
import sys

sys.path.append('src')
import tensorflow as tf
import matplotlib.pyplot as plt
from tqdm import tqdm
import detection
import recognition
import tools
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

detector = detection.Detector()
recognizer = recognition.Recognizer(
    width=200,
    height=31,
    stn=True,
    weights='kurapan',
    optimizer='RMSprop',
    include_top=False
)

recognizer.model.load_weights('weights/recognizer.h5')
image_paths = glob.glob('test images/*')

for image_path in tqdm(image_paths):
    image_name = image_path.split(os.sep)[-1]
    image = tools.read(image_path)
    boxes = detector.detect(images=[image])[0]
    predictions = recognizer.recognize_from_boxes(image=image, boxes=boxes)

    canvas = detection.drawBoxes(image=image, boxes=boxes)

    plt.imshow(canvas)

    for text, box in predictions:
        plt.annotate(s=text, xy=box[0], xytext=box[0],size=3)



    plt.savefig('test results/'+image_name,dpi=600)
    plt.clf()
    # plt.show()
