import glob
import pandas as pd
from tqdm import tqdm

file_paths = glob.glob('data/labels/*')
large_text = ''
for file_path in tqdm(file_paths):
    text = open(file_path, encoding='utf-8').read()
    large_text += text

words = large_text.split()

data = {'word': [], 'count': []}
words_set = list(set(words))

for word in tqdm(words_set):
    data['word'].append(word)
    data['count'].append(words.count(word))


df = pd.DataFrame(data)

df.to_excel('words_distribution.xlsx')
