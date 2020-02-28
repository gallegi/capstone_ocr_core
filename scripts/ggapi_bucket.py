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
    types.Feature(type=enums.Feature.Type.TEXT_DETECTION),
]


def detect_text(paths,batch):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()
    requests = []
    for path in paths:
        image_name = path.split(os.sep)[-1]
        source = {"image_uri": 'gs://ocr_bill_utop/processed/{}'.format(image_name)}
        image = {"source": source}
        request = types.AnnotateImageRequest(image=image, features=features)
        requests.append(request)
    gcs_destination = {"uri": 'gs://ocr_bill_utop/output/batch_{}'.format(batch)}
    output_config = {"gcs_destination": gcs_destination, "batch_size": 16}
    r = client.async_batch_annotate_images(requests, output_config)
    print(r)

def crawl():
    batch_size = 16

    count = 0
    for i in tqdm(range(0, len(image_names), batch_size)):
        count+=1
        detect_text(image_names[i:i + batch_size],count)


crawl()
