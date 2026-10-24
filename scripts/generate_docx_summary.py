import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load structure
with open(r'D:\TIKTOK\KKhome - Update VBPL\VBan\tt89_structure.json', 'r', encoding='utf-8') as f:
    chapters = json.load(f)

# Load analysis text
with open(r'D:\TIKTOK\KKhome - Update VBPL\VBan\Phân-tích-Thông-tư-89-2026-TT-BTC.md', 'r', encoding='utf-8') as f:
    analysis_text = f.read()

doc = docx.Document()

# Set standard page margins (2cm)
for sec in doc.sections:
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.9)
    sec.right_margin = Inches(0.8)

# Color constants
COLOR_NAVY = RGBColor(30, 58, 138)
COLOR_BLUE = RGBColor(37, 99, 235)
COLOR_GRAY = RGBColor(100, 116, 139)
COLOR_DARK = RGBColor(15, 23, 42)

# Helper function for setting cell shading
def set_cell_background(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

# COVER PAGE / HEADER
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_top1 = p_top.add_run("BỘ TÀI CHÍNH — CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
r_top1.font.name = "Segoe UI"
r_top1.font.size = Pt(11)
r_top1.font.bold = True
r_top1.font.color.rgb = COLOR_GRAY

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(24)
p_title.paragraph_format.space_after = Pt(12)
r_title = p_title.add_run("THÔNG TƯ SỐ 89/2026/TT-BTC\nTOÀN VĂN & BẢN PHÂN TÍCH TỔNG HỢP CHUYÊN SÂU")
r_title.font.name = "Segoe UI"
r_title.font.size = Pt(22)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(28)
r_sub = p_sub.add_run("Quy định chi tiết một số điều của Luật Quản lý thuế số 108/2025/QH15\nvà Nghị định số 252/2026/NĐ-CP của Chính phủ\nHiệu lực thi hành: Từ ngày 01 tháng 7 năm 2026")
r_sub.font.name = "Segoe UI"
r_sub.font.size = Pt(12)
r_sub.font.italic = True
r_sub.font.color.rgb = COLOR_DARK

doc.add_page_break()

# PART 1: ANALYSIS & SUMMARY
h1 = doc.add_heading("PHẦN I: BÁO CÁO PHÂN TÍCH TỔNG HỢP & ĐIỂM MỚI NỔI BẬT", level=1)
h1.paragraph_format.space_before = Pt(12)
h1.paragraph_format.space_after = Pt(14)
for run in h1.runs:
    run.font.name = "Segoe UI"
    run.font.color.rgb = COLOR_NAVY

# Parse markdown analysis lines and add to docx
for line in analysis_text.split('\n'):
    line = line.strip()
    if not line or line.startswith('---'):
        continue
    if line.startswith('# '):
        continue # skip main title
    elif line.startswith('## '):
        h = doc.add_heading(line.replace('## ', ''), level=2)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        for r in h.runs:
            r.font.name = "Segoe UI"
            r.font.color.rgb = COLOR_BLUE
    elif line.startswith('### '):
        h = doc.add_heading(line.replace('### ', ''), level=3)
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        for r in h.runs:
            r.font.name = "Segoe UI"
            r.font.color.rgb = COLOR_NAVY
    elif line.startswith('> '):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        r = p.add_run(line.replace('> ', ''))
        r.font.name = "Segoe UI"
        r.font.size = Pt(10)
        r.font.italic = True
        r.font.color.rgb = COLOR_GRAY
    elif line.startswith('- ') or line.startswith('* '):
        p = doc.add_paragraph(line[2:], style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        for r in p.runs:
            r.font.name = "Segoe UI"
            r.font.size = Pt(10)
    elif line.startswith('|') and '|' in line[1:]:
        # Table row - simplified rendering
        continue
    else:
        p = doc.add_paragraph(line)
        p.paragraph_format.space_after = Pt(6)
        for r in p.runs:
            r.font.name = "Segoe UI"
            r.font.size = Pt(10.5)

doc.add_page_break()

# PART 2: FULL TEXT (101 ARTICLES)
h2_title = doc.add_heading("PHẦN II: TOÀN VĂN THÔNG TƯ SỐ 89/2026/TT-BTC (101 ĐIỀU)", level=1)
h2_title.paragraph_format.space_before = Pt(12)
h2_title.paragraph_format.space_after = Pt(14)
for run in h2_title.runs:
    run.font.name = "Segoe UI"
    run.font.color.rgb = COLOR_NAVY

for c in chapters:
    c_title = c.get('title', '')
    c_sub = c.get('subtitle', '')
    
    if c_title != "Phần mở đầu":
        h_chap = doc.add_heading(f"{c_title}", level=2)
        h_chap.paragraph_format.space_before = Pt(16)
        h_chap.paragraph_format.space_after = Pt(4)
        for r in h_chap.runs:
            r.font.name = "Segoe UI"
            r.font.color.rgb = COLOR_NAVY
        if c_sub:
            p_sub = doc.add_paragraph(c_sub)
            p_sub.paragraph_format.space_after = Pt(10)
            r_csub = p_sub.runs[0]
            r_csub.font.name = "Segoe UI"
            r_csub.font.size = Pt(11)
            r_csub.font.bold = True
            r_csub.font.color.rgb = COLOR_BLUE

    for a in c.get('articles', []):
        art_title = a.get('title', '')
        art_paragraphs = a.get('paragraphs', [])
        
        h_art = doc.add_heading(art_title, level=3)
        h_art.paragraph_format.space_before = Pt(12)
        h_art.paragraph_format.space_after = Pt(4)
        for r in h_art.runs:
            r.font.name = "Segoe UI"
            r.font.color.rgb = COLOR_DARK
            r.font.bold = True
            
        for p_text in art_paragraphs:
            p = doc.add_paragraph(p_text)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = "Segoe UI"
                r.font.size = Pt(10)

output_docx_path = r'D:\TIKTOK\KKhome - Update VBPL\VBan\Thông tư 89-2026 - Tổng hợp & Phân tích.docx'
doc.save(output_docx_path)
print(f"Generated DOCX document: {output_docx_path}")
