import abc


class AbtractModel:
    def __init__(self):
        self.load_weights()

    @abc.abstractmethod
    def predict(self):
        pass

    @abc.abstractmethod
    def fit(self):
        pass

    @abc.abstractmethod
    def pre_process(self):
        pass

    @abc.abstractmethod
    def post_process(self):
        pass

    @abc.abstractmethod
    def load_weights(self):
        pass

    @abc.abstractmethod
    def save_weights(self):
        pass