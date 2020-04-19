import Config
from fonts import read_all_fonts

fonts = read_all_fonts()
open(Config.FONT_PATH + '/fontlist.txt', 'w').write('\n'.join(fonts).replace('\\', '/').replace('data/fonts/', ''))
