from Controller.AIController import AIController
import cv2


class OcrController:
    def __init__(self):
        self.ai_controller = AIController()
    #TODO: A lot of things to do here
    def get_form_id(self, text):
        pass  # return id as int

    def get_raw_text(self, text):
        return text

    def get_provinces(self, text):

        pass  # return list of provinces

    def get_districs(self, text):
        pass  # return list of districts

    def get_public_administration(self, text):
        pass  # return list of public_administration

    def get_profiles(self, text):
        pass  # return list of profiles

    def get_appointment_letter_code(self, text):
        pass  # return list

    def get_names(self, text):
        pass  # return list of names

    def get_phone_numbers(self, text):
        pass  # return list of phone numbers

    def get_street_names(self, text):
        pass  # return list of street names

    def get_personal_paper_types(self, text):
        pass  # return list of personal paper types

    def get_personal_paper_number(self, text):
        pass  # return list of personal paper number

    def get_issued_dates(self, text):
        pass  # return list of issues dates

    def get_issued_place(self, text):
        pass  # return list of issues place

    def ocr(self, mat, ocr_type):

        if ocr_type == 0:
            imgs, texts = self.ai_controller.ocr_with_tess([mat])
        elif ocr_type == 1:
            imgs, texts = self.ai_controller.ocr_with_dl([mat])[0]
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


if __name__ == '__main__':
    ocr_controller = OcrController()
    data = ocr_controller.ocr(cv2.imread(r'F:\Github\ocrcore\test images\IMG_1169 (1).png'), ocr_type=1)
    print(data)
