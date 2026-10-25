import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

json_path = r'D:\TIKTOK\KKhome - Update VBPL\VBan\tt89_structure.json'
with open(json_path, 'r', encoding='utf-8') as f:
    chapters = json.load(f)

print(f"Loaded {len(chapters)} chapters.")

# Helper to escape HTML
def esc(s):
    if not s:
        return ""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# Build full-text HTML and search index
search_index = []
articles_list = []

fulltext_html = []

for c_idx, c in enumerate(chapters):
    c_title = c.get('title', '')
    c_sub = c.get('subtitle', '')
    c_id = f"chap-{c_idx}"
    
    fulltext_html.append(f'<div class="chapter-block" id="{c_id}">')
    if c_title != "Phần mở đầu":
        fulltext_html.append(f'<div class="chapter-header">')
        fulltext_html.append(f'<div class="chapter-badge">CHƯƠNG</div>')
        fulltext_html.append(f'<h2 class="chapter-title">{esc(c_title)}</h2>')
        if c_sub:
            fulltext_html.append(f'<div class="chapter-subtitle">{esc(c_sub)}</div>')
        fulltext_html.append(f'</div>')
    
    for a in c.get('articles', []):
        art_num = a.get('number', 0)
        art_title = a.get('title', '')
        art_paragraphs = a.get('paragraphs', [])
        
        art_id = f"dieu-{art_num}" if art_num > 0 else f"intro-{c_idx}"
        
        articles_list.append({
            'id': art_id,
            'num': art_num,
            'title': art_title,
            'chapter': c_title,
            'chapter_sub': c_sub
        })
        
        # Add to search index
        full_text_content = " ".join(art_paragraphs)
        search_index.append({
            'id': art_id,
            'title': art_title,
            'chapter': c_title,
            'text': full_text_content
        })
        
        fulltext_html.append(f'<article class="article-card" id="{art_id}" data-num="{art_num}">')
        fulltext_html.append(f'<div class="article-card-header">')
        fulltext_html.append(f'<div class="article-meta">')
        if art_num > 0:
            fulltext_html.append(f'<span class="badge-art">ĐIỀU {art_num}</span>')
        fulltext_html.append(f'<span class="badge-chap">{esc(c_title)}</span>')
        fulltext_html.append(f'</div>')
        fulltext_html.append(f'<h3 class="article-title">{esc(art_title)}</h3>')
        fulltext_html.append(f'<div class="article-actions">')
        fulltext_html.append(f'<button class="action-btn" onclick="copyLink(\'{art_id}\')" title="Sao chép liên kết điều này"><i class="fa-regular fa-copy"></i> Sao chép</button>')
        fulltext_html.append(f'</div>')
        fulltext_html.append(f'</div>')
        
        fulltext_html.append(f'<div class="article-body">')
        for p in art_paragraphs:
            p_clean = esc(p)
            # Detect numbered point like 1. 2. 3.
            if re.match(r'^\d+\.\s', p):
                fulltext_html.append(f'<p class="p-clause"><strong>{p_clean[:3]}</strong>{p_clean[3:]}</p>')
            # Detect sub-point like a) b) c)
            elif re.match(r'^[a-zđ]\)\s', p):
                fulltext_html.append(f'<p class="p-point"><strong>{p_clean[:3]}</strong>{p_clean[3:]}</p>')
            # Detect sub-sub point like a.1, b.1
            elif re.match(r'^[a-zđ]\.\d+\)\s|^[a-zđ]\.\d+\s', p):
                fulltext_html.append(f'<p class="p-subpoint">{p_clean}</p>')
            else:
                fulltext_html.append(f'<p class="p-text">{p_clean}</p>')
        fulltext_html.append(f'</div>')
        fulltext_html.append(f'</article>')
    
    fulltext_html.append(f'</div>')

fulltext_html_str = "\n".join(fulltext_html)

# Build Sidebar Navigation Items
nav_items_html = []
for c_idx, c in enumerate(chapters):
    c_title = c.get('title', '')
    c_sub = c.get('subtitle', '')
    arts = c.get('articles', [])
    if not arts:
        continue
    
    c_id = f"nav-c-{c_idx}"
    nav_items_html.append(f'<div class="nav-chapter-group" id="{c_id}">')
    nav_items_html.append(f'<div class="nav-chapter-header" onclick="toggleChapter(\'{c_id}\')">')
    nav_items_html.append(f'<i class="fa-solid fa-chevron-down nav-caret"></i>')
    nav_items_html.append(f'<span class="nav-chapter-title">{esc(c_title)}</span>')
    nav_items_html.append(f'<span class="nav-count">{len(arts)}</span>')
    nav_items_html.append(f'</div>')
    
    nav_items_html.append(f'<div class="nav-article-list">')
    for a in arts:
        num = a.get('number', 0)
        title = a.get('title', '')
        art_id = f"dieu-{num}" if num > 0 else f"intro-{c_idx}"
        label = f"Điều {num}" if num > 0 else "Lời mở đầu"
        short_title = title.replace(f"Điều {num}. ", "").replace(f"Điều {num}.", "") if num > 0 else title
        if len(short_title) > 35:
            short_title = short_title[:35] + "..."
            
        nav_items_html.append(f'<a href="#{art_id}" class="nav-article-item" id="nav-item-{art_id}" onclick="selectArticle(\'{art_id}\')">')
        nav_items_html.append(f'<span class="nav-art-tag">{label}</span>')
        nav_items_html.append(f'<span class="nav-art-name">{esc(short_title)}</span>')
        nav_items_html.append(f'</a>')
    nav_items_html.append(f'</div>')
    nav_items_html.append(f'</div>')

nav_html_str = "\n".join(nav_items_html)

# Read Markdown analysis file to include in Analysis Tab
analysis_md_path = r'D:\TIKTOK\KKhome - Update VBPL\VBan\Phân-tích-Thông-tư-89-2026-TT-BTC.md'
with open(analysis_md_path, 'r', encoding='utf-8') as f:
    analysis_text = f.read()

# Generate the complete HTML
html_template = f'''<!DOCTYPE html>
<html lang="vi" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tra Cứu Thông Tư 89/2026/TT-BTC - Luật Quản Lý Thuế</title>
  <meta name="description" content="Hệ thống tra cứu điện tử và phân tích chuyên sâu Thông tư số 89/2026/TT-BTC của Bộ Tài chính hướng dẫn Luật Quản lý thuế số 108/2025/QH15 và Nghị định số 252/2026/NĐ-CP.">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

  <style>
    :root {{
      --primary: #2563eb;
      --primary-dark: #1d4ed8;
      --primary-light: #eff6ff;
      --accent: #0ea5e9;
      --bg: #f8fafc;
      --surface: #ffffff;
      --surface-2: #f1f5f9;
      --border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #64748b;
      --text-soft: #94a3b8;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --sidebar-w: 330px;
      --header-h: 68px;
      --radius: 12px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);
      --font: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    [data-theme="dark"] {{
      --bg: #0b1120;
      --surface: #131c31;
      --surface-2: #1e293b;
      --border: #24324d;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-soft: #64748b;
      --primary-light: #1e3a8a33;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.5);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    /* HEADER */
    .app-header {{
      height: var(--header-h);
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 50;
      box-shadow: var(--shadow-sm);
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .btn-toggle-sidebar {{
      display: none;
      background: none;
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 8px;
      width: 36px;
      height: 36px;
      font-size: 15px;
      cursor: pointer;
    }}

    .brand-logo {{
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: linear-gradient(135deg, #1e40af, #3b82f6);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 14px;
      letter-spacing: -0.5px;
      box-shadow: 0 2px 8px rgba(37,99,235,0.35);
    }}

    .brand-info {{
      display: flex;
      flex-direction: column;
    }}

    .brand-title {{
      font-size: 16px;
      font-weight: 800;
      letter-spacing: -0.3px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .badge-status {{
      font-size: 11px;
      font-weight: 700;
      background: #10b98118;
      color: #10b981;
      border: 1px solid #10b98140;
      border-radius: 20px;
      padding: 2px 9px;
    }}

    .brand-sub {{
      font-size: 12px;
      color: var(--text-muted);
      white-space: nowrap;
    }}

    /* SEARCH BAR */
    .header-center {{
      flex: 1;
      max-width: 520px;
      margin: 0 24px;
      position: relative;
    }}

    .search-input-wrap {{
      position: relative;
      width: 100%;
    }}

    .search-input-wrap i.search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 14px;
    }}

    .search-input {{
      width: 100%;
      height: 40px;
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 0 44px 0 38px;
      font-size: 13.5px;
      color: var(--text);
      font-family: var(--font);
      outline: none;
      transition: all 0.2s;
    }}

    .search-input:focus {{
      background: var(--surface);
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(37,99,235,0.15);
    }}

    .kbd-shortcut {{
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 11px;
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 1px 6px;
      border-radius: 4px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    /* NAV TABS */
    .header-right {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .nav-tabs {{
      display: flex;
      background: var(--surface-2);
      padding: 3px;
      border-radius: 10px;
      gap: 2px;
    }}

    .tab-btn {{
      background: transparent;
      border: none;
      font-family: var(--font);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      padding: 7px 14px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }}

    .tab-btn:hover {{
      color: var(--text);
    }}

    .tab-btn.active {{
      background: var(--surface);
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }}

    .tool-btn {{
      background: none;
      border: 1px solid var(--border);
      border-radius: 8px;
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 14px;
      transition: all 0.15s;
    }}

    .tool-btn:hover {{
      color: var(--text);
      background: var(--surface-2);
    }}

    /* MAIN APP LAYOUT */
    .app-main {{
      flex: 1;
      display: flex;
      overflow: hidden;
    }}

    /* SIDEBAR */
    .app-sidebar {{
      width: var(--sidebar-w);
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      overflow: hidden;
      transition: transform 0.25s ease;
    }}

    .sidebar-filter-box {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      background: var(--surface-2);
    }}

    .sidebar-filter-input {{
      width: 100%;
      height: 34px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      padding: 0 12px;
      font-size: 12.5px;
      color: var(--text);
      outline: none;
      font-family: var(--font);
    }}

    .sidebar-nav-tree {{
      flex: 1;
      overflow-y: auto;
      padding: 8px 10px;
    }}

    .sidebar-nav-tree::-webkit-scrollbar {{
      width: 5px;
    }}
    .sidebar-nav-tree::-webkit-scrollbar-thumb {{
      background: var(--border);
      border-radius: 4px;
    }}

    .nav-chapter-group {{
      margin-bottom: 6px;
    }}

    .nav-chapter-header {{
      display: flex;
      align-items: center;
      padding: 8px 10px;
      border-radius: 8px;
      cursor: pointer;
      user-select: none;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      transition: all 0.15s;
    }}

    .nav-chapter-header:hover {{
      background: var(--surface-2);
      color: var(--primary);
    }}

    .nav-caret {{
      font-size: 10px;
      margin-right: 8px;
      transition: transform 0.2s;
    }}

    .nav-chapter-group.collapsed .nav-caret {{
      transform: rotate(-90deg);
    }}

    .nav-chapter-group.collapsed .nav-article-list {{
      display: none;
    }}

    .nav-chapter-title {{
      flex: 1;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}

    .nav-count {{
      font-size: 10.5px;
      background: var(--surface-2);
      padding: 1px 6px;
      border-radius: 10px;
      color: var(--text-soft);
    }}

    .nav-article-list {{
      margin-left: 12px;
      padding-left: 8px;
      border-left: 1.5px solid var(--border);
      margin-top: 2px;
      display: flex;
      flex-direction: column;
      gap: 1px;
    }}

    .nav-article-item {{
      display: flex;
      align-items: baseline;
      gap: 8px;
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 12.5px;
      color: var(--text-muted);
      text-decoration: none;
      transition: all 0.15s;
      line-height: 1.35;
    }}

    .nav-article-item:hover {{
      background: var(--surface-2);
      color: var(--text);
    }}

    .nav-article-item.active {{
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 600;
    }}

    .nav-art-tag {{
      font-weight: 700;
      font-size: 11.5px;
      color: var(--primary);
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .nav-art-name {{
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    /* CONTENT VIEW */
    .app-content {{
      flex: 1;
      overflow-y: auto;
      padding: 30px 48px 100px;
      background: var(--bg);
    }}

    .app-content::-webkit-scrollbar {{
      width: 8px;
    }}
    .app-content::-webkit-scrollbar-thumb {{
      background: var(--border);
      border-radius: 4px;
    }}

    .content-container {{
      max-width: 960px;
      margin: 0 auto;
    }}

    /* HERO BANNER */
    .doc-hero {{
      background: linear-gradient(135deg, #1e3a8a, #2563eb);
      color: #fff;
      border-radius: var(--radius);
      padding: 32px;
      margin-bottom: 28px;
      box-shadow: var(--shadow-md);
      position: relative;
      overflow: hidden;
    }}

    .doc-hero::after {{
      content: "";
      position: absolute;
      top: -50px;
      right: -50px;
      width: 200px;
      height: 200px;
      background: rgba(255,255,255,0.06);
      border-radius: 50%;
      pointer-events: none;
    }}

    .hero-tag-row {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }}

    .hero-tag {{
      font-size: 11.5px;
      font-weight: 700;
      background: rgba(255,255,255,0.18);
      border: 1px solid rgba(255,255,255,0.25);
      border-radius: 20px;
      padding: 3px 12px;
      backdrop-filter: blur(4px);
    }}

    .hero-title {{
      font-size: 26px;
      font-weight: 800;
      line-height: 1.3;
      margin-bottom: 8px;
    }}

    .hero-desc {{
      font-size: 14.5px;
      opacity: 0.9;
      max-width: 800px;
      margin-bottom: 20px;
    }}

    .hero-metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 12px;
    }}

    .metric-card {{
      background: rgba(0,0,0,0.18);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 10px;
      padding: 10px 14px;
    }}

    .metric-val {{
      font-size: 22px;
      font-weight: 800;
      color: #fff;
    }}

    .metric-lab {{
      font-size: 11.5px;
      opacity: 0.8;
    }}

    /* CHAPTER BLOCK */
    .chapter-block {{
      margin-bottom: 40px;
    }}

    .chapter-header {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 4px solid var(--primary);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin-bottom: 16px;
      box-shadow: var(--shadow-sm);
    }}

    .chapter-badge {{
      font-size: 11px;
      font-weight: 800;
      color: var(--primary);
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 2px;
    }}

    .chapter-title {{
      font-size: 18px;
      font-weight: 800;
      color: var(--text);
    }}

    .chapter-subtitle {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* ARTICLE CARD */
    .article-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px 24px;
      margin-bottom: 16px;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
    }}

    .article-card:hover {{
      border-color: #cbd5e1;
      box-shadow: var(--shadow-md);
    }}

    .article-card.highlight-target {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(37,99,235,0.2);
    }}

    .article-card-header {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 14px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }}

    .article-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
    }}

    .badge-art {{
      font-size: 11px;
      font-weight: 800;
      background: var(--primary-light);
      color: var(--primary);
      border-radius: 6px;
      padding: 2px 8px;
    }}

    .badge-chap {{
      color: var(--text-soft);
      font-weight: 600;
    }}

    .article-title {{
      font-size: 17px;
      font-weight: 800;
      color: var(--text);
      line-height: 1.35;
    }}

    .article-actions {{
      display: flex;
      justify-content: flex-end;
      gap: 6px;
      margin-top: -24px;
    }}

    .action-btn {{
      background: none;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 4px 10px;
      font-size: 11.5px;
      color: var(--text-muted);
      cursor: pointer;
      font-family: var(--font);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    .action-btn:hover {{
      background: var(--surface-2);
      color: var(--text);
    }}

    .article-body p {{
      margin-bottom: 10px;
      font-size: 14px;
      color: var(--text);
      line-height: 1.65;
    }}

    .article-body p:last-child {{
      margin-bottom: 0;
    }}

    .p-clause {{
      margin-top: 12px;
      font-weight: 500;
    }}

    .p-point {{
      margin-left: 18px;
      color: var(--text);
    }}

    .p-subpoint {{
      margin-left: 36px;
      color: var(--text-muted);
      font-size: 13.5px;
    }}

    /* TAB PANELS */
    .tab-panel {{
      display: none;
    }}
    .tab-panel.active {{
      display: block;
    }}

    /* MARKDOWN CONTAINER */
    .markdown-container {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 36px 40px;
      box-shadow: var(--shadow-sm);
    }}

    .markdown-container h1 {{
      font-size: 26px;
      font-weight: 800;
      margin-bottom: 16px;
      color: var(--text);
      border-bottom: 2px solid var(--border);
      padding-bottom: 12px;
    }}

    .markdown-container h2 {{
      font-size: 20px;
      font-weight: 800;
      margin-top: 32px;
      margin-bottom: 14px;
      color: var(--primary);
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
    }}

    .markdown-container h3 {{
      font-size: 16px;
      font-weight: 700;
      margin-top: 20px;
      margin-bottom: 10px;
      color: var(--text);
    }}

    .markdown-container p {{
      font-size: 14px;
      line-height: 1.7;
      margin-bottom: 12px;
      color: var(--text);
    }}

    .markdown-container ul, .markdown-container ol {{
      margin-left: 24px;
      margin-bottom: 14px;
      font-size: 14px;
    }}

    .markdown-container li {{
      margin-bottom: 6px;
      line-height: 1.6;
    }}

    .markdown-container blockquote {{
      border-left: 4px solid var(--primary);
      background: var(--surface-2);
      padding: 14px 18px;
      border-radius: 0 8px 8px 0;
      margin: 16px 0;
      font-size: 13.5px;
      color: var(--text);
    }}

    .markdown-container table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 13px;
    }}

    .markdown-container th, .markdown-container td {{
      border: 1px solid var(--border);
      padding: 10px 14px;
      text-align: left;
    }}

    .markdown-container th {{
      background: var(--surface-2);
      font-weight: 700;
      color: var(--text);
    }}

    .markdown-container tr:nth-child(even) td {{
      background: rgba(0,0,0,0.01);
    }}

    /* SEARCH POPUP MODAL */
    .search-modal {{
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 100;
      display: none;
      align-items: flex-start;
      justify-content: center;
      padding-top: 80px;
    }}

    .search-modal.active {{
      display: flex;
    }}

    .search-dialog {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      width: 90%;
      max-width: 640px;
      box-shadow: var(--shadow-lg);
      display: flex;
      flex-direction: column;
      max-height: 80vh;
      overflow: hidden;
      animation: modalSlide 0.15s ease-out;
    }}

    @keyframes modalSlide {{
      from {{ opacity: 0; transform: translateY(-10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .search-dialog-header {{
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .search-modal-input {{
      flex: 1;
      height: 38px;
      border: none;
      background: none;
      font-size: 15px;
      font-family: var(--font);
      color: var(--text);
      outline: none;
    }}

    .search-results-list {{
      flex: 1;
      overflow-y: auto;
      padding: 8px 12px;
    }}

    .sr-item {{
      padding: 10px 14px;
      border-radius: 8px;
      cursor: pointer;
      border-bottom: 1px solid var(--border);
      transition: background 0.15s;
    }}

    .sr-item:last-child {{
      border-bottom: none;
    }}

    .sr-item:hover, .sr-item.selected {{
      background: var(--surface-2);
    }}

    .sr-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3px;
    }}

    .sr-title {{
      font-size: 13.5px;
      font-weight: 700;
      color: var(--primary);
    }}

    .sr-chap {{
      font-size: 11px;
      color: var(--text-soft);
    }}

    .sr-snippet {{
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.45;
    }}

    mark {{
      background: #fef08a;
      color: #713f12;
      padding: 0 2px;
      border-radius: 2px;
      font-weight: 700;
    }}

    /* COMPARISON TABLE */
    .compare-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
    }}

    .compare-title {{
      font-size: 18px;
      font-weight: 800;
      margin-bottom: 8px;
      color: var(--text);
    }}

    .compare-tag {{
      display: inline-block;
      font-size: 11px;
      font-weight: 700;
      background: #eff6ff;
      color: #2563eb;
      padding: 2px 8px;
      border-radius: 4px;
      margin-bottom: 14px;
    }}

    .compare-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }}

    .compare-col {{
      padding: 14px 16px;
      border-radius: 8px;
      font-size: 13px;
    }}

    .compare-col.old {{
      background: #fee2e225;
      border: 1px solid #fca5a540;
    }}

    .compare-col.new {{
      background: #dcfce725;
      border: 1px solid #86efac40;
    }}

    .col-label {{
      font-weight: 800;
      font-size: 12px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .compare-col.old .col-label {{ color: #dc2626; }}
    .compare-col.new .col-label {{ color: #16a34a; }}

    /* TOAST */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #0f172a;
      color: #fff;
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      box-shadow: var(--shadow-lg);
      z-index: 200;
      display: none;
      align-items: center;
      gap: 8px;
    }}

    /* RESPONSIVE */
    @media (max-width: 900px) {{
      .btn-toggle-sidebar {{ display: inline-flex; align-items: center; justify-content: center; }}
      .app-sidebar {{
        position: fixed;
        left: 0; top: var(--header-h); bottom: 0;
        z-index: 40;
        transform: translateX(-100%);
      }}
      .app-sidebar.open {{
        transform: translateX(0);
        box-shadow: var(--shadow-lg);
      }}
      .app-content {{
        padding: 20px 16px 80px;
      }}
      .header-center {{
        display: none;
      }}
    }}
  </style>
</head>
<body>

  <!-- APP HEADER -->
  <header class="app-header">
    <div class="header-left">
      <button class="btn-toggle-sidebar" id="btnToggleSidebar" onclick="toggleMobileSidebar()">
        <i class="fa-solid fa-bars"></i>
      </button>
      <div class="brand-logo">89</div>
      <div class="brand-info">
        <div class="brand-title">
          <span>Thông tư 89/2026/TT-BTC</span>
          <span class="badge-status">Hiệu lực: 01/07/2026</span>
        </div>
        <div class="brand-sub">Bộ Tài chính • Quy định chi tiết Luật Quản lý thuế số 108/2025/QH15 & NĐ 252/2026/NĐ-CP</div>
      </div>
    </div>

    <!-- QUICK SEARCH TRIGGER -->
    <div class="header-center">
      <div class="search-input-wrap" onclick="openSearchModal()">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input type="text" class="search-input" placeholder="Tìm kiếm nhanh điều khoản, sắc thuế, từ khóa..." readonly>
        <span class="kbd-shortcut">Ctrl K</span>
      </div>
    </div>

    <!-- NAV TABS & TOOLS -->
    <div class="header-right">
      <div class="nav-tabs">
        <button class="tab-btn active" id="tabBtnFulltext" onclick="switchTab('fulltext')">
          <i class="fa-solid fa-book-open"></i> Toàn văn (101 Điều)
        </button>
        <button class="tab-btn" id="tabBtnAnalysis" onclick="switchTab('analysis')">
          <i class="fa-solid fa-chart-pie"></i> Phân tích chuyên sâu
        </button>
        <button class="tab-btn" id="tabBtnCompare" onclick="switchTab('compare')">
          <i class="fa-solid fa-code-compare"></i> Điểm mới nổi bật
        </button>
      </div>

      <button class="tool-btn" onclick="toggleTheme()" title="Đổi giao diện sáng/tối" id="btnTheme">
        <i class="fa-solid fa-moon"></i>
      </button>
      <button class="tool-btn" onclick="window.print()" title="In văn bản">
        <i class="fa-solid fa-print"></i>
      </button>
    </div>
  </header>

  <!-- APP MAIN -->
  <main class="app-main">

    <!-- SIDEBAR NAVIGATION -->
    <aside class="app-sidebar" id="appSidebar">
      <div class="sidebar-filter-box">
        <input type="text" class="sidebar-filter-input" id="sidebarFilterInput" placeholder="🔍 Lọc số điều hoặc từ khóa..." oninput="filterSidebarArticles(this.value)">
      </div>
      <div class="sidebar-nav-tree" id="sidebarNavTree">
        {nav_html_str}
      </div>
    </aside>

    <!-- CONTENT WRAPPER -->
    <section class="app-content" id="appContent">
      <div class="content-container">

        <!-- TAB 1: FULL TEXT (101 ARTICLES) -->
        <div class="tab-panel active" id="panelFulltext">
          <!-- HERO BANNER -->
          <div class="doc-hero">
            <div class="hero-tag-row">
              <span class="hero-tag"><i class="fa-solid fa-landmark"></i> Bộ Tài chính</span>
              <span class="hero-tag"><i class="fa-solid fa-calendar-check"></i> Ban hành: 30/06/2026</span>
              <span class="hero-tag"><i class="fa-solid fa-bolt"></i> Hiệu lực: 01/07/2026</span>
            </div>
            <h1 class="hero-title">Thông tư số 89/2026/TT-BTC</h1>
            <p class="hero-desc">Quy định chi tiết một số điều của Luật Quản lý thuế số 108/2025/QH15 và Nghị định số 252/2026/NĐ-CP của Chính phủ về giao dịch điện tử, khai nộp thuế, hoàn thuế, miễn giảm thuế và thương mại điện tử.</p>
            <div class="hero-metrics">
              <div class="metric-card">
                <div class="metric-val">10</div>
                <div class="metric-lab">Chương điều chỉnh</div>
              </div>
              <div class="metric-card">
                <div class="metric-val">101</div>
                <div class="metric-lab">Điều khoản chính thức</div>
              </div>
              <div class="metric-card">
                <div class="metric-val">10+</div>
                <div class="metric-lab">Sắc thuế quy định</div>
              </div>
              <div class="metric-card">
                <div class="metric-val">100%</div>
                <div class="metric-lab">Điện tử hóa quy trình</div>
              </div>
            </div>

            <!-- ACTION DOWNLOAD BUTTONS -->
            <div class="hero-actions-row" style="margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap;">
              <a href="./VBan/Th%C3%B4ng%20t%C6%B0%2089-2026/Th%C3%B4ng%20t%C6%B0%2089-2026%20-%20T%E1%BB%95ng%20h%E1%BB%A3p%20&%20Ph%C3%A2n%20t%C3%ADch.docx" download class="btn-hero-action" style="background:#ffffff; color:#1e3a8a; padding:9px 16px; border-radius:8px; font-weight:700; font-size:12.5px; text-decoration:none; display:inline-flex; align-items:center; gap:6px; box-shadow:0 2px 6px rgba(0,0,0,0.15);">
                <i class="fa-solid fa-file-word" style="color:#2563eb;"></i> Tải Bản Word (.docx)
              </a>
              <a href="./VBan/Th%C3%B4ng%20t%C6%B0%2089-2026/Th%C3%B4ng%20t%C6%B0%2089-2026%20-%20Danh%20m%E1%BB%A5c%20Bi%E1%BB%83u%20m%E1%BA%ABu%20&%20Th%E1%BB%A7%20t%E1%BB%A5c.xlsx" download class="btn-hero-action" style="background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3); color:#ffffff; padding:9px 16px; border-radius:8px; font-weight:700; font-size:12.5px; text-decoration:none; display:inline-flex; align-items:center; gap:6px; backdrop-filter:blur(4px);">
                <i class="fa-solid fa-file-excel" style="color:#4ade80;"></i> Tải Danh mục Mẫu biểu (.xlsx)
              </a>
              <a href="./VBan/Th%C3%B4ng%20t%C6%B0%2089-2026/Ph%C3%A2n-t%C3%ADch-Th%C3%B4ng-t%C6%B0-89-2026.md" download class="btn-hero-action" style="background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3); color:#ffffff; padding:9px 16px; border-radius:8px; font-weight:700; font-size:12.5px; text-decoration:none; display:inline-flex; align-items:center; gap:6px; backdrop-filter:blur(4px);">
                <i class="fa-solid fa-file-lines" style="color:#fbbf24;"></i> Xem Bản Markdown (.md)
              </a>
            </div>
          </div>

          <!-- FULL ARTICLES LIST -->
          <div class="articles-container" id="articlesContainer">
            {fulltext_html_str}
          </div>
        </div>

        <!-- TAB 2: MARKDOWN ANALYSIS -->
        <div class="tab-panel" id="panelAnalysis">
          <div class="markdown-container" id="markdownRenderBox">
            <!-- Rendered by marked.js on client -->
          </div>
        </div>

        <!-- TAB 3: KEY CHANGES & COMPARISON -->
        <div class="tab-panel" id="panelCompare">
          <div class="markdown-container" style="margin-bottom: 24px;">
            <h1 style="border:none; margin-bottom: 6px;">Bảng Đối Chiếu Các Điểm Mới Cốt Lõi</h1>
            <p style="color:var(--text-muted); margin-bottom: 24px;">Tổng hợp những thay đổi mang tính bước ngoặt giữa Thông tư 89/2026/TT-BTC và các thông tư quản lý thuế trước đây.</p>
            
            <div class="compare-card">
              <div class="compare-title">1. Trách nhiệm khấu trừ và nộp thay thuế của Sàn TMĐT (Shopee, TikTok Shop, Lazada...)</div>
              <div class="compare-tag">Điều 33 Thông tư 89/2026/TT-BTC</div>
              <div class="compare-grid">
                <div class="compare-col old">
                  <div class="col-label"><i class="fa-solid fa-circle-xmark"></i> Quy định cũ (TT 80/2021 & TT 92/2015)</div>
                  <p>Chủ sàn chỉ có trách nhiệm cung cấp định kỳ thông tin dữ liệu doanh thu của người bán cho cơ quan thuế. Cá nhân, hộ kinh doanh trên sàn phải tự đi đăng ký, kê khai và nộp thuế.</p>
                </div>
                <div class="compare-col new">
                  <div class="col-label"><i class="fa-solid fa-circle-check"></i> Quy định mới (Thông tư 89/2026)</div>
                  <p><strong>Chủ quản nền tảng TMĐT trực tiếp khấu trừ, kê khai và nộp thay</strong> số thuế phải nộp đối với từng giao dịch của cá nhân/hộ kinh doanh bán hàng trên sàn vào NSNN.</p>
                </div>
              </div>
            </div>

            <div class="compare-card">
              <div class="compare-title">2. Xử lý sự cố mạng vào ngày hạn chót nộp tờ khai và nộp thuế</div>
              <div class="compare-tag">Điều 12 Thông tư 89/2026/TT-BTC</div>
              <div class="compare-grid">
                <div class="compare-col old">
                  <div class="col-label"><i class="fa-solid fa-circle-xmark"></i> Quy định cũ (TT 19/2021)</div>
                  <p>Doanh nghiệp phải chủ động chứng minh hệ thống mạng bị nghẽn, làm thủ tục xin xác nhận phức tạp từ cơ quan thuế hoặc nhà mạng để tránh bị phạt chậm nộp.</p>
                </div>
                <div class="compare-col new">
                  <div class="col-label"><i class="fa-solid fa-circle-check"></i> Quy định mới (Thông tư 89/2026)</div>
                  <p>Cơ quan thuế công khai thời điểm sự cố. Thời hạn nộp hồ sơ, nộp thuế của NNT <strong>tự động được gia hạn sang ngày làm việc tiếp theo</strong> sau khi hệ thống hoạt động trở lại bình thường.</p>
                </div>
              </div>
            </div>

            <div class="compare-card">
              <div class="compare-title">3. Kiểm tra thuế trực tuyến, từ xa trên cơ sở dữ liệu số lớn</div>
              <div class="compare-tag">Điều 89 Thông tư 89/2026/TT-BTC</div>
              <div class="compare-grid">
                <div class="compare-col old">
                  <div class="col-label"><i class="fa-solid fa-circle-xmark"></i> Quy định cũ</div>
                  <p>Chủ yếu thực hiện thanh tra, kiểm tra trực tiếp tại trụ sở doanh nghiệp, yêu cầu in ấn giải trình hồ sơ chứng từ giấy tốn kém chi phí.</p>
                </div>
                <div class="compare-col new">
                  <div class="col-label"><i class="fa-solid fa-circle-check"></i> Quy định mới (Thông tư 89/2026)</div>
                  <p>Chính thức áp dụng <strong>kiểm tra trực tuyến từ xa</strong> thông qua dữ liệu hóa đơn điện tử, truyền nhận dữ liệu số và làm việc trực tuyến, hạn chế tối đa kiểm tra tại chỗ.</p>
                </div>
              </div>
            </div>

            <div class="compare-card">
              <div class="compare-title">4. Quản lý Nhà thầu nước ngoài và Nhà cung cấp nước ngoài (NCCNN)</div>
              <div class="compare-tag">Điều 30, 31 Thông tư 89/2026/TT-BTC (Thay thế TT 103/2014)</div>
              <div class="compare-grid">
                <div class="compare-col old">
                  <div class="col-label"><i class="fa-solid fa-circle-xmark"></i> Quy định cũ (TT 103/2014)</div>
                  <p>Quy trình tính toán phức tạp, doanh nghiệp Việt Nam mua dịch vụ nước ngoài phải tự tính tỷ lệ GTGT và TNDN khấu trừ thủ công gây nhiều rủi ro truy thu.</p>
                </div>
                <div class="compare-col new">
                  <div class="col-label"><i class="fa-solid fa-circle-check"></i> Quy định mới (Thông tư 89/2026)</div>
                  <p>NCCNN kê khai trực tiếp qua Cổng thuế quốc tế; hoặc Ngân hàng/Trung gian thanh toán tự động khấu trừ. Đồng bộ quy trình toàn diện.</p>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>
  </main>

  <!-- SEARCH MODAL -->
  <div class="search-modal" id="searchModal" onclick="handleModalBackdropClick(event)">
    <div class="search-dialog">
      <div class="search-dialog-header">
        <i class="fa-solid fa-magnifying-glass" style="color:var(--primary)"></i>
        <input type="text" class="search-modal-input" id="searchModalInput" placeholder="Nhập số điều (VD: 19, 33) hoặc từ khóa tìm kiếm..." oninput="handleSearch(this.value)">
        <span class="kbd-shortcut" onclick="closeSearchModal()" style="cursor:pointer">ESC</span>
      </div>
      <div class="search-results-list" id="searchResultsList">
        <div style="padding: 24px; text-align: center; color: var(--text-soft); font-size: 13px;">
          Gõ từ khóa để tra cứu tức thì trong 101 Điều của Thông tư 89...
        </div>
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div class="toast" id="toastBox">
    <i class="fa-solid fa-circle-check" style="color:#10b981"></i>
    <span id="toastMsg">Đã sao chép liên kết!</span>
  </div>

  <!-- SCRIPTS -->
  <script>
    const searchData = {json.dumps(search_index, ensure_ascii=False)};
    const rawMarkdown = {json.dumps(analysis_text, ensure_ascii=False)};

    // Initialize Markdown Render
    document.addEventListener("DOMContentLoaded", () => {{
      if (typeof marked !== 'undefined') {{
        document.getElementById('markdownRenderBox').innerHTML = marked.parse(rawMarkdown);
      }}
    }});

    // Tab Switcher
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      
      if (tabId === 'fulltext') {{
        document.getElementById('tabBtnFulltext').classList.add('active');
        document.getElementById('panelFulltext').classList.add('active');
        document.getElementById('appSidebar').style.display = 'flex';
      }} else if (tabId === 'analysis') {{
        document.getElementById('tabBtnAnalysis').classList.add('active');
        document.getElementById('panelAnalysis').classList.add('active');
      }} else if (tabId === 'compare') {{
        document.getElementById('tabBtnCompare').classList.add('active');
        document.getElementById('panelCompare').classList.add('active');
      }}
      document.getElementById('appContent').scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // Sidebar chapter toggle
    function toggleChapter(chapId) {{
      const el = document.getElementById(chapId);
      if (el) el.classList.toggle('collapsed');
    }}

    // Select and navigate to article
    function selectArticle(artId) {{
      switchTab('fulltext');
      document.querySelectorAll('.nav-article-item').forEach(i => i.classList.remove('active'));
      const navItem = document.getElementById('nav-item-' + artId);
      if (navItem) navItem.classList.add('active');

      const target = document.getElementById(artId);
      if (target) {{
        document.querySelectorAll('.article-card').forEach(c => c.classList.remove('highlight-target'));
        target.classList.add('highlight-target');
        target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
      // close mobile sidebar if open
      const sb = document.getElementById('appSidebar');
      if (sb.classList.contains('open')) sb.classList.remove('open');
    }}

    // Filter sidebar list
    function filterSidebarArticles(query) {{
      const q = query.toLowerCase().trim();
      const items = document.querySelectorAll('.nav-article-item');
      items.forEach(item => {{
        const text = item.textContent.toLowerCase();
        if (!q || text.includes(q)) {{
          item.style.display = 'flex';
        }} else {{
          item.style.display = 'none';
        }}
      }});
    }}

    // Search Modal
    function openSearchModal() {{
      const modal = document.getElementById('searchModal');
      modal.classList.add('active');
      const input = document.getElementById('searchModalInput');
      input.focus();
      input.select();
    }}

    function closeSearchModal() {{
      document.getElementById('searchModal').classList.remove('active');
    }}

    function handleModalBackdropClick(e) {{
      if (e.target.id === 'searchModal') closeSearchModal();
    }}

    document.addEventListener('keydown', e => {{
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        openSearchModal();
      }}
      if (e.key === 'Escape') closeSearchModal();
    }});

    // Live Search Execution
    function handleSearch(q) {{
      const query = q.toLowerCase().trim();
      const resultsContainer = document.getElementById('searchResultsList');
      if (!query) {{
        resultsContainer.innerHTML = '<div style="padding: 24px; text-align: center; color: var(--text-soft); font-size: 13px;">Gõ từ khóa để tra cứu tức thì trong 101 Điều của Thông tư 89...</div>';
        return;
      }}

      // Match number directly
      const isNum = !isNaN(query) && parseInt(query) > 0;
      let matches = [];

      for (let item of searchData) {{
        if (isNum && item.title.includes('Điều ' + query + '.')) {{
          matches.unshift(item); // Prioritize direct article number match
        }} else if (item.title.toLowerCase().includes(query) || item.text.toLowerCase().includes(query)) {{
          matches.push(item);
        }}
        if (matches.length >= 25) break;
      }}

      if (matches.length === 0) {{
        resultsContainer.innerHTML = `<div style="padding: 24px; text-align: center; color: var(--text-soft); font-size: 13px;">Không tìm thấy kết quả phù hợp với "<strong>${{escHtml(query)}}</strong>"</div>`;
        return;
      }}

      resultsContainer.innerHTML = matches.map(m => {{
        const snippet = getSnippet(m.text, query);
        return `
          <div class="sr-item" onclick="jumpToResult('${{m.id}}')">
            <div class="sr-head">
              <span class="sr-title">${{highlight(m.title, query)}}</span>
              <span class="sr-chap">${{m.chapter}}</span>
            </div>
            <div class="sr-snippet">${{highlight(snippet, query)}}</div>
          </div>
        `;
      }}).join('');
    }}

    function jumpToResult(artId) {{
      closeSearchModal();
      selectArticle(artId);
    }}

    function highlight(text, q) {{
      if (!q) return text;
      const regex = new RegExp('(' + q.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
      return text.replace(regex, '<mark>$1</mark>');
    }}

    function getSnippet(fullText, q) {{
      const idx = fullText.toLowerCase().indexOf(q);
      if (idx === -1) return fullText.slice(0, 110) + '...';
      const start = Math.max(0, idx - 40);
      const end = Math.min(fullText.length, idx + q.length + 70);
      return (start > 0 ? '...' : '') + fullText.slice(start, end) + (end < fullText.length ? '...' : '');
    }}

    function escHtml(s) {{
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }}

    // Copy link
    function copyLink(artId) {{
      const url = window.location.origin + window.location.pathname + '#' + artId;
      navigator.clipboard.writeText(url).then(() => {{
        showToast('Đã sao chép liên kết điều khoản!');
      }});
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toastBox');
      document.getElementById('toastMsg').innerText = msg;
      toast.style.display = 'flex';
      setTimeout(() => {{
        toast.style.display = 'none';
      }}, 2500);
    }}

    // Theme Toggle
    function toggleTheme() {{
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      document.getElementById('btnTheme').innerHTML = next === 'dark' ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    }}

    // Mobile Sidebar
    function toggleMobileSidebar() {{
      document.getElementById('appSidebar').classList.toggle('open');
    }}
  </script>
</body>
</html>
'''

output_paths = [
    r'D:\TIKTOK\KKhome - Update VBPL\index.html',
    r'D:\TIKTOK\KKhome - Update VBPL\VBan\index.html',
    r'D:\TIKTOK\KKhome - Update VBPL\VBan\Thông tư 89-2026\index.html',
    r'D:\TIKTOK\KKhome - Update VBPL\public\vbpl\thong-tu-89-2026\index.html'
]

for p in output_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Generated successfully: {p} ({len(html_template):,} chars)")

