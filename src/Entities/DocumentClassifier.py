import os
import io
import pandas as pd
import glob
import pickle

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
        self.data_source_path = config.doc_clf_data_source_path
        self.data_source_path_original = config.doc_clf_data_source_path_original

        # form id is not the direct label to train -> need a mapping
        self.label_to_form_id = pd.read_csv(self.data_source_path, usecols=['form_id'])

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
    
    def save_models(self):
        '''Write model to specified paths'''
        print('Save document classifier model to:', self.model_path)
        with open(self.model_path, 'wb') as f: 
            pickle.dump(self.model, f)

        # with open(self.feature_extractor_path, 'wb') as f: 
        #     pickle.dump(self.vec, f)
    
    def __update_datasource__(self, form_id, raw_text, action):
        df = pd.read_csv(self.data_source_path)
        msg = ""
        if(action == 'add'):
            if(form_id in df['form_id'].tolist()):
                msg = 'Warning: FormID %d already exists. Replace with new text'%(form_id)
                print(msg)
                # update data source
                df.loc[df['form_id'] == form_id, 'text'] = raw_text
            else:
                # insert into data source
                msg = 'Add new FormID %d into data source'%(form_id)
                print(msg)
                df = df.append(pd.DataFrame({'text':[raw_text], 'form_id': [form_id]}))
        elif(action == 'update'):
            if(form_id in df['form_id'].tolist()):
                msg = 'Update FormID %d with new text'%(form_id)
                print(msg)
                # update data source
                df.loc[df['form_id'] == form_id, 'text'] = raw_text
            else:
                # insert into data source
                msg = 'Warning: FormID %d does not exist. Add new FormID %d into data source'%(form_id, form_id)
                print(msg)
                df = df.append(pd.DataFrame({'text':[raw_text], 'form_id': [form_id]}))
        elif(action == 'delete'):
            if(form_id in df['form_id'].tolist()):
                # delete from data source
                msg = 'Delete FormID %d from data source'%(form_id)
                print(msg)
                df = df[df['form_id'] != form_id]
            else:
                msg = 'Warning FormID %d does not exists. No action is taken'%(form_id)
                print(msg)
        elif(action == 'delete_all'):
            msg = 'Delete all data source'
            print(msg)
            df = df.iloc[0:0]
        elif(action == 'train_original'):
            msg = 'Train with default orginal data'
            print(msg)
            df = pd.read_csv(self.data_source_path_original)
        else:
            msg = 'Action is not valid. Please provide 1 of these actions: add, update, delete, delete_all, train_original'
            print(msg)

        df.to_csv(self.data_source_path, index=False)
        print('Update document classification data source')

        return df, msg

    def train(self, request_data):
        '''Train model when data source is updated with request_data
            Args:
                - request_data: raw_text send from clients to insert or update data source'''
        action = request_data['action']
        form_id = request_data['ft']['FormID']
        raw_text = request_data['ft']['APIOutput']['raw_text']

        # update data source
        templates, msg = self.__update_datasource__(form_id, raw_text, action)

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
            
        return msg

    def train_original_data(self):
        '''Train model with original data source'''
        templates = pd.read_csv(self.data_source_path)
        # retrain model
        template_X = self.vec.transform(templates['text'])
        template_y = templates.index.values # form id maybe not mono_increasing -> use index as label
        self.model.fit(template_X, template_y)
        print('Done retraining document classification model')


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
    doc.train_original_data()
    print(doc.predict(text))