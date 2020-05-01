import numpy as np
import pandas as pd
import re
import pickle
import matplotlib.pyplot as plt
import time

import sys

sys.path.append('src')
from vncorenlp import VnCoreNLP
import logging
import numpy as np
import pandas as pd


class EntityRecognizer():
    def __init__(self, config):
        province_district = pd.read_excel(config.ner_province_district_path)
        cqhc = pd.read_excel(config.ner_cqhc_path)
        self.ref_district = province_district['Quận Huyện'].drop_duplicates()
        self.ref_province = province_district['Tỉnh Thành Phố'].drop_duplicates()
        self.ref_province = self.ref_province.str.replace('Tỉnh', '').str.replace('Thành phố', '').str.strip()
        self.ref_cqhc = cqhc.PublicAdministrationName.drop_duplicates()

        logging.basicConfig(level=logging.DEBUG)
        self.ner_annotator = VnCoreNLP(config.ner_engine_path)

    def __ner_lookup__(self, text, data_source):
        matched = data_source.str.lower().map(lambda x: x in text.lower())
        return data_source[matched].tolist()

    def ner_province(self, text):
        return self.__ner_lookup__(text, self.ref_province)

    def ner_district(self, text):
        return self.__ner_lookup__(text, self.ref_district)

    def ner_cqhc(self, text):
        return self.__ner_lookup__(text, self.ref_cqhc)

    def ner_person_names(self, text):
        text= text.replace('\n',' . ')
        annotated_text = self.ner_annotator.annotate(text)
        sentences = []
        for sentence in  [x for x in annotated_text['sentences']]:
            sentences +=sentence

        annotated_text = pd.DataFrame(sentences)
        names = list(annotated_text[annotated_text['nerLabel'] == 'B-PER']['form'].str.replace('_', ' '))
        ignore_chars = ['j', 'z']
        for name in names:
            for ignore_char in ignore_chars:
                if ignore_char in name.lower():
                    names.remove(name)

        return names

    def ner_tthc():
        # TODO: implement ner tthc
        pass


if __name__ == "__main__":
    ent = EntityRecognizer(Config())
    text = 'SỞ CÔNG THƯƠNG GIA LAI\n\nCỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM\n\nĐộc lập - Tự do - Hạnh phúc\n\n\n\nPHIẾU HẸN\n\nTRẢ KẾT QUẢ  KÊ KHAI LẠI GIÁ THUỐC SẢN XUẤT TẠI VIỆT NAM ĐỐI VỚI CƠ SỞ CÓ TRỤ SỞ SẢN XUẤT THUỐC ĐÓNG TRÊN ĐỊA BÀN THÀNH PHỐ\n\n(HS ĐKT mới đối với NNT là tổ chức KD (trừ các ĐV trực thuộc )\n\n\n\nTên đơn vị: Công ti TNHH ABZ\n\nMã số thuế: 197484244\n\nĐịa chỉ: P.2002, N2, CT 1.1, Chung cư ngõ 183 Hoàng Văn Thái, phường Khương Trung, quận Thanh Xuân, Hà Nội\n\nSố hồ sơ nhận: Gr81zcvJ3P\n\n\n\nCơ quan thuế đã nhận hồ sơ thuế của đơn vị gồm:\n\nSổ photo hộ khẩu\n\nCơ quan thuế sẽ trả kết quả giải quyết hồ sơ vào:  ngày 10 tháng 2 năm 2039\n\nHình thức trả kết quả:\n\n- Trực tiếp tại cơ quan thuế\n\nKhi đến nhận kết quả để nghỉ người đến nhận mang theo giấy hẹn này và giấy giới thiệu hoặc chứng minh thư nhân dân của người nhận. Nếu có vướng mắc, để nghỉ liên hệ đến :\n\n               - Số điện thoại: 914903685\n\n               - Địa chỉ: Số nhà 15, Tổ 2, khu 6B, phường Hồng Hải, thành phố Hạ Long, Quảng Ninh\n\nLâm Đồng, ngày 1 tháng 10\n\nCÁN BỘ VIẾT PHIẾU HẸN\n\n(Ký, ghi rõ họ tên)\n\nĐoàn Bửu Chưởng'
    print(ent.ner_district(text))
    print(ent.ner_province(text))
    print(ent.ner_cqhc(text))
