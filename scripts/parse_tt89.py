import zipfile
import xml.etree.ElementTree as ET
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r'D:\TIKTOK\KKhome - Update VBPL\VBan\Thông tư 89-2026.docx'

with zipfile.ZipFile(docx_path) as z:
    xml_content = z.read('word/document.xml')

tree = ET.fromstring(xml_content)

paragraphs = []
for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    text = ''.join(node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text).strip()
    if text:
        paragraphs.append(text)

print(f'Total paragraphs extracted: {len(paragraphs)}')

doc_structure = []
current_chapter = {'title': 'Phần mở đầu', 'subtitle': '', 'articles': []}
current_article = {'number': 0, 'title': 'Lời mở đầu', 'paragraphs': []}

for p in paragraphs:
    if re.match(r'^Chương\s+[IVXLCDM]+', p, re.I):
        if current_article['paragraphs'] or current_article['title']:
            current_chapter['articles'].append(current_article)
            current_article = {'number': 0, 'title': '', 'paragraphs': []}
        if current_chapter['articles']:
            doc_structure.append(current_chapter)
        current_chapter = {'title': p, 'subtitle': '', 'articles': []}
    elif not current_chapter['subtitle'] and current_chapter['title'] != 'Phần mở đầu' and not current_chapter['articles'] and not p.startswith('Điều '):
        current_chapter['subtitle'] = p
    elif re.match(r'^Điều\s+\d+\.', p, re.I):
        if current_article['title'] or current_article['paragraphs']:
            current_chapter['articles'].append(current_article)
        m = re.match(r'^Điều\s+(\d+)\.\s*(.*)', p, re.I)
        art_num = int(m.group(1)) if m else 0
        current_article = {'number': art_num, 'title': p, 'paragraphs': []}
    else:
        current_article['paragraphs'].append(p)

if current_article['title'] or current_article['paragraphs']:
    current_chapter['articles'].append(current_article)
if current_chapter['articles']:
    doc_structure.append(current_chapter)

print(f'Total chapters: {len(doc_structure)}')
total_articles = 0
for idx, c in enumerate(doc_structure):
    arts = c['articles']
    total_articles += len(arts)
    print(f"{c['title']} ({c.get('subtitle', '')}): {len(arts)} articles")

print(f'Total articles counted: {total_articles}')

with open(r'D:\TIKTOK\KKhome - Update VBPL\VBan\tt89_structure.json', 'w', encoding='utf-8') as f:
    json.dump(doc_structure, f, ensure_ascii=False, indent=2)

print('Saved structure to tt89_structure.json')
