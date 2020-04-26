import requests

def main():
    request_data = {
        "api_output": 
        {
            "form_id": -1,
            "raw_text": "VP HĐND&UBND THỊ XÃ ĐÔNG TRIỀU \n\nCỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM \n\nBỘ PHẬN TNHS&TKQ \n\nĐộc lập - Tự do - Hạnh phúc \n\nSố: 47/54/NHS\n\nTỉnh Bắc Ninh, ngày 6 tháng 12 năm 2014 \n\nĐịa chỉ: Xóm 120, Phố Thanh Đàm, Phường Ninh Đa, Huyện Đơn Dương, Tỉnh Đắk Nông \n\nGIẤY BIÊN NHẬN HỒ SƠ \n\nMã hồ sơ: 06VL0FTMI5GN \n\n(Liên 2: Giao cho công dân, tổ chức)  \n\nHọ và tên: Công Huệ Hoa \n\nChức vụ: Cán bộ tiếp nhận hồ sơ và trả kết quả  \n\nĐã tiếp nhận hồ sơ của ông (bà): Khoa Lan Khuê \n\nSố điện thoại: 0704962870 \n\nTên thủ tục tiếp nhận: Đăng ký biến động quyền sử dụng đất  \n\nHồ sơ gồm:  \n\n1. Giấy chứng nhận quyền sử dụng đất (bản gốc + bản sao)  \n\n2. Đơn xin tách, hợp thửa đất  \n\n- Toàn bộ hồ sơ tại giấy hẹn gốc  \n\n- Bổ sung thêm biên bản xác minh đơn kiến nghị  \n\nNgày tiếp nhận hồ sơ: 14:29:35, ngày 6 tháng 12 năm 2014 \n\nNgày hẹn trả kết quả: 19:35:29, ngày 4 tháng 10 năm 2013 \n\nĐể biết thông tin về thủ tục hành chính, tình trạng xử lý hồ sơ, ông (bà) vui lòng điện thoại đến số \n0769620471 hoặc email cho chúng tôi theo địa chỉ donghoi@quangbinh.gov.vn \n\nNGƯỜI NỘP HS   \n\nNGƯỜI NHẬN KQ  \n\nNGƯỜI TIẾP.NHẬN \n\n(Ký và ghi rõ họ tên) \n\n(Ký và ghi rõ họ tên)  \n\n(Ký và ghi rõ họ tên)  \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\nThời gian nhận kết quả trên \n\nThời gian nhận kết quả trên \n\nthực tế: 19 giờ 35 phút, ngày 4  thực tế: …. giờ….phút, ngày \n\ntháng 10 năm 2013 \n\n \n\n \n\n \n\n…. tháng….năm…. \n\n  Công Huệ Hoa \n\nĐể tra cứu thông tin hồ sơ, công dân đưa vào máy quét mã vạch hoặc nhập mã hồ sơ  \n\nvào phần tra cứu và nhấn phím Enter (không nhập dấu *) \n\n \n\n \n\n \n \n\n",
            "province": ["Bình Định", "Đắk Nông"],
            "district": ["Thị xã Bắc Ninh", "Đơn Dương"],
            "public_administration": ["UBND Thị xã Bắc Ninh"],
            "profile": ["Cấp lại CMT", "Cấp lại con dấu"],
            "appointment_letter_code": ["1234"],
            "name": [],
            "phone_number": ["0704962870"],
            "street": ["Đường Cầu Diễn"],
            "personal_paper_type": ["Căn cước công dân"],
            "personal_paper_number": ["94567812"],
            "issued_date": ["2020-04-20"],
            "issued_place": ["Hà Nội"]
        }
    }

    response = requests.post('http://127.0.0.1:8887/retrain', json=request_data)
    print(response.json()['ret'])

if __name__ == "__main__":
    main()