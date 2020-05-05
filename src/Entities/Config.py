import string
import os

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
        self.recognizer_weights_path ='weights/bill_recognizer_LabelmeDataset.h5'

        # doc_clf model and data path
        self.doc_clf_data_source_path = "data_source/document_clf_db.csv"
        self.doc_clf_model = "weights/doc_clf_model.pkl"
        self.doc_clf_ft_ext = "weights/doc_clf_ft_ext.pkl"

        # ner data source path
        self.ner_province_district_path = 'data_source/ProvinceDistrict.xls'
        self.ner_cqhc_path = 'data_source/CQHC.xls'
        self.ner_engine_path = os.getcwd() + r'/weights/VnCoreNLP-1.1.1.jar'
        self.read_config()

    def read_config(self,config_path = 'weights/config.txt'):
        lines = open(config_path,encoding='utf-8').read().split('\n')
        data= {}
        for line in lines:
            z = line.split('=')
            if len(z)==2:
                data[z[0]]=z[1]
        self.port=  data['PORT']
        self.is_debug = int(data['DEBUG'])

if __name__ == '__main__':
    config = Config()
    dat = config.__dict__
    print()