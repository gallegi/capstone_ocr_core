import sys
sys.path.append("src")

from Entities.Config import Config

from Entities.EntityRecognizer import EntityRecognizer
from Controller.AIController import AIController
import cv2
import glob
import  os
import pytesseract
from tqdm import tqdm

FOLDER = "D:\\FPT Education\\Capstone\\Documents\\30sample\\paddedImages"
OUT_FOLDER = "D:\\FPT Education\\Capstone\\AI module\\NER\\OCRResult"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def main():
    ai_controller = AIController(Config())
    os.makedirs(OUT_FOLDER, exist_ok=True)
    image_paths = glob.glob(os.path.join(FOLDER, "*"))

    for path in tqdm(image_paths):
        img = cv2.imread(path)
        name = path.split("\\")[-1].split(".")[0]
        text = ai_controller.ocr_with_tess([img])[1][0]
        with open(os.path.join(OUT_FOLDER, name+".txt"), 'w', encoding='utf-8') as f:
            f.write(text)

main()