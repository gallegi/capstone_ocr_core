import sys

sys.path.append('src')

from difflib import SequenceMatcher
import detection
import recognition
import tools
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)


class RecognizerMaster():

    def __init__(self):
        self.detector = detection.Detector()
        # self.recognizer = recognition.Recognizer()

        self.recognizer = recognition.Recognizer(
            width=200,
            height=31,
            stn=True,
            weights='kurapan',
            optimizer='RMSprop',
            include_top=False
        )
        self.recognizer.model.load_weights('weights/recognizer_CmndDataset.h5')

    def similar(self, first_content, second_content):
        return SequenceMatcher(None, first_content, second_content).ratio()

    def sort_first_element(self, elem):
        return elem[0]

    def sort_2nd_element(self, elem):
        return elem[1]

    def process_boxes_to_order_boxes(self, boxes):
        boxes_in_a_line = []
        order_boxes = []
        content = []
        for i in range(0, len(boxes) - 1):
            if boxes[i + 1][1] - boxes[i][1] < 2 * boxes[i][2] / 3:
                boxes_in_a_line.append(boxes[i])
            else:
                boxes_in_a_line.append(boxes[i])
                boxes_in_a_line.sort(key=self.sort_first_element)
                order_boxes.append(boxes_in_a_line)
                boxes_in_a_line = []
            if i == len(boxes) - 2:
                boxes_in_a_line.append(boxes[i + 1])
                boxes_in_a_line.sort(key=self.sort_first_element)
                order_boxes.append(boxes_in_a_line)
        for boxes_in_line in order_boxes:
            line_content = []
            for i in boxes_in_line:
                line_content.append(i[3])
            content.append(line_content)
        return order_boxes, content

    def get_infor(self, content, identify_key):
        key_content = ""
        key = identify_key.split()
        length_key = len(key)
        for list_text in content:
            if self.similar(list_text[0], key[0]) >= 0.5:
                for i in range(length_key, len(list_text)):
                    key_content += list_text[i] + ' '
                break
        return key_content

    def get_place(self, content, identify_key):
        key_content = ""
        try:
            key = identify_key.split()
            length_key = len(key)
            similar_pos = None
            for line_index in range(0, len(content)):
                if self.similar(content[line_index][0], key[0]) >= 0.6:
                    similar_pos = line_index
                    for i in range(length_key, len(content[line_index])):
                        key_content += content[line_index][i] + ' '
                    break
            for i in range(0, len(content[similar_pos + 1])):
                key_content += content[similar_pos + 1][i] + ' '
        except:
            pass
        return key_content

    def get_identify_number(self, content):
        for list_text in content:
            for text in list_text:
                if len(text) < 9:
                    continue
                try:
                    identify_number = int(text)
                    return identify_number
                except:
                    continue
        return ''

    def get_information_identify_credit_card(self, content):
        identify_key = ["số", "họ tên", "sinh ngày", "nguyên quán", "nơi dkhk thường trú"]
        identify_number = self.get_identify_number(content)
        name = self.get_infor(content, identify_key[1])
        date_of_birth = self.get_infor(content, identify_key[2])
        hometown = self.get_place(content, identify_key[3])
        permanent_place_of_residence = self.get_place(content, identify_key[4])

        return identify_number, name, date_of_birth, hometown, permanent_place_of_residence

    def create_json_infor(self, identify_number, name, date_of_birth, hometown, permanent_place_of_residence):
        information = {
            "ocr_content": {
                "identify_number": identify_number,
                "full_name": name,
                "dob": date_of_birth,
                "native_land": hometown,
                "permanent_address": permanent_place_of_residence
            }
        }
        return information

    def recognizer_image(self, image_path):
        image = tools.read(image_path)
        boxes = self.detector.detect(images=[image])[0]
        predictions = self.recognizer.recognize_from_boxes(image=image, boxes=boxes)

        list_box = []
        for text, box in predictions:
            list_box.append([box[0][0], box[0][1], box[3][1] - box[0][1], text])
        list_box.sort(key=self.sort_2nd_element)
        order_boxes, content = self.process_boxes_to_order_boxes(list_box)
        identify_number, name, date_of_birth, hometown, permanent_place_of_residence = self.get_information_identify_credit_card(
            content)
        json_file = self.create_json_infor(identify_number, name, date_of_birth, hometown, permanent_place_of_residence)
        return json_file
