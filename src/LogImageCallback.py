import random

import matplotlib.pyplot as plt
from keras.callbacks import Callback

import tools


class LogImageCallback(Callback):
    def __init__(self, validation_labels, recognizer):
        self.validation_labels = validation_labels
        self.recognizer = recognizer
        super().__init__()

    def on_epoch_end(self, epoch, logs=None):
        image_filepath, box, actual = random.choice(self.validation_labels)
        xmin, ymin, xmax, ymax = box[0][0], box[0][1], box[-1][0], box[-1][1]
        predicted = self.recognizer.recognize(image_filepath)
        print(f'Predicted: {predicted}, Actual: {actual}')
        image = tools.read(image_filepath)
        # image = detection.drawBoxes(image=image, boxes=[box])
        plt.annotate(predicted, box[0], color='green')
        _ = plt.imshow(image)
        plt.show()
