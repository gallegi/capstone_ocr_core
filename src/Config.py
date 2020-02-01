import string

data_dir = 'data'
alphabet = sorted(list(set(
    string.digits.lower() + string.ascii_letters.lower() + '' + '-ọụạảãàáâậầấẩẫăắằặẳẵóòõỏôộổỗồốơờớợởỡéèẻẽêếềệểễúùủũưựữửừứíìịỉĩýỳỷỵỹđ:;,.')))
# alphabet = string.digits + string.ascii_lowercase
# alphabet += open('data/japanese_alphabet.txt',encoding='utf-8').read()
# alphabet = list(set(alphabet))
# alphabet.sort()
alphabet = ''.join(alphabet)

word_gen_model_path = data_dir + '/markov_wordgen.json'
text_gen_model_path = data_dir + '/markov_textgen.json'
