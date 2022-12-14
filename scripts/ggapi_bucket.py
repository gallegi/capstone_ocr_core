import glob
import os

from google.cloud import vision
from google.cloud.vision import types, enums
from tqdm import tqdm

# bucket download command
# gsutil -m cp -R gs://vnpost/output .



bucket_name = 'vnpost'
source_folder = r'C:\Users\Binh Bum\Downloads\Photos\batch_2/'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Binh Bum\OneDrive\AWS keys\HERAI-b35db0453388.json"
image_names = glob.glob(source_folder + '/*.jpg')
features = [
    types.Feature(type=enums.Feature.Type.DOCUMENT_TEXT_DETECTION),
    types.Feature(type=enums.Feature.Type.TEXT_DETECTION),
]


def detect_text(paths, batch):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()
    requests = []
    for path in paths:
        image_name = path.split(os.sep)[-1]
        source = {"image_uri": 'gs://{}/with_marker/{}'.format(bucket_name, image_name)}
        image = {"source": source}
        request = types.AnnotateImageRequest(image=image, features=features)
        requests.append(request)
    gcs_destination = {"uri": 'gs://{}/output/batch_{}'.format(bucket_name, batch)}
    output_config = {"gcs_destination": gcs_destination, "batch_size": 16}
    r = client.async_batch_annotate_images(requests, output_config)
    # print(r)


def crawl():
    batch_size = 16
    count = 0
    for i in tqdm(range(0, len(image_names), batch_size)):
        count += 1
        detect_text(image_names[i:i + batch_size], count)


crawl()
