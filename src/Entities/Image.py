import cv2

from Entities.Predict import Predict


class Image:
    def __init__(self, image):
        if type(image) is str:
            self.mat = cv2.imread(image)
        else:
            self.mat = image

    def draw_box(self, box, color=(0, 255, 0), thickness=2):
        cv2.rectangle(self.mat, (box.xmin, box.ymin), (box.xmax, box.ymax), color, thickness)
        return self.mat

    def draw_predict(self, predict, text_color=(0, 127, 255), box_color=(0, 255, 0), thickness=2, font_scale=1):
        predict: Predict

        self.mat = self.draw_box(predict.box, color=box_color, thickness=thickness)

        font = cv2.FONT_HERSHEY_SIMPLEX
        lineType = 2

        cv2.putText(self.mat, predict.text,
                    (predict.box.xmin, predict.box.ymin),
                    font,
                    font_scale,
                    text_color,
                    lineType)

        return self.mat
