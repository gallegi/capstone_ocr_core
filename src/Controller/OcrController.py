import sys

from Entities.Config import Config

sys.path.append("src")

from Entities.EntityRecognizer import EntityRecognizer
from Controller.AIController import AIController
import cv2



class OcrController:
    def __init__(self,config):
        self.ai_controller = AIController(config)
        self.ner = EntityRecognizer(config)


    #TODO: A lot of things to do here
    def get_form_id(self, text):
        return int(self.ai_controller.classify_form_id(text))

    def get_raw_text(self, text):
        return text

    def get_provinces(self, text):
        return self.ner.ner_province(text)

    def get_districs(self, text):
        return self.ner.ner_district(text)

    def get_public_administration(self, text):
        return self.ner.ner_cqhc(text)

    def get_profiles(self, text):
        return []

    def get_appointment_letter_code(self, text):
        return []

    def get_names(self, text):
        return self.ner.ner_person_names(text)

    def get_phone_numbers(self, text):
        return []

    def get_street_names(self, text):
        return []

    def get_personal_paper_types(self, text):
        return []

    def get_personal_paper_number(self, text):
        return []

    def get_issued_dates(self, text):
        return []

    def get_issued_place(self, text):
        return []

    def ocr(self, mat, ocr_type):

        if ocr_type == 0:
            imgs, texts = self.ai_controller.ocr_with_tess([mat])
        elif ocr_type == 1:
            imgs, texts = self.ai_controller.ocr_with_dl([mat])
        img = imgs[0]
        text = texts[0]
        data = {
            "form_id": self.get_form_id(text),
            "raw_text": self.get_raw_text(text),
            "province": self.get_provinces(text),  # (list tất cả các tỉnh thành có trên form)
            "district": self.get_districs(text),  # (nếu không có thì trả về array rỗng)
            "public_administration": self.get_public_administration(text),
            "profile": self.get_profiles(text),
            "appointment_letter_code": self.get_appointment_letter_code(text),
            "name": self.get_names(text),
            "phone_number": self.get_phone_numbers(text),
            "street": self.get_street_names(text),
            "personal_paper_type": self.get_personal_paper_types(text),
            "personal_paper_number": self.get_personal_paper_number(text),
            "issued_date": self.get_issued_dates(text),
            "issued_place": self.get_issued_place(text),
        }
        return img,data

    def set_new_doc_clf(self, new_doc_clf):
        '''Replace old document classifier by new one'''
        self.ai_controller.document_classifier = new_doc_clf
        

if __name__ == '__main__':
    ocr_controller = OcrController()
    if(len(sys.argv) == 1):
        data = ocr_controller.ocr(cv2.imread(r'F:\Github\ocrcore\test images\IMG_1169 (1).png'), ocr_type=1)
    elif(len(sys.argv) == 2):
        data = ocr_controller.ocr(cv2.imread(sys.argv[1]), ocr_type=1)
    elif(len(sys.argv) == 3):
        data = ocr_controller.ocr(cv2.imread(sys.argv[1]), ocr_type=int(sys.argv[2]))
    print(data)
