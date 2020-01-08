class Label:
    def __init__(self, image, boxs, word):
        self.image = image
        self.boxs = boxs
        self.word = word

    def __iter__(self):
        return self.image, self.boxs, self.word
