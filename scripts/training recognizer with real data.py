import sys
sys.path.append('./src')
import Config
from datasets.LabelmeDataset import LabelmeDataset
import imgaug
import matplotlib.pyplot as plt
import sklearn.model_selection
import tensorflow as tf
import recognition


model_name = 'vnpost_recognizer_LabelmeDataset'
dataset = LabelmeDataset(r'data/vnpost/vnpost_train/', name='vnpost')
train_labels = dataset.labels
train_labels = [(filepath, box, str(word)) for filepath, box, word in train_labels]
dataset.labels = train_labels
alphabet = ''.join(Config.alphabet)
recognizer_alphabet = ''.join(sorted(set(alphabet)))
recognizer = recognition.Recognizer(
    width=200,
    height=31,
    stn=True,
    alphabet=recognizer_alphabet,
    # weights=None,
    optimizer='adam',
    include_top=False,
    attention=True,
)
recognizer.training_model.summary()
try:
    recognizer.training_model.load_weights('weights/{}.h5'.format(model_name))
    print('weights loaded')
except:
    print("Can't find or load weights")

augmenter = imgaug.augmenters.Sequential([
    imgaug.augmenters.Multiply((0.9, 1.1)),
    imgaug.augmenters.GammaContrast(gamma=(0.5, 3.0)),
    imgaug.augmenters.Invert(0.25, per_channel=0.5)
])



batch_size = 8
train_labels, validation_labels = sklearn.model_selection.train_test_split(train_labels, test_size=0.2, random_state=42)
(training_image_gen, training_steps), (validation_image_gen, validation_steps) = [
    (
        dataset.get_recognizer_image_generator(
            height=recognizer.model.input_shape[1],
            width=recognizer.model.input_shape[2],
            alphabet=recognizer.alphabet,
            augmenter=augmenter
        ),
        len(labels) // batch_size
    ) for labels, augmenter in [(train_labels, augmenter), (validation_labels, None)]
]
training_gen, validation_gen = [
    recognizer.get_batch_generator(
        image_generator=image_generator,
        batch_size=batch_size
    )
    for image_generator in [training_image_gen, validation_image_gen]
]

# training_gen, validation_gen =  [
#     tf.data.Dataset.from_generator(
#         functools.partial(recognizer.get_batch_generator,
#                           image_generator=image_generator,
#                           batch_size=batch_size),
#         output_types=((tf.float32, tf.int64, tf.float64, tf.int64), tf.float64),
#         output_shapes=((tf.TensorShape([None, 31, 200, 1]), tf.TensorShape([None, recognizer.training_model.input_shape[1][1]]),
#                         tf.TensorShape([None,
#                                         1]), tf.TensorShape([None,
#                                                              1])), tf.TensorShape([None, 1])))
#     for image_generator in [training_image_gen, validation_image_gen]
# ]

for i in range(4):
    image, text = next(training_image_gen)
    plt.title(text)
    _ = plt.imshow(image)
    plt.show()

callbacks = [
    # LogImageCallback(validation_labels, recognizer),
    # tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=10, restore_best_weights=False),
    tf.keras.callbacks.ModelCheckpoint('weights/vnpost_recognizer_{}.h5'.format(type(dataset).__name__),
                                       monitor='val_acc',
                                       save_best_only=True),
]
training_steps = 2000
validation_steps = 100

recognizer.training_model.fit_generator(
    generator=training_gen,
    steps_per_epoch=training_steps,
    # steps_per_epoch=1000,
    # validation_steps=10,
    validation_steps=validation_steps,
    validation_data=validation_gen,
    callbacks=callbacks,
    epochs=100,
)

# for i in range(6):
#     image_filepath, box, actual = random.choice(validation_labels)
#     xmin, ymin, xmax, ymax = box[0][0], box[0][1], box[-1][0], box[-1][1]
#     predicted = recognizer.recognize(image_filepath)
#     print(f'Predicted: {predicted}, Actual: {actual}')
#     image = tools.read(image_filepath)
#     # image = detection.drawBoxes(image=image, boxes=[box])
#     plt.annotate(predicted, box[0])
#     _ = plt.imshow(image)
#     plt.show()
