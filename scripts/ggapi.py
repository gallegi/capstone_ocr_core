import glob
import io
import os

from google.cloud import vision
from tqdm import tqdm

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "HERAI-94e855c052e7.json"

image_names = glob.glob('test images/*')


def detect_text(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def crawl():
    url = 'https://demo.ocr.clova.ai/api/api/request'

    for image_path in tqdm(image_names):
        detect_text(image_path)


crawl()
