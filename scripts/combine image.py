import glob
import os

import cv2
import numpy as np

limit = 20 * 10 ** 6
image_names = glob.glob('test images/*')
f = open('combine_log.txt', 'a')
total_size = 0
images = []
max_width = 0
total_height = 0
count = 0
final_image = None


def get_sizes(mat):
    if mat is None:
        return 0
    cv2.imwrite('temp.jpg', mat)
    return os.path.getsize('temp.jpg')


def combine(images):
    final_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)
    current_y = 0
    for image in images:
        final_image[current_y:image.shape[0] + current_y, :image.shape[1], :] = image
        current_y += image.shape[0]
    return final_image


total_images = len(image_names)

while len(image_names) > 0:
    while get_sizes(final_image) < limit and len(image_names) > 0:
        name = image_names.pop()
        print('Processing  : {} %\r'.format(round((1 - len(image_names) / total_images) * 100, 2)))
        mat = cv2.imread(name)
        h, w, c = mat.shape
        images.append(mat)
        if images[-1].shape[1] > max_width:
            max_width = images[-1].shape[1]

        f.write('{}\t{}\t{}\t{}\n'.format('image_{}.jpg'.format(count), name, total_height, total_height + h))
        total_height += images[-1].shape[0]
        final_image = combine(images)

    total_size = 0
    images = []
    cv2.imwrite('image_{}.jpg'.format(count), final_image)
    count += 1
    max_width = 0
    total_height = 0
    final_image = None
