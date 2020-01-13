import string

data_dir='data'
alphabet = sorted(list(set(string.digits.lower() + string.ascii_letters.lower() + '' + '-ọụạảãàáâậầấẩẫăắằặẳẵóòõỏôộổỗồốơờớợởỡéèẻẽêếềệểễúùủũưựữửừứíìịỉĩýỳỷỵỹđ')))
word_gen_model_path = data_dir+'/markov_wordgen.json'
text_gen_model_path = data_dir+'/markov_textgen.json'