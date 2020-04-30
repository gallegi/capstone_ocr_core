from vncorenlp import VnCoreNLP
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
vncorenlp_file = r'F:\Github\ocrcore\weights\VnCoreNLP-1.1.1.jar'
annotator = VnCoreNLP(vncorenlp_file)


# Input
text = 'SỞ CÔNG THƯƠNG GIA LAI\n\nCỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM\n\nĐộc lập - Tự do - Hạnh phúc\n\n\n\nPHIẾU HẸN\n\nTRẢ KẾT QUẢ  KÊ KHAI LẠI GIÁ THUỐC SẢN XUẤT TẠI VIỆT NAM ĐỐI VỚI CƠ SỞ CÓ TRỤ SỞ SẢN XUẤT THUỐC ĐÓNG TRÊN ĐỊA BÀN THÀNH PHỐ\n\n(HS ĐKT mới đối với NNT là tổ chức KD (trừ các ĐV trực thuộc )\n\n\n\nTên đơn vị: Công ti TNHH ABZ\n\nMã số thuế: 197484244\n\nĐịa chỉ: P.2002, N2, CT 1.1, Chung cư ngõ 183 Hoàng Văn Thái, phường Khương Trung, quận Thanh Xuân, Hà Nội\n\nSố hồ sơ nhận: Gr81zcvJ3P\n\n\n\nCơ quan thuế đã nhận hồ sơ thuế của đơn vị gồm:\n\nSổ photo hộ khẩu\n\nCơ quan thuế sẽ trả kết quả giải quyết hồ sơ vào:  ngày 10 tháng 2 năm 2039\n\nHình thức trả kết quả:\n\n- Trực tiếp tại cơ quan thuế\n\nKhi đến nhận kết quả để nghỉ người đến nhận mang theo giấy hẹn này và giấy giới thiệu hoặc chứng minh thư nhân dân của người nhận. Nếu có vướng mắc, để nghỉ liên hệ đến :\n\n               - Số điện thoại: 914903685\n\n               - Địa chỉ: Số nhà 15, Tổ 2, khu 6B, phường Hồng Hải, thành phố Hạ Long, Quảng Ninh\n\nLâm Đồng, ngày 1 tháng 10\n\nCÁN BỘ VIẾT PHIẾU HẸN\n\n(Ký, ghi rõ họ tên)\n\nĐoàn Bửu Chưởng'


# To perform word segmentation, POS tagging, NER and then dependency parsing
annotated_text = annotator.annotate(text)

# To perform word segmentation only
# word_segmented_text = annotator.tokenize(text)

annotated_text = annotated_text['sentences'][0]+ annotated_text['sentences'][1]
annotated_text = pd.DataFrame(annotated_text)
names = list(annotated_text[annotated_text['nerLabel']=='B-PER']['form'].str.replace('_',' '))
annotator.close()