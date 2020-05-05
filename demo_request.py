import requests

def add():
    request_data = {
        "action":"add",
        "ft":
            {
                "FormID":89,
                "FormName":"test regex",
                "FormImageLink":"giay-hen.jpg",
                "APIOutput":{
                    "form_id":1,
                    "raw_text":"VP HĐND&UBND THỊ XÃ ĐÔNG TRIỀU \\n\\nCỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM \\n\\nBỘ PHẬN TNHS&TKQ \\n\\nĐộc lập - Tự do - Hạnh phúc \\n\\nSố: 47/54/NHS \\n\\nTỉnh Bắc Ninh, ngày 6 tháng 12 năm 2014 \\n\\nĐịa chỉ: Xóm 120, Phố Thanh Đàm, Phường Ninh Đa, Huyện Đơn Dương, Tỉnh Đắk Nông \\n\\nGIẤY BIÊN NHẬN HỒ SƠ \\n\\nMã hồ sơ: 06VL0FTMI5GN \\n\\n(Liên 2: Giao cho công dân, tổ chức)  \\n\\n Họ và tên: Công Huệ Hoa \\n\\nChức vụ: Cán bộ tiếp nhận hồ sơ và trả kết quả  \\n\\nĐã tiếp nhận hồ sơ của ông (bà): Khoa Lan Khuê \\n\\nSố điện thoại: 0704962870 \\n\\n Tên thủ tục tiếp nhận: Đăng ký biến động quyền sử dụng đất  \\n\\nHồ sơ gồm:  \\n\\n1. Giấy chứng nhận quyền sử dụng đất (bản gốc + bản sao)  \\n\\n2. Đơn xin tách, hợp thửa đất  \\n\\n - Toàn bộ hồ sơ tại giấy hẹn gốc  \\n\\n- Bổ sung thêm biên bản xác minh đơn kiến nghị  \\n\\nNgày tiếp nhận hồ sơ: 14:29:35, ngày 6 tháng 12 năm 2014 \\n\\n Ngày hẹn trả kết quả: 19:35:29, ngày 4 tháng 10 năm 2013 \\n\\n Để biết thông tin về thủ tục hành chính, tình trạng xử lý hồ sơ, ông (bà) vui lòng điện thoại đến số \\n0769620471 hoặc email cho chúng tôi theo địa chỉ donghoi@quangbinh.gov.vn \\n\\n NGƯỜI NỘP HS   \\n\\nNGƯỜI NHẬN KQ  \\n\\nNGƯỜI TIẾP.NHẬN \\n\\n(Ký và ghi rõ họ tên) \\n\\n(Ký và ghi rõ họ tên)  \\n\\n(Ký và ghi rõ họ tên) \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\nThời gian nhận kết quả trên \\n\\nThời gian nhận kết quả trên \\n\\nthực tế: 19 giờ 35 phút, ngày 4  thực tế: …. giờ….phút, ngày \\n\\ntháng 10 năm 2013 \\n\\n \\n\\n \\n\\n \\n\\n…. tháng….năm…. \\n\\n  Công Huệ Hoa \\n\\nĐể tra cứu thông tin hồ sơ, công dân đưa vào máy quét mã vạch hoặc nhập mã hồ sơ \\n\\nvào phần tra cứu và nhấn phím Enter (không nhập dấu *) \\n\\n \\n\\n \\n\\n \\n \\n\\n",
                    },
	        }
    }

    response = requests.post('http://127.0.0.1:8888/retrain', json=request_data)
    print(response.json())

def add2():
    request_data = {
        "action":"add",
        "ft":
            {
                "FormID":89,
                "FormName":"test regex",
                "FormImageLink":"giay-hen.jpg",
                "APIOutput":{
                    "form_id":1,
                    "raw_text":"Add 2",
                    },
	        }
    }

    response = requests.post('http://127.0.0.1:8888/retrain', json=request_data)
    print(response.json())

def update():
    request_data = {
        "action":"update",
        "ft":
            {
                "FormID":89,
                "FormName":"test regex",
                "FormImageLink":"giay-hen.jpg",
                "APIOutput":{
                    "form_id":1,
                    "raw_text":"Update",
                    },
	        }
    }

    response = requests.post('http://127.0.0.1:8888/retrain', json=request_data)
    print(response.json())

def update2():
    request_data = {
        "action":"update",
        "ft":
            {
                "FormID":1111,
                "FormName":"test regex",
                "FormImageLink":"giay-hen.jpg",
                "APIOutput":{
                    "form_id":1,
                    "raw_text":"VP HĐND&UBND THỊ XÃ ĐÔNG TRIỀU \\n\\nCỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM \\n\\nBỘ PHẬN TNHS&TKQ \\n\\nĐộc lập - Tự do - Hạnh phúc \\n\\nSố: 47/54/NHS \\n\\nTỉnh Bắc Ninh, ngày 6 tháng 12 năm 2014 \\n\\nĐịa chỉ: Xóm 120, Phố Thanh Đàm, Phường Ninh Đa, Huyện Đơn Dương, Tỉnh Đắk Nông \\n\\nGIẤY BIÊN NHẬN HỒ SƠ \\n\\nMã hồ sơ: 06VL0FTMI5GN \\n\\n(Liên 2: Giao cho công dân, tổ chức)  \\n\\n Họ và tên: Công Huệ Hoa \\n\\nChức vụ: Cán bộ tiếp nhận hồ sơ và trả kết quả  \\n\\nĐã tiếp nhận hồ sơ của ông (bà): Khoa Lan Khuê \\n\\nSố điện thoại: 0704962870 \\n\\n Tên thủ tục tiếp nhận: Đăng ký biến động quyền sử dụng đất  \\n\\nHồ sơ gồm:  \\n\\n1. Giấy chứng nhận quyền sử dụng đất (bản gốc + bản sao)  \\n\\n2. Đơn xin tách, hợp thửa đất  \\n\\n - Toàn bộ hồ sơ tại giấy hẹn gốc  \\n\\n- Bổ sung thêm biên bản xác minh đơn kiến nghị  \\n\\nNgày tiếp nhận hồ sơ: 14:29:35, ngày 6 tháng 12 năm 2014 \\n\\n Ngày hẹn trả kết quả: 19:35:29, ngày 4 tháng 10 năm 2013 \\n\\n Để biết thông tin về thủ tục hành chính, tình trạng xử lý hồ sơ, ông (bà) vui lòng điện thoại đến số \\n0769620471 hoặc email cho chúng tôi theo địa chỉ donghoi@quangbinh.gov.vn \\n\\n NGƯỜI NỘP HS   \\n\\nNGƯỜI NHẬN KQ  \\n\\nNGƯỜI TIẾP.NHẬN \\n\\n(Ký và ghi rõ họ tên) \\n\\n(Ký và ghi rõ họ tên)  \\n\\n(Ký và ghi rõ họ tên) \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\nThời gian nhận kết quả trên \\n\\nThời gian nhận kết quả trên \\n\\nthực tế: 19 giờ 35 phút, ngày 4  thực tế: …. giờ….phút, ngày \\n\\ntháng 10 năm 2013 \\n\\n \\n\\n \\n\\n \\n\\n…. tháng….năm…. \\n\\n  Công Huệ Hoa \\n\\nĐể tra cứu thông tin hồ sơ, công dân đưa vào máy quét mã vạch hoặc nhập mã hồ sơ \\n\\nvào phần tra cứu và nhấn phím Enter (không nhập dấu *) \\n\\n \\n\\n \\n\\n \\n \\n\\n",
                    },
	        }
    }

    response = requests.post('http://127.0.0.1:8888/retrain', json=request_data)
    print(response.json())

def delete():
    request_data = {
        "action":"delete",
        "ft":
            {
                "FormID":89,
                "FormName":"test regex",
                "FormImageLink":"giay-hen.jpg",
                "APIOutput":{
                    "form_id":1,
                    "raw_text":"VP HĐND&UBND THỊ XÃ ĐÔNG TRIỀU \\n\\nCỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM \\n\\nBỘ PHẬN TNHS&TKQ \\n\\nĐộc lập - Tự do - Hạnh phúc \\n\\nSố: 47/54/NHS \\n\\nTỉnh Bắc Ninh, ngày 6 tháng 12 năm 2014 \\n\\nĐịa chỉ: Xóm 120, Phố Thanh Đàm, Phường Ninh Đa, Huyện Đơn Dương, Tỉnh Đắk Nông \\n\\nGIẤY BIÊN NHẬN HỒ SƠ \\n\\nMã hồ sơ: 06VL0FTMI5GN \\n\\n(Liên 2: Giao cho công dân, tổ chức)  \\n\\n Họ và tên: Công Huệ Hoa \\n\\nChức vụ: Cán bộ tiếp nhận hồ sơ và trả kết quả  \\n\\nĐã tiếp nhận hồ sơ của ông (bà): Khoa Lan Khuê \\n\\nSố điện thoại: 0704962870 \\n\\n Tên thủ tục tiếp nhận: Đăng ký biến động quyền sử dụng đất  \\n\\nHồ sơ gồm:  \\n\\n1. Giấy chứng nhận quyền sử dụng đất (bản gốc + bản sao)  \\n\\n2. Đơn xin tách, hợp thửa đất  \\n\\n - Toàn bộ hồ sơ tại giấy hẹn gốc  \\n\\n- Bổ sung thêm biên bản xác minh đơn kiến nghị  \\n\\nNgày tiếp nhận hồ sơ: 14:29:35, ngày 6 tháng 12 năm 2014 \\n\\n Ngày hẹn trả kết quả: 19:35:29, ngày 4 tháng 10 năm 2013 \\n\\n Để biết thông tin về thủ tục hành chính, tình trạng xử lý hồ sơ, ông (bà) vui lòng điện thoại đến số \\n0769620471 hoặc email cho chúng tôi theo địa chỉ donghoi@quangbinh.gov.vn \\n\\n NGƯỜI NỘP HS   \\n\\nNGƯỜI NHẬN KQ  \\n\\nNGƯỜI TIẾP.NHẬN \\n\\n(Ký và ghi rõ họ tên) \\n\\n(Ký và ghi rõ họ tên)  \\n\\n(Ký và ghi rõ họ tên) \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\nThời gian nhận kết quả trên \\n\\nThời gian nhận kết quả trên \\n\\nthực tế: 19 giờ 35 phút, ngày 4  thực tế: …. giờ….phút, ngày \\n\\ntháng 10 năm 2013 \\n\\n \\n\\n \\n\\n \\n\\n…. tháng….năm…. \\n\\n  Công Huệ Hoa \\n\\nĐể tra cứu thông tin hồ sơ, công dân đưa vào máy quét mã vạch hoặc nhập mã hồ sơ \\n\\nvào phần tra cứu và nhấn phím Enter (không nhập dấu *) \\n\\n \\n\\n \\n\\n \\n \\n\\n",
                    },
	        }
    }

    response = requests.post('http://127.0.0.1:8888/retrain', json=request_data)
    print(response.json())

def delete_all():
    request_data = {
        "action":"delete_all",
        "ft":
            {
                "FormID":89,
                "FormName":"test regex",
                "FormImageLink":"giay-hen.jpg",
                "APIOutput":{
                    "form_id":1,
                    "raw_text":"VP HĐND&UBND THỊ XÃ ĐÔNG TRIỀU \\n\\nCỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM \\n\\nBỘ PHẬN TNHS&TKQ \\n\\nĐộc lập - Tự do - Hạnh phúc \\n\\nSố: 47/54/NHS \\n\\nTỉnh Bắc Ninh, ngày 6 tháng 12 năm 2014 \\n\\nĐịa chỉ: Xóm 120, Phố Thanh Đàm, Phường Ninh Đa, Huyện Đơn Dương, Tỉnh Đắk Nông \\n\\nGIẤY BIÊN NHẬN HỒ SƠ \\n\\nMã hồ sơ: 06VL0FTMI5GN \\n\\n(Liên 2: Giao cho công dân, tổ chức)  \\n\\n Họ và tên: Công Huệ Hoa \\n\\nChức vụ: Cán bộ tiếp nhận hồ sơ và trả kết quả  \\n\\nĐã tiếp nhận hồ sơ của ông (bà): Khoa Lan Khuê \\n\\nSố điện thoại: 0704962870 \\n\\n Tên thủ tục tiếp nhận: Đăng ký biến động quyền sử dụng đất  \\n\\nHồ sơ gồm:  \\n\\n1. Giấy chứng nhận quyền sử dụng đất (bản gốc + bản sao)  \\n\\n2. Đơn xin tách, hợp thửa đất  \\n\\n - Toàn bộ hồ sơ tại giấy hẹn gốc  \\n\\n- Bổ sung thêm biên bản xác minh đơn kiến nghị  \\n\\nNgày tiếp nhận hồ sơ: 14:29:35, ngày 6 tháng 12 năm 2014 \\n\\n Ngày hẹn trả kết quả: 19:35:29, ngày 4 tháng 10 năm 2013 \\n\\n Để biết thông tin về thủ tục hành chính, tình trạng xử lý hồ sơ, ông (bà) vui lòng điện thoại đến số \\n0769620471 hoặc email cho chúng tôi theo địa chỉ donghoi@quangbinh.gov.vn \\n\\n NGƯỜI NỘP HS   \\n\\nNGƯỜI NHẬN KQ  \\n\\nNGƯỜI TIẾP.NHẬN \\n\\n(Ký và ghi rõ họ tên) \\n\\n(Ký và ghi rõ họ tên)  \\n\\n(Ký và ghi rõ họ tên) \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\nThời gian nhận kết quả trên \\n\\nThời gian nhận kết quả trên \\n\\nthực tế: 19 giờ 35 phút, ngày 4  thực tế: …. giờ….phút, ngày \\n\\ntháng 10 năm 2013 \\n\\n \\n\\n \\n\\n \\n\\n…. tháng….năm…. \\n\\n  Công Huệ Hoa \\n\\nĐể tra cứu thông tin hồ sơ, công dân đưa vào máy quét mã vạch hoặc nhập mã hồ sơ \\n\\nvào phần tra cứu và nhấn phím Enter (không nhập dấu *) \\n\\n \\n\\n \\n\\n \\n \\n\\n",
                    },
	        }
    }

    response = requests.post('http://127.0.0.1:8888/retrain', json=request_data)
    print(response.json())

def retrain_original():
    request_data = {
        "action":"train_original",
        "ft":
            {
                "FormID":89,
                "FormName":"test regex",
                "FormImageLink":"giay-hen.jpg",
                "APIOutput":{
                    "form_id":1,
                    "raw_text":"VP HĐND&UBND THỊ XÃ ĐÔNG TRIỀU \\n\\nCỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM \\n\\nBỘ PHẬN TNHS&TKQ \\n\\nĐộc lập - Tự do - Hạnh phúc \\n\\nSố: 47/54/NHS \\n\\nTỉnh Bắc Ninh, ngày 6 tháng 12 năm 2014 \\n\\nĐịa chỉ: Xóm 120, Phố Thanh Đàm, Phường Ninh Đa, Huyện Đơn Dương, Tỉnh Đắk Nông \\n\\nGIẤY BIÊN NHẬN HỒ SƠ \\n\\nMã hồ sơ: 06VL0FTMI5GN \\n\\n(Liên 2: Giao cho công dân, tổ chức)  \\n\\n Họ và tên: Công Huệ Hoa \\n\\nChức vụ: Cán bộ tiếp nhận hồ sơ và trả kết quả  \\n\\nĐã tiếp nhận hồ sơ của ông (bà): Khoa Lan Khuê \\n\\nSố điện thoại: 0704962870 \\n\\n Tên thủ tục tiếp nhận: Đăng ký biến động quyền sử dụng đất  \\n\\nHồ sơ gồm:  \\n\\n1. Giấy chứng nhận quyền sử dụng đất (bản gốc + bản sao)  \\n\\n2. Đơn xin tách, hợp thửa đất  \\n\\n - Toàn bộ hồ sơ tại giấy hẹn gốc  \\n\\n- Bổ sung thêm biên bản xác minh đơn kiến nghị  \\n\\nNgày tiếp nhận hồ sơ: 14:29:35, ngày 6 tháng 12 năm 2014 \\n\\n Ngày hẹn trả kết quả: 19:35:29, ngày 4 tháng 10 năm 2013 \\n\\n Để biết thông tin về thủ tục hành chính, tình trạng xử lý hồ sơ, ông (bà) vui lòng điện thoại đến số \\n0769620471 hoặc email cho chúng tôi theo địa chỉ donghoi@quangbinh.gov.vn \\n\\n NGƯỜI NỘP HS   \\n\\nNGƯỜI NHẬN KQ  \\n\\nNGƯỜI TIẾP.NHẬN \\n\\n(Ký và ghi rõ họ tên) \\n\\n(Ký và ghi rõ họ tên)  \\n\\n(Ký và ghi rõ họ tên) \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\n \\n\\nThời gian nhận kết quả trên \\n\\nThời gian nhận kết quả trên \\n\\nthực tế: 19 giờ 35 phút, ngày 4  thực tế: …. giờ….phút, ngày \\n\\ntháng 10 năm 2013 \\n\\n \\n\\n \\n\\n \\n\\n…. tháng….năm…. \\n\\n  Công Huệ Hoa \\n\\nĐể tra cứu thông tin hồ sơ, công dân đưa vào máy quét mã vạch hoặc nhập mã hồ sơ \\n\\nvào phần tra cứu và nhấn phím Enter (không nhập dấu *) \\n\\n \\n\\n \\n\\n \\n \\n\\n",
                    },
	        }
    }

    response = requests.post('http://103.104.117.175/retrain', json=request_data)
    print(response.json())

if __name__ == "__main__":
    retrain_original()