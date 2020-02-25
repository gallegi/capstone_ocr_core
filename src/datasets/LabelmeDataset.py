import glob
import json
import os

import numpy as np

from datasets.AbtractDataset import Dataset
from datasets.Label import Label


class LabelmeDataset(Dataset):

    def _read_labels(self, source_path):
        json_paths = glob.glob(source_path + '/*.json')
        labels = []
        for json_path in json_paths:
            json_path = os.path.normpath(json_path)
            json_path_parts = json_path.split(os.sep)
            json_path_parts[-2] = 'images'
            json_path_parts[-1] = json_path_parts[-1].replace('json', 'jpg')
            image_path = os.sep.join(json_path_parts)

            image_name = image_path.split(os.sep)[-1]

            data = json.load(open(json_path, encoding='utf-8'))
            for shape in data['shapes']:
                text = shape['label']
                xmin, ymin, xmax, ymax = tuple(map(int, shape['points'][0] + shape['points'][1]))
                _label = Label(image=image_path,
                               boxs=np.array([[xmin, ymin], [xmin, ymax], [xmax, ymin], [xmax, ymax]]), word=text)
                labels.append((_label.image, _label.boxs, _label.word))
        return labels

    def __init__(self, path, name='Labelme dataset'):
        source_path = path
        self.name = name
        self.labels = self._read_labels(source_path)

    def _build_labels(self):
        pass
