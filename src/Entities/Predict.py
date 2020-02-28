

class Predict:
    def __init__(self,box=None,text=None,confidence=None,time_predict=None):
        self.box = box
        self.text = text
        self.confidence=confidence

        self.time_predict= time_predict