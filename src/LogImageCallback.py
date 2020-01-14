import random

import cv2
from keras.callbacks import Callback
import matplotlib.pyplot as plt
import tools


class LogImageCallback(Callback):
    def __init__(self,validation_labels,recognizer):
        self.validation_labels = validation_labels
        self.recognizer= recognizer

    def on_epoch_end(self, epoch, logs=None):
        image_filepath, box, actual = random.choice(self.validation_labels)
        xmin, ymin, xmax, ymax = box[0][0], box[0][1], box[-1][0], box[-1][1]
        predicted = self.recognizer.recognize_from_boxes(image_filepath, [box])[0][0]
        print(f'Predicted: {predicted}, Actual: {actual}')
        image = tools.read(image_filepath)
        # image = detection.drawBoxes(image=image, boxes=[box])
        image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), 2)
        plt.annotate(predicted, box[0])
        _ = plt.imshow(image)
        plt.savefig('logs/{}.png'.format(epoch))

