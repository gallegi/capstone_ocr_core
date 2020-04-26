import glob

import matplotlib.pyplot as plt
from pytesseract import pytesseract
from tqdm import tqdm
import cv2

import detection
import tools
from Entities.Config import Config
from Entities.DocumentDetector import DocumentDetector
from Entities.TextDetector import TextDetector
from Entities.TextRecognizer import TextRecognizer
from Entities.DocumentClassifier import DocumentClassifier

pytesseract.tesseract_cmd = r"/home/nam/local/bin/tesseract"
doc_clf_model = "weights/"

class AIController:
    def __init__(self):
        config = Config()
        self.document_detector = DocumentDetector(config)
        self.text_detector = TextDetector(config)
        self.text_recognizer = TextRecognizer(config)
        self.document_classifier = DocumentClassifier(config)

    def ocr_with_dl(self, mats):
        texts = []
        imgs = []
        for mat in mats:
            # stage 1: detect document
            mat = self.document_detector.find_document(mat)
            # Stage 2: Detect text
            boxes = self.text_detector.find_words(mat)
            # Stage 3: Recognize text
            text = self.text_recognizer.recognize([mat], boxes)
            imgs.append(mat)
            texts.append(text)
        return imgs,texts

    def ocr_with_tess(self,mats):
        texts = []
        imgs = []
        for mat in mats:
            # stage 1: detect document
            mat = self.document_detector.find_document(mat)
            text = pytesseract.image_to_string(mat, lang='vie')
            imgs.append(mat)
            texts.append(text)
        return imgs,texts

    def classify_form_id(self, raw_text):
        '''Classify raw_text to get form id'''
        return self.document_classifier.predict(raw_text)

    def recognize_entiies(self,text):
        # TODO : Implement Ner here
        pass


if __name__ == '__main__':
    image_paths = glob.glob('test images/*')
    ai_controller = AIController()
    for path in tqdm(image_paths):
        ## Read image
        mat = tools.read(path)
        texts = ai_controller.ocr_with_tess([mat])
        print(texts)