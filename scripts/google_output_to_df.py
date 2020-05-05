import pandas as pd
import json
import glob

from tqdm import tqdm

json_paths = glob.glob(r'C:\Users\Binh Bum\Downloads\Photos\test_label\output/*')

image_names = []
points = []
words= []
for json_path in tqdm(json_paths):
    text = open(json_path, encoding='utf-8').read()
    data = json.loads(text)
    for image in data['responses']:
        for annotation in image['textAnnotations'][:1]:
            image_names.append(image['context']['uri'].split('/')[-1])
            word = annotation['description']
            words.append(word)
            z = pd.DataFrame(annotation['boundingPoly']['vertices'])
            z = z.values
            center = z.mean(axis=0)
            z = z.flatten()
            points.append(list(z)+list(center))


df = pd.DataFrame(columns=['x1','y1','x2','y2','x3','y3','x4','y4','x_mean','y_mean'],data=points)
df['image_name'] = image_names
df['word'] = words
df.to_json(r'C:\Users\Binh Bum\Downloads\Photos\test_label/google_output.json')