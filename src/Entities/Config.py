import string


class Config:
    def __init__(self):
        alphabet =[]
        alphabet += sorted(list(set(string.digits.lower() + string.ascii_letters.lower() + '' + '-ọụạảãàáâậầấẩẫăắằặẳẵóòõỏôộổỗồốơờớợởỡéèẻẽêếềệểễúùủũưựữửừứíìịỉĩýỳỷỵỹđ:;,.')))
        alphabet += string.digits + string.ascii_lowercase
        alphabet +=  '[],.)(?!/'
        alphabet = list(set(alphabet))
        alphabet = sorted(alphabet)
        alphabet = ''.join(alphabet)
        print('Prepared alphabet : {}'.format(alphabet))


        self.alphabet = alphabet
        self.recognizer_weights_path ='weights/vi_recognizer_v2_attention.h5'
