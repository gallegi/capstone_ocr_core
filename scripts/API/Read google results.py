import glob
import json

import editdistance
import pandas as pd

json_paths = glob.glob(r'D:\evaluate ocr\output/*.json')

label_source = r'C:\Users\Nguyen Anh Binh\Downloads\labels\labels/'

df = pd.read_csv(r"C:\Users\Nguyen Anh Binh\Downloads\scripts_API_evaluated.csv")

df['Google'] = ''

for path in json_paths:
    data = json.loads(open(path, encoding='utf-8').read())
    responses = data['responses']
    for response in responses:
        text = response['textAnnotations'][0]['description'].lower()
        label_name = response['context']['uri'].split('/')[-1].split('.')[0]
        label_path = label_source + label_name + '.txt'
        label = open(label_path, encoding='utf-8').read()
        accuracy = 1 - editdistance.eval(label, text) / max(len(text), len(label))
        df['Google'].loc[df['Image'] == label_name] = accuracy

# print(df)
df.to_csv('evaluate.csv', index=False)
