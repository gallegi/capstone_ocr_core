import os
import io
import pandas as pd
import glob
import pickle
import json
import pyodbc

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

import sys
sys.path.append('src')
from Entities.Config import Config

class DocumentClassifier:
    def __init__(self, config):
        self.model_path = config.doc_clf_model
        self.feature_extractor_path = config.doc_clf_ft_ext
        # self.data_source_path = config.doc_clf_data_source_path
        # self.data_source_path_original = config.doc_clf_data_source_path_original
        self.connection_string = config.doc_clf_connection_string

        # form id is not the direct label to train -> need a mapping
        conn = self.__get_connection_string__()
        self.label_to_form_id = pd.read_sql('select FormID form_id from FormTemplate', conn)['form_id']
        print('Type of form id first read', type(self.label_to_form_id))
        conn.close()

        if(self.model_path is not None):
            if(not os.path.exists(self.model_path)):
                self.model = KNeighborsClassifier(n_neighbors=1)
            else:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
        else:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)

        print(self.feature_extractor_path)
        if(self.feature_extractor_path is not None):   
            if(not os.path.exists(self.feature_extractor_path)):   
                self.vec = TfidfVectorizer()
            else:
                with open(self.feature_extractor_path, 'rb') as f:
                    self.vec = pickle.load(f)
        else:
            with open(self.feature_extractor_path, 'rb') as f:
                self.vec = pickle.load(f)

    def __get_connection_string__(self):
        '''Return a connection string to sql server'''
        return pyodbc.connect(self.connection_string)

    def save_models(self):
        '''Write model to specified paths'''
        print('Save document classifier model to:', self.model_path)
        with open(self.model_path, 'wb') as f: 
            pickle.dump(self.model, f)

        # with open(self.feature_extractor_path, 'wb') as f: 
        #     pickle.dump(self.vec, f)
    
    def __update_datasource__(self, form_id, raw_text, action):
        conn = self.__get_connection_string__()
        df = pd.read_sql('select FormID form_id, APIOutput text from FormTemplate', conn)
        msg = ""


        df.to_csv(self.data_source_path, index=False)
        print('Update document classification data source')

        return df, msg

    def train(self, request_data):
        '''Train model when data source is updated with request_data
            Args:
                - request_data: raw_text send from clients to insert or update data source'''
        action = request_data['action']
        print('Request retraining with action:', action)

        conn = self.__get_connection_string__()
        templates = pd.read_sql('select FormID form_id, APIOutput text from FormTemplate', conn)
        conn.close()

        # update mapping from label to form id
        self.label_to_form_id = templates['form_id']
        # print(self.label_to_form_id)

        # retrain model
        if(templates.empty):
            print('Data source is empty. No retrain')
        else:
            template_X = self.vec.transform(templates['text'])
            template_y = templates.index.values # form id maybe not mono_increasing -> use index as label
            self.model.fit(template_X, template_y)
            print('Done retraining document classification model')
            
        return "Perfrom retraining with total number of forms:"+str(len(templates))

    # def train_original_data(self):
    #     '''Train model with original data source'''
    #     templates = pd.read_csv(self.data_source_path_original)
    #     # retrain model
    #     template_X = self.vec.transform(templates['text'])
    #     template_y = templates.index.values # form id maybe not mono_increasing -> use index as label
    #     self.model.fit(template_X, template_y)
    #     print('Done retraining document classification model')


    def predict(self, raw_text):
        '''Return form_id with raw_text'''
        features = self.vec.transform([raw_text])
        ind = self.model.predict(features)[0]
        print(ind)
        return self.label_to_form_id.iloc[ind]

if __name__ == "__main__":
    text = 'Mẫu CC03 ban hành kèm theo Thông tư số 66/2015/TT-BCA ngày 15/12/2015 CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc GIẤY HẸN Trả thẻ Căn cước công dân Công an, qua đã tiếp nhận hồ sơ và làm thủ tục thẻ Căn cước công dân đối với công dân; Họ, chữ đệm và tên:.. Sinh ngày:............ Giới tính:.. Nơi thường trú Thời gian hẹn trả thẻ Căn cước công dân đối với công dân vào. giờ.......phút, thử.. ngày..................... Tai dia chi.............................. ........... ........., ngày ... tháng... nha. .. NGƯỜI LẬP GIÁ HENT" (Ký, ghi rõ họ tên)'
    config = Config()
    doc = DocumentClassifier(config)
    doc.train({'action':'none'})
    print(doc.predict(text))