from vncorenlp import VnCoreNLP
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
vncorenlp_file = r'F:\Github\ocrcore\weights\VnCoreNLP-1.1.1.jar'
annotator = VnCoreNLP(vncorenlp_file)


# Input
text = 'VĂN PHÒNG ỦY BAN NHÂN DÂN TỈNH CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAMTT KIỂM SOÁT TTHC & PHỤC VU HCC Độc lập - Tự do - Hạnh phúcSố: 00092/TTPVHCC Đồng Thúóp, ngày 20 tháng 11 năm 2019GIẤY TIẾP NHẬN HỒ SƠ VÀ HẸN TRẢ KẾT QUẢBộ phận tiếp nhận và trả kết quả hồ sơ: Sở Nội vụTiếp nhận hồ sơ của: _ VÕ MINH DƯƠNGĐịa chỉ: KHÓM 3 THỊ TRẤN MỸ AN, thị trấn Mỹ An, huyện Tháp Mười, tỉnh Đồng ThápSố điện thoại: 0939572712Nội dung đang yêu cầu giải quyết: 05 — Thủ tục tặng thưởng Bằng khen cấp tỉnh theo đợt hoặc chuyênđề cấp cho VÕ MINH DƯƠNG1. Thành phần hồ sơ nộp gồm:Các loại chứng từ có trong hồ sơBáo cáo thành tích của các trường hợp đề nghị khen 4.101 <® ¿1zTờ trình kèm theo danh sách của sở, ban, ngành, đoàn NZ Tp. 7Á.0thể tỉnhBiên bản của Trưởng khối, Trưởng cụm thi đua của tỉnh 0                   - 1 ++=.CQ¬ơa 2. Số lượng hồ sơ: 1 (bộ)3. Thời gian giải quyết hồ sơ là: 25 ngày làm việc4. Thời gian trả kết quả giải quyết hồ sơ: 08 giờ 37 phút, ngày 20 tháng 11 năm 20195, Thời gian trả kết quả của giải quyết hồ sơ: 08 giờ 37 phút, ngày 25 tháng 12 năm 20196. Ghi chú hồ sơ: TỜ TRÌNH, BIÊN BẢN7. Liên kết thành phần hồ sơ8. Đăng ký nhận kết quả tại: Trung tâm kiểm soát TTHC và phục vụ Đồng ThápVào sổ theo dõi hồ sơ, Quyền số: Số thứ tự: 00092NGƯỜI NỘP HỒ Sơ NGƯỜI NHẬN HỒ SƠ(Ký và ghi rõ họ tên) (Ký và ghi rõ họ tên)VÕ MINH DƯƠNG Đặng Thị Bích Trâm'


# To perform word segmentation, POS tagging, NER and then dependency parsing
annotated_text = annotator.annotate(text)

# To perform word segmentation only
# word_segmented_text = annotator.tokenize(text)

annotated_text = annotated_text['sentences'][0]+ annotated_text['sentences'][1]
annotated_text = pd.DataFrame(annotated_text)
names = list(annotated_text[annotated_text['nerLabel']=='B-PER']['form'].str.replace('_',' '))
annotator.close()