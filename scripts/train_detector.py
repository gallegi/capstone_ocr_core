import glob
import math
import os
import sys

sys.path.append('src')

import Config

import tqdm
import matplotlib.pyplot as plt
import tensorflow as tf
import sklearn.model_selection

import data_generation
import detection
import recognition
from Config import data_dir
import fonts
import imgaug


assert tf.test.is_gpu_available(), 'No GPU is available.'

alphabet = ''.join(Config.alphabet)
recognizer_alphabet = ''.join(sorted(set(alphabet.lower())))
fonts = fonts.read_all_fonts()
backgrounds = glob.glob(data_dir + '/backgrounds/*.jpg')
augmenter = imgaug.augmenters.Sequential([
    imgaug.augmenters.Multiply((0.9, 1.1)),
    imgaug.augmenters.GammaContrast(gamma=(0.5, 3.0)),
    imgaug.augmenters.Invert(0.25, per_channel=0.5)
])

text_generator = data_generation.get_text_generator(alphabet=alphabet)
print('The first generated text is:', next(text_generator))


def get_train_val_test_split(arr):
    train, valtest = sklearn.model_selection.train_test_split(arr, train_size=0.8, random_state=42)
    val, test = sklearn.model_selection.train_test_split(valtest, train_size=0.5, random_state=42)
    return train, val, test


background_splits = get_train_val_test_split(backgrounds)
font_splits = get_train_val_test_split(fonts)

image_generators = [
    data_generation.get_image_generator(
        height=640,
        width=640,
        text_generator=text_generator,
        font_groups={
            alphabet: current_fonts
        },
        backgrounds=current_backgrounds,
        font_size=(60, 120),
        margin=50,augmenter=augmenter,
        rotationX=(-0.05, 0.05),
        rotationY=(-0.05, 0.05),
        rotationZ=(-15, 15)
    ) for current_fonts, current_backgrounds in zip(
        font_splits,
        background_splits
    )
]

# See what the first validation image looks like.
image, lines = next(image_generators[1])
text = data_generation.convert_lines_to_paragraph(lines)
print('The first generated validation image (below) contains:', text)
plt.imshow(image)

detector = detection.Detector(weights='clovaai_general')
# detector.model.summary()
recognizer = recognition.Recognizer(
    width=200,
    height=31,
    stn=True,
    alphabet=recognizer_alphabet,
    weights='kurapan',
    optimizer='RMSprop',
    include_top=False
)
for layer in recognizer.backbone.layers:
    layer.trainable = False

detector_batch_size = 1
detector_basepath = os.path.join('weights', f'detector')
detection_train_generator, detection_val_generator, detection_test_generator = [
    detector.get_batch_generator(
        image_generator=image_generator,
        batch_size=detector_batch_size
    ) for image_generator in image_generators
]
detector.model.fit_generator(
    generator=detection_train_generator,
    steps_per_epoch=math.ceil(len(background_splits[0]) / detector_batch_size),
    epochs=1000,
    workers=0,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(restore_best_weights=True, patience=5),
        # tf.keras.callbacks.CSVLogger(f'{detector_basepath}.csv'),
        tf.keras.callbacks.ModelCheckpoint(filepath=f'{detector_basepath}.h5', monitor='acc', save_best_only=True,
                                           save_weights_only=True)
    ],
    validation_data=detection_val_generator,
    validation_steps=math.ceil(len(background_splits[1]) / detector_batch_size)
)
