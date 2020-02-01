import glob
import os
import sys

import cv2

sys.path.append('src')
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
    include_top=0
)

recognizer.model.load_weights('weights/recognizer.h5')
image_paths = glob.glob('test images/*')

for image_path in tqdm(image_paths):
    image_name = image_path.split(os.sep)[-1]
    image = tools.read(image_path)
    # image = ndimage.rotate(image, 90)
    h, w, c = image.shape
    image = cv2.resize(image, (int(w / 2), int(h / 2)))
    if image is None: continue
    try:
        boxes = detector.detect(images=[image])[0]
    except:
        continue
    predictions = recognizer.recognize_from_boxes(image=image, boxes=boxes)

    canvas = detection.drawBoxes(image=image, boxes=boxes)

    plt.imshow(canvas)

    for text, box in predictions:
        plt.annotate(s=text, xy=box[0], xytext=box[0], size=3)

    #         data = json.dumps(predictions)
    #         open('test results/'+image_name.split('.')[0]+'.json','w').write(data)
    plt.savefig('test results/' + image_name, dpi=600)
    plt.clf()
# plt.show()
