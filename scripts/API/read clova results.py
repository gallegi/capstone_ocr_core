import glob
import json
import os

import editdistance
import pandas as pd

json_paths = glob.glob(r'data\test_results/*.json')

label_source = r'C:\Users\Nguyen Anh Binh\Downloads\labels\labels/'

df = pd.read_csv(r"scripts/API/evaluate_techchain_google.csv")

df['Clova'] = ''

for path in json_paths:
    data = json.loads(open(path, encoding='utf-8').read())
    responses = data['words']
    texts = []

    for response in responses:
        text = response['text']
        texts.append(text)
    text = ' '.join(texts)

    label_name = path.split(os.sep)[-1].split('.')[0]
    label_path = label_source + label_name + '.txt'
    label = open(label_path, encoding='utf-8').read()
    accuracy = 1 - editdistance.eval(label, text) / max(len(text), len(label))
    df['Clova'].loc[df['Image'] == label_name] = accuracy

print(df)
# df.to_csv('evaluate_google_techchain_clova.csv', index=False)
