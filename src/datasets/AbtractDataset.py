import itertools
from abc import abstractmethod
from random import shuffle

import numpy as np

import tools


class Dataset:
    # Abtract class for Dataset object
    def __init__(self):
        self.labels = self._build_labels()
        self.name = 'abtract'

    def build_recognize_generator(self, width, height, augmenter=None, area_threshold=0.5):
        """Generated augmented (image, lines) tuples from a list
        of (filepath, lines, confidence) tuples. Confidence using for semi supervised data, not implemented.
        Args:s
            augmenter: An augmenter to apply to the images.
            width: The width to use for output images
            height: The height to use for output images
            area_threshold: The area threshold to use to keep
                characters in augmented images.
        """
        labels = self.labels.copy()
        for index in itertools.cycle(range(len(labels))):
            if index == 0:
                shuffle(labels)
            image_filepath, lines, _ = labels[index]
            image = tools.read(image_filepath)
            if augmenter is not None:
                image, lines = tools.augment(boxes=lines,
                                             boxes_format='lines',
                                             image=image,
                                             area_threshold=area_threshold,
                                             augmenter=augmenter)
            image, scale = tools.fit(image,
                                     width=width,
                                     height=height,
                                     mode='letterbox',
                                     return_scale=True)
            lines = tools.adjust_boxes(boxes=lines, boxes_format='lines', scale=scale)
            yield image, lines

    def get_recognizer_image_generator(self, height, width, alphabet, augmenter=None):
        """Generate augmented (image, text) tuples from a list
        of (filepath, box, label) list label objects.
        Args:
            height: The height of the images to return
            width: The width of the images to return
            alphabet: The alphabet which limits the characters returned
            augmenter: The augmenter to apply to images
        """
        error_chars = ''
        for _image_name, _box, text in self.labels:
            for c in text:
                if c not in alphabet:
                    error_chars += c
        error_chars = ''.join(list(set(error_chars)))
        print('Error line characters : {}'.format(error_chars))
        n_with_illegal_characters = sum(any(c not in alphabet for c in text) for _, _, text in self.labels)
        if n_with_illegal_characters > 0:
            print(f'{n_with_illegal_characters} / {len(self.labels)} instances have illegal characters.')
        labels = self.labels.copy()
        for index in itertools.cycle(range(len(labels))):
            if index == 0:
                shuffle(labels)
            filepath, box, text = labels[index]
            cval = np.random.randint(low=0, high=255, size=3).astype('uint8')
            if box is not None:
                try:
                    image = tools.warpBox(image=tools.read(filepath),
                                          box=box.astype('float32'),
                                          target_height=height,
                                          target_width=width,
                                          cval=cval)
                except:
                    continue
            else:
                image = tools.read_and_fit(filepath_or_array=filepath,
                                           width=width,
                                           height=height,
                                           cval=cval)
            text = ''.join([c for c in text if c in alphabet])
            if not text:
                continue
            if augmenter:
                image = augmenter.augment_image(image)
            yield (image, text)

    @abstractmethod
    def _build_labels(self):
        pass
