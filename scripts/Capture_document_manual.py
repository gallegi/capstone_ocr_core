import time
from pathlib import Path

import cv2


def create_folder(path):
    Path(path).mkdir(parents=True, exist_ok=True)


# cv2.imshow('t',np.zeros((23,23,3)))

source = "data/captured/"
create_folder(source)

cap = cv2.VideoCapture(1)
print('Init cap')
cap.set(3, 1080)
cap.set(4, 1920)
cap.set(28, 15)
page = 1
while True:
    ret, mat = cap.read()
    if not ret:
        break
    else:
        cv2.imshow('page {}'.format(page), mat)
        k = cv2.waitKey(1)
        page_source = source + 'Page_{}/'.format(page)
        if k == ord('s'):
            image_name = time.strftime("%Y%m%d-%H%M%S") + '.png'
            cv2.imwrite(image_name, mat)
        elif k == ord('n'):
            page += 1
            cv2.destroyAllWindows()
            print('Next to page : {}'.format(page))
        elif k == ord('q'):
            break

cap.release()
