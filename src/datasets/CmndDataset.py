import glob
import json
import os
import uuid

import cv2
import numpy as np
from tqdm import tqdm

import Config
from datasets.AbtractDataset import Dataset
from datasets.Label import Label


class CmndDataset(Dataset):
    @staticmethod
    def build_dataset(source_path=Config.data_dir + '/data_cmnd/'):
        os.makedirs(source_path + '/croped', exist_ok=True)
        image_paths = glob.glob(Config.data_dir + '/data_cmnd/images/*')
        data = []
        for image_path in tqdm(image_paths):
            image_path = os.path.normpath(image_path)
            image_path_parts = image_path.split(os.sep)
            image_path_parts[-2] = 'labels'
            original_mat = cv2.imread(image_path)
            image_path_parts[-1] = image_path_parts[-1].replace('.jpg', '.json')
            label_path = '/'.join(image_path_parts)
            label = json.load(open(label_path, encoding='utf-8'))
            for shape in label['shapes']:
                text = shape['label']
                if 'word_' in text:
                    text = text.replace('word_', '')
                else:
                    continue
                xmin, ymin, xmax, ymax = tuple(map(int, shape['points'][0] + shape['points'][1]))
                mat = original_mat[ymin:ymax, xmin:xmax]

                unique_filename = str(uuid.uuid4())

                cv2.imwrite(Config.data_dir + '/data_cmnd/croped/{}.jpg'.format(unique_filename), mat)
                _label = Label(image=image_path,
                               boxs=np.array([[xmin, ymin], [xmin, ymax], [xmax, ymin], [xmax, ymax]]), word=text)
                data.append((_label.image, _label.boxs, _label.word))
        json_string = json.dumps(data)
        f = open(source_path + '/label.json', 'w', encoding='utf-8').write(json_string)

    def _read_labels(self, source_path):
        json_paths = glob.glob(source_path + '/labels/*.json')
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
                if 'word_' in text:
                    text = text.replace('word_', '')
                else:
                    continue
                xmin, ymin, xmax, ymax = tuple(map(int, shape['points'][0] + shape['points'][1]))
                _label = Label(image=image_path,
                               boxs=np.array([[xmin, ymin], [xmin, ymax], [xmax, ymin], [xmax, ymax]]), word=text)
                labels.append((_label.image, _label.boxs, _label.word))
        return labels

    def __init__(self):
        source_path = Config.data_dir + '/data_cmnd/'
        # if not is_dataset_generated:
        #     print('Create dataset')
        #     CmndDataset.build_dataset()
        # self.labels = json.load(open(Config.data_dir+'/data_cmnd/label.json',encoding='utf-8'))
        self.labels = self._read_labels(source_path)
        # super().__init__()

    def _build_labels(self):
        pass


if __name__ == '__main__':
    t = CmndDataset()
    # CmndDataset.build_dataset()
