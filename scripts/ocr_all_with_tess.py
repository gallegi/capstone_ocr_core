import glob
import os

import cv2
import pytesseract
from tqdm import tqdm
import pandas as pd
from Controller.AIController import AIController
from Entities.Config import Config

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ai_controller = AIController(config=Config())

data_source = r'C:\Users\Binh Bum\Downloads\Photos\test_images/*'

list_image_names = []
list_texts = []

image_paths = glob.glob(data_source)
for image_path in tqdm(image_paths):
    mat = cv2.imread(image_path)
    imgs, texts = ai_controller.ocr_with_tess([mat])
    image_name = image_path.split(os.sep)[-1]
    text = texts[0]

    list_image_names.append(image_name)
    list_texts.append(text)

df = pd.DataFrame()
df['image_name'] = list_image_names
df['word'] = list_texts

df.to_json(r"C:\Users\Binh Bum\Downloads\Photos\test_label\tess_output.json")
