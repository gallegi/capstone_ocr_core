import glob
import re
import time
import sys
sys.path.append('src')
import os
import matplotlib.pyplot as plt
from imageio import imread
from io import BytesIO
import cv2
import numpy as np
import pytesseract
import tensorflow.compat.v1 as tf
import tornado
from PIL import Image, ImageDraw, ImageFont
from pytesseract import Output
from tornado.web import RequestHandler
from tqdm import tqdm
import detection
import recognition
import tools
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
    include_top=0,
    attention=1
)

recognizer.training_model.load_weights('weights/vi_recognizer_v2.h5')
def load_graph(frozen_graph_filename, inputName, outputName):
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(
            graph_def,
            input_map=None,
            return_elements=None,
            name="prefix",
            op_dict=None,
            producer_op_list=None
        )
    x = graph.get_tensor_by_name('prefix/' + inputName + ':0')
    y = graph.get_tensor_by_name('prefix/' + outputName + ':0')
    return graph, x, y


def refineCorner(img, sess, x, y_eval, retainFactor):
    ans_x = 0.0
    ans_y = 0.0
    o_img = np.copy(img)
    y = None
    x_start = 0
    y_start = 0
    up_scale_factor = (img.shape[1], img.shape[0])
    myImage = np.copy(o_img)
    CROP_FRAC = retainFactor
    while (myImage.shape[0] > 10 and myImage.shape[1] > 10):
        img_temp = cv2.resize(myImage, (32, 32))
        img_temp = np.expand_dims(img_temp, axis=0)
        response = y_eval.eval(feed_dict={
            x: img_temp}, session=sess)
        response_up = response[0]
        response_up = response_up * up_scale_factor
        y = response_up + (x_start, y_start)
        x_loc = int(y[0])
        y_loc = int(y[1])

        if x_loc > myImage.shape[1] / 2:
            start_x = min(x_loc + int(round(myImage.shape[1] * CROP_FRAC / 2)), myImage.shape[1]) - int(round(
                myImage.shape[1] * CROP_FRAC))
        else:
            start_x = max(x_loc - int(myImage.shape[1] * CROP_FRAC / 2), 0)
        if y_loc > myImage.shape[0] / 2:
            start_y = min(y_loc + int(myImage.shape[0] * CROP_FRAC / 2), myImage.shape[0]) - int(
                myImage.shape[0] * CROP_FRAC)
        else:
            start_y = max(y_loc - int(myImage.shape[0] * CROP_FRAC / 2), 0)
        ans_x += start_x
        ans_y += start_y
        myImage = myImage[start_y:start_y + int(myImage.shape[0] * CROP_FRAC),
                  start_x:start_x + int(myImage.shape[1] * CROP_FRAC)]
        img = img[start_y:start_y + int(img.shape[0] * CROP_FRAC), start_x:start_x + int(img.shape[1] * CROP_FRAC)]
        up_scale_factor = (img.shape[1], img.shape[0])

    ans_x += y[0]
    ans_y += y[1]
    return (int(round(ans_x)), int(round(ans_y)))


def getCorners(img, sess, x, output):
    o_img = np.copy(img)
    myImage = np.copy(o_img)
    myImage = myImage.astype(np.uint8)
    img_temp = cv2.resize(myImage, (32, 32))
    img_temp = np.expand_dims(img_temp, axis=0)
    response = output.eval(feed_dict={
        x: img_temp}, session=sess)
    response = response[0]
    x = response[[0, 2, 4, 6]]
    y = response[[1, 3, 5, 7]]
    x = x * myImage.shape[1]
    y = y * myImage.shape[0]

    tl = myImage[max(0, int(2 * y[0] - (y[3] + y[0]) / 2)):int((y[3] + y[0]) / 2),
         max(0, int(2 * x[0] - (x[1] + x[0]) / 2)):int((x[1] + x[0]) / 2)]

    tr = myImage[max(0, int(2 * y[1] - (y[1] + y[2]) / 2)):int((y[1] + y[2]) / 2),
         int((x[1] + x[0]) / 2):min(myImage.shape[1] - 1, int(x[1] + (x[1] - x[0]) / 2))]

    br = myImage[int((y[1] + y[2]) / 2):min(myImage.shape[0] - 1, int(y[2] + (y[2] - y[1]) / 2)),
         int((x[2] + x[3]) / 2):min(myImage.shape[1] - 1, int(x[2] + (x[2] - x[3]) / 2))]

    bl = myImage[int((y[0] + y[3]) / 2):min(myImage.shape[0] - 1, int(y[3] + (y[3] - y[0]) / 2)),
         max(0, int(2 * x[3] - (x[2] + x[3]) / 2)):int((x[3] + x[2]) / 2)]

    tl = (tl, max(0, int(2 * x[0] - (x[1] + x[0]) / 2)), max(0, int(2 * y[0] - (y[3] + y[0]) / 2)))
    tr = (tr, int((x[1] + x[0]) / 2), max(0, int(2 * y[1] - (y[1] + y[2]) / 2)))
    br = (br, int((x[2] + x[3]) / 2), int((y[1] + y[2]) / 2))
    bl = (bl, max(0, int(2 * x[3] - (x[2] + x[3]) / 2)), int((y[0] + y[3]) / 2))
    return tl, tr, br, bl


def order_points(pts):
    pts = np.array(pts)
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


def ocr_full(rgb, min_conf=0.7, draw_box=False, display_text=False):
    d = pytesseract.image_to_data(rgb, lang='vie', output_type=Output.DICT)
    print('OCR tesseract finished')
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > min_conf * 100:
            text = d['text'][i]
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            if draw_box:
                cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 1)
            if display_text:
                img_pil = Image.fromarray(rgb)
                draw = ImageDraw.Draw(img_pil)
                draw.text((x, y + 10), text, font=font, fill=(0, 0, 255, 255))
                rgb = np.array(img_pil)
    return rgb, d

def ocr(mat):
    text = pytesseract.image_to_string(mat,lang='vie')
    print(text)
    keys = ['Tên','Địa chỉ','Số điện thoại','Số  thứ tự']
    regs = ['hồ sơ của:[ \t_]*([^\n\r]*)','chỉ:\s*([^\n\r]*)','điện thoại:\s*([0-9]*)','thứ tự:\s*([0-9]*)']
    data = {}
    for i,key in enumerate(keys):
        try:
            data[key] = re.search(regs[i], text)[1]
        except:
            data[key] = ''

    return mat,data

def find_document(img):
    h,w,c = img.shape
    data = getCorners(img, sessCorners, xCorners, yCorners)
    corner_address = []
    counter = 0
    for b in data:
        a = b[0]
        temp = np.array(refineCorner(a, sess, x, y, float(0.85)))
        temp[0] += b[1]
        temp[1] += b[2]
        corner_address.append(temp)
        counter += 1
    points = []
    for a in range(0, len(data)):
        cv2.line(img, tuple(corner_address[a % 4]), tuple(corner_address[(a + 1) % 4]), (255, 0, 0), 2)
        points.append(tuple(corner_address[a % 4]))
    img = four_point_transform(img, points)
    return img


def _process(origin):
    doc_mat = find_document(origin)

    img, data = ocr(doc_mat)

    image_path = 'public/demo_{}.jpg'.format(time.strftime("%Y%m%d-%H%M%S"))

    return data, image_path, img



if __name__ == "__main__":

    graph, x, y = load_graph('weights/cornerRefiner.pb', "Corner/inputTensor", "Corner/outputTensor")
    graphCorners, xCorners, yCorners = load_graph('weights/getCorners.pb', "Input/inputTensor",
                                                  "FCLayers/outputTensor")
    sess = tf.Session(graph=graph)
    sessCorners = tf.Session(graph=graphCorners)

    image_paths = glob.glob('test images/*')
    for path in image_paths:


        ## Read image
        mat = tools.read(path)
        h,w,c = mat.shape

        mat = cv2.resize(mat, (int(w / 1.3), int(h / 1.3)))

        ## corner detection, refine corner
        doc_mat = find_document(mat)
        ## Detect text box craft
        boxes = detector.detect(images=[doc_mat])[0]
        ## Recognize CRNN
        predictions = recognizer.recognize_from_boxes(image=doc_mat, boxes=boxes)


        ## Display


        image_name = path.split(os.sep)[-1]
        canvas = detection.drawBoxes(image=doc_mat, boxes=boxes)

        plt.imshow(canvas)

        for text, box in predictions:
            plt.annotate(s=text, xy=box[0], xytext=box[0], size=3)
        plt.savefig('test results/' + image_name+ '.png', dpi=600, bbox_inches='tight')
        plt.clf()
