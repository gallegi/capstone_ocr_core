import time

import tornado
from imageio import imread
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
import json
import cv2
from PIL import Image
import base64
import io
import numpy as np

import sys
import os 
sys.path.append("src")

from Controller.AIController import AIController
from Controller.OcrController import OcrController
from src.recognizer_master import RecognizerMaster
import tensorflow as tf
import traceback
import re

ocr_controller = OcrController()


class OcrHandler(RequestHandler):

    def process(self, mat, ocr_type=0):
        data = ocr_controller.ocr(mat, ocr_type)
        return data

    def get(self):
        self.render("public/index.html", image_src='', data={})

    def post(self, *args, **kwargs):
        if len(self.request.files) == 0:
            self.render('public/index.html', image_src='', data={})
            return
        try:
            file_body = self.request.files['file1'][0]['body']
            ocr_type = 1
            if 'ocr_type' in self.request.arguments:
                ocr_type = int(self.request.arguments['ocr_type'][0].decode())
            mat = imread(io.BytesIO(file_body))
            mat = cv2.cvtColor(mat, cv2.COLOR_RGB2BGR)
            img, data = self.process(mat, ocr_type)
            image_path = 'public/demo_{}.jpg'.format(time.strftime("%Y%m%d-%H%M%S"))
            cv2.imwrite(image_path, img)
            self.render('public/index.html', image_src=image_path, data=data)
        except:
            self.render('public/index.html', image_src='', data={})


def make_app():
    routes = [(r'/', OcrHandler),
              (r'/(?:public)/(.*)', tornado.web.StaticFileHandler, {'path': './public'}),
              ]
    return Application(routes)


if __name__ == '__main__':
    app = make_app()
    print('Start serving')
    app.listen(8888)
    IOLoop.current().start()
