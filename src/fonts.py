import PIL
import fontTools
import tqdm
from fontTools.ttLib import TTFont

import data_generation
import Config
import glob


def _font_supports_alphabet(filepath, alphabet):
    """Verify that a font contains a specific set of characters.

    Args:
        filepath: Path to fsontfile
        alphabet: A string of characters to check for.
    """
    font = TTFont(filepath)
    # font = fontTools.ttLib.TTFont(filepath)
    if not all(any(ord(c) in table.cmap.keys() for table in font['cmap'].tables) for c in alphabet):
        return False
    font = PIL.ImageFont.truetype(filepath)
    try:
        for character in alphabet:
            font.getsize(character)
    except:
        return False
    return True


def read_all_fonts(path=Config.FONT_PATH):
    fonts = [
        filepath for filepath in tqdm.tqdm(glob.glob(path + '/**/*.ttf', recursive=True))
        if (
                (not any(keyword in filepath.lower() for keyword in ['thin', 'light'])) and
                _font_supports_alphabet(filepath=filepath, alphabet=Config.alphabet)
        )
    ]
    print('Find {} valid fonts'.format(len(fonts)))

    return fonts