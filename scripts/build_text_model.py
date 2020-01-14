import glob
import os
import sys
sys.path.append('src')
from essential_generators import MarkovTextGenerator, MarkovWordGenerator
import tools
from Config import data_dir

if not os.path.isdir(data_dir + '/documents'):
    os.mkdir(data_dir + '/documents')

files = glob.glob(data_dir + '/documents/*')
if len(files) == 0:
    word_path = tools.download_and_verify(
        url='https://raw.githubusercontent.com/duyetdev/vietnamese-wordlist/master/Viet74K.txt',
        cache_dir=data_dir + '/documents'
    )

files = glob.glob(data_dir + '/documents/*')
print('Found : {} documents'.format(len(files)))

text = ''
for file in files:
    text += open(file, encoding='utf-8').read()


def make_text_training_data(output=data_dir + '/markov_textgen.json'):
    gen = MarkovTextGenerator(load_model=False)
    gen.train(text)
    gen.save_model(output)


def make_word_training_data(output=data_dir + '/markov_wordgen.json'):
    gen = MarkovWordGenerator(load_model=False)
    gen.train(text)
    gen.save_model(output)


make_text_training_data()
make_word_training_data()
