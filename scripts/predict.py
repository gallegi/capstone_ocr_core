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
# recognizer.model = load_model('logs/recognizer.h5')
recognizer.model.load_weights('weights/recognizer.h5')
image_paths = glob.glob('test images/*')

for image_path in tqdm(image_paths):
    image_name = image_path.split(os.sep)[-1]
    image = tools.read(image_path)
    boxes = detector.detect(images=[image])[0]
    predictions = recognizer.recognize_from_boxes(image=image, boxes=boxes)

    # Plot the results.
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 10))

    # canvas = detection.drawBoxes(image, boxes)
    canvas = detection.drawBoxes(image=image, boxes=boxes)

    ax1.imshow(image)
    ax2.imshow(canvas)

    for text, box in predictions:
        ax2.annotate(s=text, xy=box[0], xytext=box[0] - 50)

    # plt.savefig('test results/'+image_name)
    plt.show()
