import re
import pickle
import matplotlib.pyplot as plt
import time

import sys

sys.path.append('src')
from vncorenlp import VnCoreNLP
import logging
import pandas as pd
import unidecode

class EntityRecognizer():
    def __init__(self, config):
        province_district = pd.read_excel(config.ner_province_district_path)
        cqhc = pd.read_excel(config.ner_cqhc_path)

        self.ref_district = province_district['Quận Huyện'].drop_duplicates().dropna()
        self.ref_district_no_accent = self.ref_district.map(lambda x: unidecode.unidecode(x))

        self.ref_province = province_district['Tỉnh Thành Phố'].drop_duplicates().dropna()
        self.ref_province = self.ref_province.str.replace('Tỉnh', '').str.replace('Thành phố', '').str.strip()
        self.ref_province_no_accent = self.ref_province.map(lambda x: unidecode.unidecode(x))

        self.ref_cqhc = cqhc.PublicAdministrationName.str.lower()\
                                            .str.strip().drop_duplicates().reset_index(drop=True)
        self.ref_cqhc_no_accent = self.ref_cqhc.map(lambda x: unidecode.unidecode(x))

        self.patterns_profile = [re.compile('(?<=Noi dung yeu cau giai quyet)[\n ]*[^\n.]+', flags=re.IGNORECASE),
                         re.compile('(?<=THU TUC)[:\n ]*[^\n.]+', flags=re.IGNORECASE),
                         re.compile('(?<=Ten thu tuc tiep nhan:)[\n ]*[^\n.]+'),
                         re.compile('(?<=Ve viec)[:\n ]*[^\n.]+', flags=re.IGNORECASE),
                         re.compile('(?<=TRA KET QUA)[\n ]*[^\n.]+'),
                         re.compile('(?<=Giay tiep nhan)[\n ]*[^\n.]+'),
                         re.compile('(?<=GIAY BIEN NHAN)[\n ]*[^\n.]+'),
                         re.compile('(?<=BIEN BAN GIAO NHAN)[\n ]*[^\n.]+'),
                         re.compile('(?<=Tra ket qua giai quyet)[\n ]*[^\n.]+'),
                         re.compile('(?<=GIAY HEN)[\n ]*[^\n.]+'),
                         re.compile('(?<=PHIEU HEN\n).*'),
                         re.compile('(?<=Noi dung ho so)[\n ]*[^\n.]+'),
                         re.compile('(?<=Noi dung dang yeu cau giai quyet:)[\n ]*[^\n.]+'),
                         re.compile('(?<=Thu tuc tiep nhan:)[\n ]*[^\n.]+'),
                         re.compile('(?<=Loai ho so)[:\n ]*[^\n.]+')]
        
        self.patterns_alc = [re.compile('[A-Z]{3}[0-9]{9}'),
                        re.compile('(?<=So ho so nhan)[\n ]*:+[\n ]*[^\n. ]+'),
                       re.compile('(?<=So)[\n ]*:+[\n ]*[^\n. ]+'),
                       re.compile('(?<=Ma so ho so)[\n ]*:+[\n ]*[^\n. ]+'),
                       re.compile('(?<=Ma ho so)[\n ]*:+[\n ]*[^\n. ]+'),
                       re.compile('(?<=Ma so)[\n ]*:+[\n ]*[^\n. ]+')]

        self.patterns_address = [re.compile('(?<=Dia chi)[ ]*:+[ ]*[^\n.]+', flags=re.IGNORECASE),
                       re.compile('(?<=thuong tru tai)[ ]*:+[ ]*[^\n.]+', flags=re.IGNORECASE),
                       re.compile('(?<=tai)[ ]*:+[ ]*[^\n.]+', flags=re.IGNORECASE),
                       re.compile('(?<=co quan)[ ]*:+[ ]*[^\n.]+', flags=re.IGNORECASE),]

        self.patterns_phone_number = [re.compile('((09|03|07|08|05)+([0-9]{8}))')]

        self.patterns_ppc = [re.compile('0[0-9]{11}', flags=re.IGNORECASE)]

        logging.basicConfig(level=logging.DEBUG)
        self.ner_annotator = VnCoreNLP(config.ner_engine_path)

    def __ner_lookup__(self, text, data_source, data_source_no_accent):
        text_lower = unidecode.unidecode(text.lower())
        matched = data_source_no_accent.str.lower().map(lambda x: x in text_lower)
        return data_source[matched].tolist()

    def __ner_province__(self, text):
        return self.__ner_lookup__(text, self.ref_province, self.ref_province_no_accent)

    def __ner_district__(self, text):
        return self.__ner_lookup__(text, self.ref_district, self.ref_district_no_accent)

    def __ner_cqhc__(self, text):
        return self.__ner_lookup__(text, self.ref_cqhc, self.ref_cqhc_no_accent)

    def __search__(self, ptn, text, flag):
        o = re.search(ptn, text, flags=flag)
        if (o is None):
            return 0, 0
        return o.start(), o.end()

    def __preprocessing__(self, text):
        space_norm = re.sub('[\\t ]+', ' ', text)
        rm = re.sub('CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM[\\n ]*', '', space_norm)
        rm = re.sub('Độc lập — Tự do - Hạnh phúc[\\n ]*', '', rm)
        rm = rm.replace('—', '-')
        return rm

    def ner_province_district_cqhc(self, raw_text):
        text = self.__preprocessing__(raw_text)
        result_province = self.__ner_province__(text)
        result_district = self.__ner_district__(text)
        list_province = pd.DataFrame({'province': result_province, 'common': 1})
        list_district = pd.DataFrame({'district': result_district, 'common': 1})
        list_cqhc = pd.DataFrame({'cqhc': self.__ner_cqhc__(text), 'common': 1})
        temp = pd.merge(list_province, list_district, how='outer')
        temp = pd.merge(temp, list_cqhc, how='outer')
        temp = temp.fillna('None').astype(str)
        temp['cqhc1'] = (temp['cqhc'] + ' ' + temp['province']).map(lambda x: unidecode.unidecode(x))
        temp['cqhc2'] = (temp['cqhc'] + ' ' + temp['district']).map(lambda x: unidecode.unidecode(x))

        text_lower = unidecode.unidecode(text.lower())

        cqhc_province = temp['cqhc1'].map(lambda x: self.__search__(x, text_lower, re.IGNORECASE))
        cqhc_district = temp['cqhc2'].map(lambda x: self.__search__(x, text_lower, re.IGNORECASE))

        try:
            result_cqhc = pd.concat([cqhc_province, cqhc_district]).drop_duplicates().map(
                lambda x: text[x[0]:x[1]]).str.strip()
            result_cqhc = result_cqhc[result_cqhc != ''].drop_duplicates().tolist()

            if (len(result_cqhc) == 0):
                print(list_cqhc['cqhc'])
                print(list_cqhc['cqhc'].drop_duplicates())
                return result_province, result_district, list_cqhc['cqhc'].drop_duplicates().tolist()
        except Exception as ex:
            return result_province, result_district, list_cqhc['cqhc'].drop_duplicates().tolist()

        return result_province, result_district, result_cqhc

    def __ner_pattern__(self, raw_text, patterns, is_noise_funct=None):
        text = raw_text.replace('\xa0', ' ')
        text = self.__preprocessing__(text)
        text_no_accent = unidecode.unidecode(text)
        res = []
        for ptn in patterns:
            match_ptn = ptn.finditer(text_no_accent)
            if (match_ptn is None):
                continue
            for m in match_ptn:
                extracted = m.group()
                s = m.start()
                e = m.end()

                if (is_noise_funct is not None):
                    if (is_noise_funct(extracted)):
                        continue

                res.append(re.sub('[.\n:]', ' ', text[s:e]).strip())
        return pd.Series(res).drop_duplicates().tolist()

    def __count_words__(self, token, extracted):
        return len(list(filter(lambda x: x != '', re.split(token, extracted))))

    def __is_noise_profile__(self, extracted):
        if ('giai quyet ho so vào' in extracted):
            return True
        if ('hanh phuc' in extracted.lower()):
            return True
        if ('ma ho so' in extracted.lower()):
            return True
        if (self.__count_words__('[\n ]', extracted) < 2):
            return True
        if (re.match('\([^\(\)]+\)', extracted.strip()) is not None):
            return True
        if (re.search('ngay\s*\d+\s*thang\s*\d+\s*nam\s*\d+', extracted) is not None):
            return True

        return False

    def ner_profiles(self, text):
        return self.__ner_pattern__(text, self.patterns_profile, self.__is_noise_profile__)

    def ner_appoitment_letter_codes(self, text):
        return self.__ner_pattern__(text, self.patterns_alc)

    def ner_addresses(self, text):
        return self.__ner_pattern__(text, self.patterns_address)

    def ner_phone_numbers(self, text):
        return self.__ner_pattern__(text, self.patterns_phone_number)

    def ner_personal_paper_numbers(self, text):
        return self.__ner_pattern__(text, self.patterns_ppc)

    def ner_personal_paper_types(self, text):
        return ['căn cước công dân']

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



if __name__ == "__main__":
    ent = EntityRecognizer(Config())
    text = 'SỞ CÔNG THƯƠNG GIA LAI\n\nCỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM\n\nĐộc lập - Tự do - Hạnh phúc\n\n\n\nPHIẾU HẸN\n\nTRẢ KẾT QUẢ  KÊ KHAI LẠI GIÁ THUỐC SẢN XUẤT TẠI VIỆT NAM ĐỐI VỚI CƠ SỞ CÓ TRỤ SỞ SẢN XUẤT THUỐC ĐÓNG TRÊN ĐỊA BÀN THÀNH PHỐ\n\n(HS ĐKT mới đối với NNT là tổ chức KD (trừ các ĐV trực thuộc )\n\n\n\nTên đơn vị: Công ti TNHH ABZ\n\nMã số thuế: 197484244\n\nĐịa chỉ: P.2002, N2, CT 1.1, Chung cư ngõ 183 Hoàng Văn Thái, phường Khương Trung, quận Thanh Xuân, Hà Nội\n\nSố hồ sơ nhận: Gr81zcvJ3P\n\n\n\nCơ quan thuế đã nhận hồ sơ thuế của đơn vị gồm:\n\nSổ photo hộ khẩu\n\nCơ quan thuế sẽ trả kết quả giải quyết hồ sơ vào:  ngày 10 tháng 2 năm 2039\n\nHình thức trả kết quả:\n\n- Trực tiếp tại cơ quan thuế\n\nKhi đến nhận kết quả để nghỉ người đến nhận mang theo giấy hẹn này và giấy giới thiệu hoặc chứng minh thư nhân dân của người nhận. Nếu có vướng mắc, để nghỉ liên hệ đến :\n\n               - Số điện thoại: 914903685\n\n               - Địa chỉ: Số nhà 15, Tổ 2, khu 6B, phường Hồng Hải, thành phố Hạ Long, Quảng Ninh\n\nLâm Đồng, ngày 1 tháng 10\n\nCÁN BỘ VIẾT PHIẾU HẸN\n\n(Ký, ghi rõ họ tên)\n\nĐoàn Bửu Chưởng'
    print(ent.ner_province_district_cqhc(text))
