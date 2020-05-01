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

from Entities.Config import Config
from Entities.DocumentClassifier import DocumentClassifier
from Controller.AIController import AIController
from Controller.OcrController import OcrController
from src.recognizer_master import RecognizerMaster
import tensorflow as tf
import traceback
import re
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

config = Config()
ocr_controller = OcrController(config)

class OcrDemo(RequestHandler):

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
            file_body = self.request.files['image'][0]['body']
            ocr_type = 1
            if 'ocr_type' in self.request.arguments:
                ocr_type = int(self.request.arguments['ocr_type'][0].decode())
                print(ocr_type)
            mat = imread(io.BytesIO(file_body))
            mat = cv2.cvtColor(mat, cv2.COLOR_RGB2BGR)
            img, data = self.process(mat, ocr_type)
            image_path = 'public/demo_{}.jpg'.format(time.strftime("%Y%m%d-%H%M%S"))
            cv2.imwrite(image_path, img)
            self.render('public/index.html', image_src=image_path, data=data)
        except:
            raise
            self.render('public/index.html', image_src='', data={})

class OcrHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    def process(self, mat, ocr_type=0):
        data = ocr_controller.ocr(mat, ocr_type)
        return data

    def get(self):
        self.render("public/index.html", image_src='', data={})

    def post(self, *args, **kwargs):
        if len(self.request.files) == 0:
            print(self.request.data)
            print(self.request)
            self.write({'error':'request file is empty'})
            self.finish()
            return
        try:
            file_body = self.request.files['image'][0]['body']
            mat = imread(io.BytesIO(file_body))
            mat = cv2.cvtColor(mat, cv2.COLOR_RGB2BGR)
            img, data = self.process(mat, 0)
            image_path = 'public/demo_{}.jpg'.format(time.strftime("%Y%m%d-%H%M%S"))
            cv2.imwrite(image_path, img)
            print(data)
            self.write(data)
            self.finish()  # Without this the client's request will hang
        except:
            self.write({'error':'an error has occurred'})
            self.finish()  # Without this the client's request will hang

class RetrainHandler(RequestHandler):
    def post(self, *args, **kwargs): 
        doc_clf = DocumentClassifier(config)
        print(self.request.body)
        request_data = json.loads(self.request.body)
        doc_clf.train(request_data)
        doc_clf.save_models()
        ocr_controller.set_new_doc_clf(doc_clf)
        self.write({"ret": "cool"})
        self.finish()  # Without this the client's request will hang

def make_app():
    routes = [(r'/', OcrDemo),
              (r'/ocr', OcrHandler),
              (r'/(?:public)/(.*)', tornado.web.StaticFileHandler, {'path': './public'}),
              (r'/retrain', RetrainHandler)]
    return Application(routes)


if __name__ == '__main__':
    app = make_app()
    print('Start serving')

    if config.is_debug:
        port = config.port
    else:
        port = 80
    app.listen(port)
    IOLoop.current().start()
