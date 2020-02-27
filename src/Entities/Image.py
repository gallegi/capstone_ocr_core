import cv2

from Entities.Predict import Predict


class Image:
    def __init__(self, image):
        if type(image) is str:
            self.mat = cv2.imread(image)
        else:
            self.mat = image

        self._text_line_height = 20
        self.text_location = [0,self._text_line_height]

    def put_text(self,text,x = None,y=None,text_color=(0, 127, 0), box_color=(0, 255, 0), thickness=2, font_scale=1):

        if x and y is None :
            x,y = tuple(self.text_location)

        cv2.putText(self.mat, text,
                    (x,y),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    font_scale,
                    text_color,
                    2)

        self.text_location[1]+=self._text_line_height
        return self.mat

    def draw_boxes(self,boxes, color=(0, 255, 0), thickness=2):
        for box in boxes:
            self.draw_box(box,color,thickness)

        return self.mat

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

    def show(self, window_name='image', wait_key=0):
        cv2.imshow(window_name, self.mat)
        return cv2.waitKey(wait_key)
