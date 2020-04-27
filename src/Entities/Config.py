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
        self.recognizer_weights_path ='weights/vi_recognizer_v2.h5'

        # doc_clf model and data path
        self.doc_clf_data_source_path = "data_source/document_clf_db.csv"
        self.doc_clf_model = "weights/doc_clf_model.pkl"
        self.doc_clf_ft_ext = "weights/doc_clf_ft_ext.pkl"

        # ner data source path
        self.ner_province_district_path = 'data_source/ProvinceDistrict.xls'
        self.ner_cqhc_path = 'data_source/CQHC.xls'

