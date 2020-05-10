Branch for Code AI model only


## GUIDE :
### Installation :

```batch
git clone https://gitlab.com/maycuatroi/ocrcore
cd ocrcore
pip install -r requirements.txt
```
1. weight link : https://drive.google.com/file/d/13OtK29OBfE62hUmaj2MIJu9UKDKx-fyz/view?usp=sharing
2. data_source link (data_source.zip): https://drive.google.com/drive/u/0/folders/1zjDt3NIKKsnwOg35leSUcOeBLj-3F0Lq
### Predict :

đặt ảnh vào folder ./test images

run :
```shell script
python scripts/predict.py
```

### Train with generated data :

##### build dataset :

Khi clone mới về chạy 1 lần để khởi tạo data set
```
python scripts/downlaod_data.py
python scripts/build_text_model.py
```

Chạy để training với data tự gen
```shell script
python scripts/train_recognizer.py
```

### Train with labeled data : 
 Download data from : [Link](https://drive.google.com/file/d/1EmrtGBgUPODSPg3UVd_zJLNIydkS9P45/view?usp=sharing)

Giải nén vào folder ./data -> ./data/data_cmnd/*

run scripts : 

``
python scripts/training recognizer with real data.py
``

## Current results :
