import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load structure
with open(r'D:\TIKTOK\KKhome - Update VBPL\VBan\tt89_structure.json', 'r', encoding='utf-8') as f:
    chapters = json.load(f)

wb = openpyxl.Workbook()

# Style definitions
font_title = Font(name='Segoe UI', size=16, bold=True, color='1E3A8A')
font_header = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
font_bold = Font(name='Segoe UI', size=10, bold=True, color='0F172A')
font_normal = Font(name='Segoe UI', size=10, color='1E293B')
font_link = Font(name='Segoe UI', size=10, color='2563EB', underline='single')

fill_navy = PatternFill(start_color='1E40AF', end_color='1E40AF', fill_type='solid')
fill_blue_light = PatternFill(start_color='EFF6FF', end_color='EFF6FF', fill_type='solid')
fill_gray_light = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
fill_green_light = PatternFill(start_color='DCFCE7', end_color='DCFCE7', fill_type='solid')
fill_orange_light = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid')

thin_border_side = Side(style='thin', color='CBD5E1')
border_all = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
align_left = Alignment(horizontal='left', vertical='center', wrap_text=True)

# -----------------------------------------------------------------------------
# SHEET 1: DANH MỤC 101 ĐIỀU KHOẢN
# -----------------------------------------------------------------------------
ws1 = wb.active
ws1.title = "Danh mục 101 Điều Khoản"
ws1.views.sheetView[0].showGridLines = True

ws1.merge_cells('A1:E1')
ws1['A1'] = "DANH MỤC CÁC ĐIỀU KHOẢN - THÔNG TƯ SỐ 89/2026/TT-BTC"
ws1['A1'].font = font_title
ws1['A1'].alignment = align_left

ws1.merge_cells('A2:E2')
ws1['A2'] = "Căn cứ Luật Quản lý thuế số 108/2025/QH15 & Nghị định số 252/2026/NĐ-CP • Hiệu lực từ 01/07/2026"
ws1['A2'].font = Font(name='Segoe UI', size=11, italic=True, color='64748B')
ws1['A2'].alignment = align_left

headers_ws1 = ["STT", "Số Điều", "Tên Điều Khoản", "Thuộc Chương", "Phân Hệ / Trọng Tâm"]
for col_num, h in enumerate(headers_ws1, 1):
    c = ws1.cell(row=4, column=col_num)
    c.value = h
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = border_all
ws1.row_dimensions[4].height = 28

row_idx = 5
stt = 1
for c in chapters:
    c_title = c.get('title', '')
    for a in c.get('articles', []):
        num = a.get('number', 0)
        title = a.get('title', '')
        if num == 0:
            continue
            
        short_title = title.replace(f"Điều {num}. ", "").replace(f"Điều {num}.", "").strip()
        
        # Categorize
        cat = "Quy định chung"
        if 7 <= num <= 16: cat = "Giao dịch điện tử & T-VAN"
        elif 17 <= num <= 34: cat = "Khai & Phân bổ thuế (GTGT, TNDN, TNCN, TMĐT)"
        elif 35 <= num <= 44: cat = "Nộp thuế, gia hạn & bù trừ nợ"
        elif 45 <= num <= 64: cat = "Thủ tục Hoàn thuế & Nộp thừa"
        elif 65 <= num <= 86: cat = "Miễn, giảm, nợ thuế & DTA"
        elif 87 <= num <= 90: cat = "Kiểm tra thuế & Giám sát từ xa"
        elif 91 <= num <= 94: cat = "Một cửa liên thông điện tử"
        elif 95 <= num <= 98: cat = "Ủy nhiệm thu & Mẫu biểu"
        elif 99 <= num <= 101: cat = "Hiệu lực & Chuyển tiếp"

        fill_row = fill_blue_light if stt % 2 == 0 else fill_gray_light
        
        ws1.cell(row=row_idx, column=1, value=stt).alignment = align_center
        ws1.cell(row=row_idx, column=2, value=f"Điều {num}").alignment = align_center
        ws1.cell(row=row_idx, column=3, value=short_title).alignment = align_left
        ws1.cell(row=row_idx, column=4, value=c_title).alignment = align_left
        ws1.cell(row=row_idx, column=5, value=cat).alignment = align_left

        for col in range(1, 6):
            cell = ws1.cell(row=row_idx, column=col)
            cell.font = font_normal
            cell.border = border_all
            cell.fill = fill_row
            
        ws1.row_dimensions[row_idx].height = 22
        row_idx += 1
        stt += 1

# -----------------------------------------------------------------------------
# SHEET 2: BẢNG SO SÁNH ĐIỂM MỚI
# -----------------------------------------------------------------------------
ws2 = wb.create_sheet(title="Điểm Mới Nổi Bật")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells('A1:E1')
ws2['A1'] = "BẢNG TỔNG HỢP SO SÁNH ĐIỂM MỚI - THÔNG TƯ 89/2026/TT-BTC"
ws2['A1'].font = font_title
ws2['A1'].alignment = align_left

headers_ws2 = ["STT", "Lĩnh Vực / Sắc Thuế", "Quy Định Trước Đây", "Quy Định Mới Tại TT 89/2026", "Tác Động Đối Với NNT"]
for col_num, h in enumerate(headers_ws2, 1):
    c = ws2.cell(row=3, column=col_num)
    c.value = h
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = border_all
ws2.row_dimensions[3].height = 28

changes_data = [
    (1, "Sàn Thương Mại Điện Tử (Shopee, TikTok Shop, Lazada...)", 
     "Sàn chỉ có trách nhiệm cung cấp định kỳ thông tin doanh thu của người bán cho cơ quan thuế theo quý (TT 80/2021). Người bán phải tự kê khai và nộp thuế.",
     "Chủ quản nền tảng sàn TMĐT trực tiếp KHẤU TRỪ, KÊ KHAI VÀ NỘP THAY toàn bộ số thuế phát sinh từ từng giao dịch của cá nhân/hộ kinh doanh (Điều 33).",
     "Cá nhân/hộ bán online không cần tự đi kê khai thủ công; triệt tiêu hoàn toàn tình trạng trốn thuế TMĐT; minh bạch dòng tiền."),
    (2, "Xử lý sự cố mạng nộp thuế", 
     "Doanh nghiệp phải chủ động chứng minh hệ thống lỗi, xin xác nhận văn bản từ nhà mạng để không bị tính chậm nộp (TT 19/2021).",
     "Cơ quan thuế công khai thời gian sự cố trên Cổng điện tử; tự động gia hạn thời hạn nộp tờ khai và tiền thuế sang ngày làm việc tiếp theo sau khi sửa xong (Điều 12).",
     "Doanh nghiệp không bị phạt oan tiền chậm nộp 0.03%/ngày và vi phạm thời hạn nộp hồ sơ khi Cổng thuế quốc gia gặp nghẽn mạng."),
    (3, "Nhà thầu nước ngoài & Nhà cung cấp nước ngoài (NCCNN)", 
     "Áp dụng cơ chế phức tạp theo TT 103/2014; bên mua tại Việt Nam phải tự tính và khấu trừ thủ công với rủi ro thuế lớn.",
     "Bãi bỏ hoàn toàn TT 103/2014; NCCNN đăng ký, kê khai và nộp thuế trực tiếp qua Cổng thuế quốc tế; hoặc Ngân hàng/Trung gian thanh toán khấu trừ tự động (Điều 30, 31).",
     "Chuẩn hóa quy trình quốc tế, giảm thiểu tranh chấp thuế cho các doanh nghiệp mua dịch vụ SaaS, phần mềm, quảng cáo toàn cầu."),
    (4, "Phương thức Kiểm tra thuế", 
     "Chủ yếu kiểm tra trực tiếp tại trụ sở người nộp thuế, yêu cầu in ấn trình nộp hồ sơ chứng từ giấy khối lượng lớn.",
     "Bổ sung phương thức KIỂM TRA TRỰC TUYẾN TỪ XA trên cơ sở dữ liệu hóa đơn điện tử lớn và truyền nhận dữ liệu số (Điều 89).",
     "Giảm chi phí tiếp đoàn kiểm tra; doanh nghiệp minh bạch và tuân thủ tốt sẽ được cơ quan thuế thẩm định nhanh qua hệ thống số."),
    (5, "Hoàn thuế và Xử lý tiền nộp thừa", 
     "Thủ tục hoàn tiền nộp thừa và hoàn GTGT tách rời, thời gian luân chuyển tra soát thủ công kéo dài.",
     "Cơ chế Lệnh hoàn trả điện tử qua Kho bạc; tự động bù trừ tiền nộp thừa với các nghĩa vụ nợ thuế khác trước khi chuyển khoản (Điều 42, 51, 61).",
     "Tiền hoàn thuế về tài khoản ngân hàng của doanh nghiệp nhanh chóng, minh bạch tiến độ qua thông báo điện tử."),
    (6, "Kết nối hạ tầng trực tiếp & T-VAN", 
     "T-VAN chỉ là đơn vị trung gian truyền nhận đơn thuần; chưa có cơ chế kết nối API dữ liệu thuế lớn.",
     "Cho phép các doanh nghiệp lớn có hạ tầng CNTT chuẩn hóa kết nối API trực tiếp vào Hệ thống thông tin quản lý thuế (Điều 14).",
     "Tối ưu vận hành cho các tập đoàn, chuỗi bán lẻ, sàn TMĐT có hàng triệu giao dịch mỗi ngày.")
]

row_idx = 4
for item in changes_data:
    stt_val, field_val, old_val, new_val, impact_val = item
    ws2.cell(row=row_idx, column=1, value=stt_val).alignment = align_center
    ws2.cell(row=row_idx, column=2, value=field_val).alignment = align_left
    ws2.cell(row=row_idx, column=3, value=old_val).alignment = align_left
    ws2.cell(row=row_idx, column=4, value=new_val).alignment = align_left
    ws2.cell(row=row_idx, column=5, value=impact_val).alignment = align_left

    for col in range(1, 6):
        cell = ws2.cell(row=row_idx, column=col)
        cell.font = font_normal
        cell.border = border_all
        if col == 3: cell.fill = fill_orange_light
        elif col == 4: cell.fill = fill_green_light
        else: cell.fill = fill_gray_light
        
    ws2.row_dimensions[row_idx].height = 65
    row_idx += 1

# -----------------------------------------------------------------------------
# SHEET 3: DANH MỤC BIỂU MẪU CHỦ YẾU
# -----------------------------------------------------------------------------
ws3 = wb.create_sheet(title="Hệ Thống Mẫu Biểu")
ws3.views.sheetView[0].showGridLines = True

ws3.merge_cells('A1:F1')
ws3['A1'] = "DANH MỤC CÁC BIỂU MẪU & THỦ TỤC ĐIỆN TỬ - THÔNG TƯ 89/2026/TT-BTC"
ws3['A1'].font = font_title
ws3['A1'].alignment = align_left

headers_ws3 = ["STT", "Ký Hiệu Mẫu", "Tên Mẫu Biểu / Văn Bản", "Phân Hệ Nghiệp Vụ", "Căn Cứ Điều Khoản", "Đối Tượng Sử Dụng"]
for col_num, h in enumerate(headers_ws3, 1):
    c = ws3.cell(row=3, column=col_num)
    c.value = h
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = border_all
ws3.row_dimensions[3].height = 28

forms_data = [
    (1, "Mẫu số 01/ĐK-TĐT", "Tờ khai đăng ký giao dịch với cơ quan thuế bằng phương thức điện tử", "Giao dịch điện tử", "Điều 13", "Người nộp thuế mới đăng ký thuế điện tử"),
    (2, "Mẫu số 02/ĐK-TĐT", "Văn bản đề nghị kết nối trực tiếp với Hệ thống CNTT quản lý thuế", "Giao dịch điện tử", "Điều 14", "Doanh nghiệp lớn có hạ tầng kết nối trực tiếp"),
    (3, "Mẫu số 01/TS", "Văn bản đề nghị tra soát thông tin thu nộp ngân sách nhà nước", "Nộp thuế & Tra soát", "Điều 37", "Người nộp thuế nộp sai tiểu mục, cơ quan thu"),
    (4, "Mẫu số 01/GHN", "Văn bản đề nghị gia hạn nộp thuế, tiền chậm nộp, tiền phạt", "Gia hạn nộp thuế", "Điều 38", "Doanh nghiệp gặp thiên tai, hỏa hoạn, bất khả kháng"),
    (5, "Mẫu số 01/MGTH", "Văn bản đề nghị miễn (giảm) tiền chậm nộp tiền thuế", "Miễn chậm nộp", "Điều 41", "Người nộp thuế đủ điều kiện miễn tiền chậm nộp"),
    (6, "Mẫu số 01/ĐNHT", "Giấy đề nghị hoàn trả khoản thu ngân sách nhà nước", "Hoàn thuế", "Điều 46, Điều 56", "Người nộp thuế đề nghị hoàn GTGT, TTĐB, tiền thừa"),
    (7, "Mẫu số 01/QĐHT", "Quyết định về việc hoàn trả khoản thu ngân sách nhà nước", "Hoàn thuế", "Điều 50, Điều 60", "Cơ quan thuế ban hành hoàn trả cho NNT"),
    (8, "Mẫu số 02/QĐHT", "Quyết định hoàn trả kiêm bù trừ thu ngân sách nhà nước", "Hoàn thuế", "Điều 50, Điều 60", "Cơ quan thuế bù trừ nợ trước khi hoàn"),
    (9, "Mẫu số 01/KN-TĐT", "Văn bản đề nghị khoanh tiền thuế nợ", "Xử lý nợ thuế", "Điều 84", "Người nộp thuế thuộc diện giải thể, phá sản, bỏ trốn"),
    (10, "Mẫu số 01/XN-TĐT", "Hồ sơ đề nghị xóa nợ tiền thuế, tiền chậm nộp, tiền phạt", "Xử lý nợ thuế", "Điều 85", "Cơ quan thuế thẩm định xóa nợ không thu hồi được"),
    (11, "Mẫu số 01/NDN-TĐT", "Văn bản đề nghị nộp dần tiền thuế nợ có bảo lãnh ngân hàng", "Nộp dần nợ thuế", "Điều 86", "Người nộp thuế có bảo lãnh thanh toán của TCTD"),
    (12, "Mẫu số 01/TMĐT-KT", "Tờ khai khấu trừ, nộp thay thuế của Chủ quản sàn TMĐT", "Thương mại điện tử", "Điều 33", "Sàn Shopee, TikTok Shop, Lazada, Tiki...")
]

row_idx = 4
for item in forms_data:
    stt_val, code_val, name_val, group_val, ref_val, user_val = item
    ws3.cell(row=row_idx, column=1, value=stt_val).alignment = align_center
    ws3.cell(row=row_idx, column=2, value=code_val).alignment = align_center
    ws3.cell(row=row_idx, column=3, value=name_val).alignment = align_left
    ws3.cell(row=row_idx, column=4, value=group_val).alignment = align_left
    ws3.cell(row=row_idx, column=5, value=ref_val).alignment = align_center
    ws3.cell(row=row_idx, column=6, value=user_val).alignment = align_left

    fill_row = fill_blue_light if stt_val % 2 == 0 else fill_gray_light
    for col in range(1, 7):
        cell = ws3.cell(row=row_idx, column=col)
        cell.font = font_normal
        cell.border = border_all
        cell.fill = fill_row
        if col == 2: cell.font = font_bold
        
    ws3.row_dimensions[row_idx].height = 24
    row_idx += 1

# Auto-fit column widths
for sheet in [ws1, ws2, ws3]:
    for col in sheet.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val = str(cell.value or '')
            if cell.row in [1, 2]: # skip title rows
                continue
            max_len = max(max_len, len(val))
        sheet.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 55)

# Save workbook
excel_path = r'D:\TIKTOK\KKhome - Update VBPL\VBan\Thông tư 89-2026 - Danh mục Biểu mẫu & Thủ tục.xlsx'
wb.save(excel_path)
print(f"Generated Excel workbook: {excel_path}")
