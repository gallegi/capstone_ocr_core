import detection
from Entities.AbtractModel import AbtractModel


class TextDetector(AbtractModel):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.detector = detection.Detector()

    def predict(self, mats):
       return  self.detector.detect(images=mats)

    def fit(self):
        pass

    def pre_process(self):
        pass

    def post_process(self):
        pass

    def load_weights(self):
        pass

    def save_weights(self):
        pass

    def find_words(self, mat):
        return self.predict([mat])
