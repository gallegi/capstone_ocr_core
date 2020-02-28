import glob
import io
import json
import os

from google.cloud import vision
from google.cloud.vision import types, enums
from tqdm import tqdm

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "HERAI-94e855c052e7.json"

image_names = glob.glob('/home/linhnq3/Disk2T/khanhtd2/utop/processed/*')
features = [
    types.Feature(type=enums.Feature.Type.DOCUMENT_TEXT_DETECTION),

]


def detect_text(paths):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()
    requests = []
    for path in paths:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        request = types.AnnotateImageRequest(image=image, features=features)
        requests.append(request)

    response = client.batch_annotate_images(requests=requests)

    data = {}

    for i, res in enumerate(response.responses):
        image_name = paths[i].split(os.sep)[-1]
        data[image_name] = {}
        full_text = res.full_text_annotation.text
        annotations = []
        for annotation in res.text_annotations:
            text = annotation.description
            points = []
            for point in response.responses[1].text_annotations[3].bounding_poly.vertices:
                point = [point.x, point.y]
            points.append(point)
            annotations.append({'text': text, 'points': points})

        data[image_name]['full text'] = full_text
        data[image_name]['annotations'] = annotations

    return data


def crawl():
    batch_size = 16
    for i in tqdm(range(0, len(image_names), batch_size)):
        data = detect_text(image_names[i:i + batch_size])
        with open('data/google_api_response/image {} - {}.json'.format(i, i + batch_size), 'w') as f:
            json.dump(data, f)


crawl()
