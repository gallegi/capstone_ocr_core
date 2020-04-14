import glob
import os

import PIL
import tqdm
from PIL import ImageFont
from fontTools.ttLib import TTFont

import Config


def _font_supports_alphabet(filepath, alphabet):
    """Verify that a font contains a specific set of characters.

    Args:
        filepath: Path to fsontfile
        alphabet: A string of characters to check for.
    """
    font = TTFont(filepath)
    if not all(any(ord(c) in table.cmap.keys() for table in font['cmap'].tables) for c in alphabet):
        return False
    font = ImageFont.truetype(filepath)
    try:
        for character in alphabet:
            font.getsize(character)
    except:
        return False
    return True


def read_all_fonts(path=Config.FONT_PATH):
    if os.path.isfile(path+'/fontlist.txt'):
        print('Found fontlist.txt file, read font list from file')
        lines = open(path+'/fontlist.txt','r',encoding='utf-8').read().split('\n')
        return [Config.FONT_PATH + '/'+line for line in lines]

    fonts = [
        filepath for filepath in tqdm.tqdm(glob.glob(path + '/**/*.ttf', recursive=True))
        if (
                (not any(keyword in filepath.lower() for keyword in ['thin', 'light'])) and
                _font_supports_alphabet(filepath=filepath, alphabet=Config.alphabet)
        )
    ]
    print('Find {} valid fonts'.format(len(fonts)))

    return fonts


if __name__ == '__main__':
    fonts = read_all_fonts()
    print(fonts)
