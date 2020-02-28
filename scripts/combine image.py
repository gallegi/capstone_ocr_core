import glob
import os

import cv2
import numpy as np

limit = 20 * 10 ** 6
image_names = glob.glob('/home/linhnq3/Disk2T/khanhtd2/utop/bill_images/*')
f = open('/home/linhnq3/Disk2T/khanhtd2/utop/combine_log.txt', 'a')
total_size = 0
images = []
max_width = 0
total_height = 0
count = 0
final_image = None


def combine(images):
    final_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)
    current_y = 0
    for image in images:
        final_image[current_y:image.shape[0] + current_y, :image.shape[1], :] = image
        current_y += image.shape[0]
    return final_image


total_images = len(image_names)

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
fontScale = 1
fontColor = (255, 255, 255)
lineType = 1

while len(image_names) > 0:
    while len(images)<60 and len(image_names) > 0:
        name = image_names.pop()
        print('Processing  : {} %'.format(round((1 - len(image_names) / total_images) * 100, 2)),end='\r')
        mat = cv2.imread(name)
        if mat is None:
            continue

        h, w, c = mat.shape
        blank = np.zeros((h + 40, w, c), dtype=np.uint8)

        bottomLeftCornerOfText = (0, h+17)
        # print(name.split(os.sep)[-1])
        blank = cv2.putText(blank,'image_name : '+ name.split(os.sep)[-1],
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,lineType
                    )
        # cv2.imshow('blank',blank)
        blank[:h, :, :] = mat
        mat = blank
        h, w, c = mat.shape
        images.append(mat)
        if images[-1].shape[1] > max_width:
            max_width = images[-1].shape[1]

        f.write('{}\t{}\t{}\t{}\n'.format('image_{}.jpg'.format(count), name, total_height, total_height + h))
        total_height += images[-1].shape[0]
        final_image = combine(images)


    total_size = 0
    images = []
    cv2.imwrite('/home/linhnq3/Disk2T/khanhtd2/utop/processed/image_{}.jpg'.format(count), final_image)
    count += 1
    max_width = 0
    total_height = 0
    final_image = None
