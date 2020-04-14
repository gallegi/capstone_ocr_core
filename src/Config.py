import glob
import string

data_dir = 'data'
alphabet =[]
alphabet += sorted(list(set(string.digits.lower() + string.ascii_letters.lower() + '' + '-ọụạảãàáâậầấẩẫăắằặẳẵóòõỏôộổỗồốơờớợởỡéèẻẽêếềệểễúùủũưựữửừứíìịỉĩýỳỷỵỹđ:;,.')))
alphabet += string.digits + string.ascii_lowercase
alphabet +=  '[],.)(?!/'
alphabet = list(set(alphabet))
alphabet = sorted(alphabet)
alphabet = ''.join(alphabet)
print('Prepared alphabet : {}'.format(alphabet))
count = 0
word_gen_model_path = data_dir + '/markov_wordgen.json'
text_gen_model_path = data_dir + '/markov_textgen.json'
FONT_PATH = data_dir + '/fonts/'

backgrounds = glob.glob(data_dir + '/backgrounds/*.jpg')+ glob.glob('/home/linhnq3/Disk2T/data/synthtext/bg_img/*')
