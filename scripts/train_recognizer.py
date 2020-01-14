import datetime
import glob
import math
import os
import sys

sys.path.append('src')
import Config
import tqdm
import tensorflow as tf
import sklearn.model_selection

import data_generation
# import detection
import recognition
from Config import data_dir

assert tf.test.is_gpu_available(), 'No GPU is available.'
import imgaug
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

alphabet = ''.join(Config.alphabet)
recognizer_alphabet = ''.join(sorted(set(alphabet.lower())))
augmenter = imgaug.augmenters.Sequential([
    imgaug.augmenters.Multiply((0.9, 1.1)),
    imgaug.augmenters.GammaContrast(gamma=(0.5, 3.0)),
    imgaug.augmenters.Invert(0.25, per_channel=0.5)
])

fonts = [
    filepath for filepath in tqdm.tqdm(glob.glob(data_dir + '/fonts/**/*.ttf'))
    if (
            (not any(keyword in filepath.lower() for keyword in ['thin', 'light'])) and
            data_generation.font_supports_alphabet(filepath=filepath, alphabet=alphabet)
    )
]

backgrounds = glob.glob(data_dir + '/backgrounds/*.jpg')

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
        margin=50,
        rotationX=(-0.05, 0.05),
        rotationY=(-0.05, 0.05),
        rotationZ=(-15, 15), augmenter=augmenter
    ) for current_fonts, current_backgrounds in zip(
        font_splits,
        background_splits
    )
]

recognizer = recognition.Recognizer(
    width=200,
    height=31,
    stn=True,
    alphabet=recognizer_alphabet,
    weights='kurapan',
    optimizer='adam',
    include_top=False
)
# for layer in recognizer.backbone.layers:
#     layer.trainable = False

detector_batch_size = 1
detector_basepath = os.path.join('weights', f'detector_{datetime.datetime.now().isoformat()}')
max_length = 10

recognition_image_generators = [
    data_generation.convert_image_generator_to_recognizer_input(
        image_generator=image_generator,
        max_string_length=min(recognizer.training_model.input_shape[1][1], max_length),
        target_width=recognizer.model.input_shape[2],
        target_height=recognizer.model.input_shape[1],
        margin=1
    ) for image_generator in image_generators
]

# image, text = next(recognition_image_generators[1])
# print('This image contains:', text)
# plt.imshow(image)
# plt.show()

recognition_batch_size = 8
recognizer_basepath = os.path.join('weights', f'recognizer')
recognition_train_generator, recognition_val_generator, recogntion_test_generator = [
    recognizer.get_batch_generator(
        image_generator=image_generator,
        batch_size=recognition_batch_size,
        lowercase=True
    ) for image_generator in recognition_image_generators
]

try:
    recognizer.training_model.load_weights('weights/recognizer.h5')
    print('weights loaded')
except:
    print("Can't find or load weights")

recognizer.training_model.fit_generator(
    generator=recognition_train_generator,
    epochs=1000,
    steps_per_epoch=1000,
    callbacks=[
        # tf.keras.callbacks.EarlyStopping(restore_best_weights=True, patience=25),
        tf.keras.callbacks.ModelCheckpoint(filepath=f'{recognizer_basepath}.h5')
    ],
)

# image, text, lines = next(image_generators[0])
# boxes = detector.detect(images=[image])[0]
# drawn = detection.drawBoxes(image=image, boxes=boxes)
# predictions = recognizer.recognize_from_boxes(boxes=boxes, image=image)
# print(text, [text for text, box in predictions])
# plt.imshow(drawn)
# plt.show()
