import os
import sys
import zipfile

sys.path.append('src')
import tools
from Config import data_dir

if not os.path.isdir(data_dir + '/fonts'):
    fonts_zip_path = tools.download_and_verify(
        url='https://storage.googleapis.com/keras-ocr/fonts.zip',
        sha256='d4d90c27a9bc4bf8fff1d2c0a00cfb174c7d5d10f60ed29d5f149ef04d45b700',
        cache_dir=data_dir
    )
    with zipfile.ZipFile(fonts_zip_path) as zfile:
        zfile.extractall(data_dir + '/fonts')

if not os.path.isdir(data_dir + '/backgrounds'):
    backgrounds_zip_path = tools.download_and_verify(
        url='https://storage.googleapis.com/keras-ocr/backgrounds.zip',
        sha256='f263ed0d55de303185cc0f93e9fcb0b13104d68ed71af7aaaa8e8c91389db471',
        cache_dir=data_dir
    )
    with zipfile.ZipFile(backgrounds_zip_path) as zfile:
        zfile.extractall(data_dir + '/backgrounds')
