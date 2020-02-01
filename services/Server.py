import base64
import sys

sys.path.append('../../src')
from io import BytesIO
import tornado
from imageio import imread
from tornado.web import Application, RequestHandler

import cv2
import sys

sys.path.append('src')
import matplotlib.pyplot as plt
import detection
import recognition
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
    include_top=True
)


class MainHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.render('templates/home.html', data={}, image_src='')

    def process(self, image):
        image = cv2.resize(image, (768, 1024))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        boxes = detector.detect(images=[image])[0]
        predictions = recognizer.recognize_from_boxes(image=image, boxes=boxes)
        canvas = detection.drawBoxes(image=image, boxes=boxes)
        plt.imshow(canvas)

        for text, box in predictions:
            plt.annotate(s=text, xy=box[0], xytext=box[0], size=3)

        plt.savefig('tmp/tmp.png', dpi=600)
        plt.clf()
        mat = cv2.imread('tmp/tmp.png')
        return mat

    def post(self):
        if len(self.request.files) == 0:
            self.write('No file detected')
            return
        file_body = self.request.files['image'][0]['body']
        mat = imread(BytesIO(file_body))
        mat = cv2.cvtColor(mat, cv2.COLOR_RGB2BGR)
        mat = self.process(mat)
        retval, buffer = cv2.imencode('.png', mat)
        png_as_text = base64.b64encode(buffer).decode()
        img_str = 'data:image/png;base64, {}'.format(png_as_text)
        self.render('templates/home.html', data={}, image_src=img_str)


class Application(Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": 'templates/js'}),
        ]
        settings = {
            "xsrf_cookies": False,
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class Server:
    def start(self, port):
        app = Application()
        app.listen(port)
        self.ready = True
        tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    server = Server()
    server.start(8080)
