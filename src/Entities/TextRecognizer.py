import recognition
import tools
from Entities.AbtractModel import AbtractModel
from fullflow import recognizer


class TextRecognizer(AbtractModel):
    def predict(self, mats, boxes):
        return recognizer.recognize_from_boxes(images=mats, box_groups=boxes)

    def fit(self):
        pass

    def pre_process(self):
        pass

    def post_process(self):
        pass

    def load_weights(self):
        try:
            self.recognizer.training_model.load_weights(self.config.recognizer_weights_path)
        except:
            print("recognizer fail to load weights at : {}".format(self.config.recognizer_weights_path))

    def save_weights(self):
        pass

    def __init__(self, config):

        self.config = config
        self.alphabet = config.alphabet
        self.recognizer = recognition.Recognizer(
            width=200,
            height=31,
            stn=True,
            weights='kurapan',
            optimizer='RMSprop',
            include_top=0,
            attention=1
        )
        super().__init__()


    def recognize(self, mats, boxes):
        prediction_groups = self.predict(mats, boxes)
        predictions = [list(zip(predictions, boxes)) for predictions, boxes in zip(prediction_groups, boxes)]

        lines = tools.combine_to_line(predictions[0])
        return '\n'.join(lines)