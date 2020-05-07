# F:\Github\ocrcore\data\vnpost\vnpost_train_rotated
import glob
import os

import cv2
from tqdm import tqdm

from Entities.Config import Config
from Entities.DocumentDetector import DocumentDetector

document_detector = DocumentDetector(Config())
image_paths = glob.glob(r'C:\Users\Binh Bum\Downloads\Photos/batch_*/*/*.jpg',recursive=True)
for image_path in tqdm(image_paths):
    image_name = image_path.split(os.sep)[-1]
    mat = cv2.imread(image_path)
    doc_mat = document_detector.find_document(mat)
    cv2.imwrite(r'data/vnpost/vnpost_train_rotated/{}'.format(image_name),doc_mat)