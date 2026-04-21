"""
app.py  –  Streamlit web app, KHÔNG cần API key
Deploy: push lên GitHub (app.py + teacher_core.py + requirements.txt) -> streamlit.io/cloud
"""
import io
import streamlit as st
import pandas as pd
from teacher_core import (process_data, detect_header_row, find_column,
                           detect_ambiguous_in_data, detect_unknown_subjects,
                           _ALL_CODES)

NIEN_KHOA_OPTIONS = ["2025-2026", "2026-2027", "2027-2028"]

st.set_page_config(page_title="PCCM", page_icon="2️⃣", layout="wide")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════════════
   PCCM – Design System
   Phong cách: Modern-Clean x Retro/Vintage Pastel
   Hỗ trợ đầy đủ Light Mode & Dark Mode
═══════════════════════════════════════════════════════════════════ */

/* ── Google Font (Roboto Mono cho accent retro) ───────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;600&family=Inter:wght@400;500;600;700&display=swap');

/* ── Biến màu – Light Mode ────────────────────────────────────────── */
:root {
  /* Pastel nền & surface */
  --bg-page:          #F2F0EB;          /* kem ấm */
  --bg-card:          #FAFAF7;          /* trắng ngà */
  --bg-card-hover:    #F5F3EE;
  --bg-sidebar:       #EDE9E0;          /* be nhạt */

  /* Chữ – tương phản cao */
  --text-primary:     #1C1A16;          /* nâu than */
  --text-secondary:   #4A4540;          /* nâu trung */
  --text-muted:       #7A736A;          /* xám ấm */
  --text-on-accent:   #FFFFFF;

  /* Accent – Indigo đậm (CTA chính) */
  --accent-cta:       #3D2E8C;          /* indigo đậm */
  --accent-cta-hover: #2E2270;
  --accent-cta-light: rgba(61,46,140,0.10);
  --accent-cta-glow:  rgba(61,46,140,0.28);

  /* Border & divider */
  --border:           #D6D0C4;
  --border-strong:    #B0A898;

  /* Trạng thái */
  --step-bg:          rgba(61,46,140,0.07);
  --step-border:      #3D2E8C;
  --step-text:        #2E2270;

  --success-bg:       rgba(42,130,84,0.09);
  --success-border:   #2A8254;
  --success-text:     #1A5C3A;

  --warn-bg:          rgba(185,105,0,0.09);
  --warn-border:      #B96900;
  --warn-text:        #7A4500;

  /* Card ambig */
  --card-bg:          #FAFAF7;
  --card-border:      #D6D0C4;

  /* Help / sidebar section */
  --help-bg:          rgba(61,46,140,0.05);
  --help-border:      rgba(61,46,140,0.20);

  /* Code inline */
  --code-bg:          rgba(61,46,140,0.08);
  --code-text:        #3D2E8C;

  /* Tags */
  --tag-green-bg:     rgba(42,130,84,0.12);
  --tag-green-fg:     #1A5C3A;
  --tag-blue-bg:      rgba(61,46,140,0.12);
  --tag-blue-fg:      #2E2270;
  --tag-orange-bg:    rgba(185,105,0,0.12);
  --tag-orange-fg:    #7A4500;

  /* Table */
  --table-head-bg:    #EDE9E0;
  --table-border:     #D6D0C4;
  --table-row-alt:    rgba(61,46,140,0.03);

  /* Shadow */
  --shadow-card:      0 2px 10px rgba(28,26,22,0.08), 0 0 0 1px var(--border);
  --shadow-card-hover:0 4px 20px rgba(28,26,22,0.12), 0 0 0 1px var(--border-strong);
}

/* ── Biến màu – Dark Mode ─────────────────────────────────────────── */
[data-theme="dark"] {
  --bg-page:          #141210;
  --bg-card:          #1E1C18;
  --bg-card-hover:    #242218;
  --bg-sidebar:       #191713;

  --text-primary:     #EDE9E0;
  --text-secondary:   #B8B0A4;
  --text-muted:       #7A736A;
  --text-on-accent:   #FFFFFF;

  --accent-cta:       #7B6ECC;
  --accent-cta-hover: #9486D8;
  --accent-cta-light: rgba(123,110,204,0.15);
  --accent-cta-glow:  rgba(123,110,204,0.35);

  --border:           #2E2B24;
  --border-strong:    #3E3A30;

  --step-bg:          rgba(123,110,204,0.13);
  --step-border:      #7B6ECC;
  --step-text:        #C4BAF0;

  --success-bg:       rgba(72,196,130,0.13);
  --success-border:   #48C482;
  --success-text:     #9EEAC4;

  --warn-bg:          rgba(250,170,80,0.13);
  --warn-border:      #FAAA50;
  --warn-text:        #FDDBA0;

  --card-bg:          #1E1C18;
  --card-border:      #2E2B24;

  --help-bg:          rgba(123,110,204,0.08);
  --help-border:      rgba(123,110,204,0.25);

  --code-bg:          rgba(123,110,204,0.15);
  --code-text:        #C4BAF0;

  --tag-green-bg:     rgba(72,196,130,0.18);
  --tag-green-fg:     #9EEAC4;
  --tag-blue-bg:      rgba(123,110,204,0.18);
  --tag-blue-fg:      #C4BAF0;
  --tag-orange-bg:    rgba(250,170,80,0.18);
  --tag-orange-fg:    #FDDBA0;

  --table-head-bg:    #242218;
  --table-border:     #2E2B24;
  --table-row-alt:    rgba(123,110,204,0.05);

  --shadow-card:      0 2px 10px rgba(0,0,0,0.35), 0 0 0 1px var(--border);
  --shadow-card-hover:0 4px 20px rgba(0,0,0,0.50), 0 0 0 1px var(--border-strong);
}

/* ── Base & Typography ────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg-page) !important;
  color: var(--text-primary) !important;
}
[data-testid="stHeader"] {
  background: var(--bg-page) !important;
  border-bottom: 1px solid var(--border);
}
[data-testid="stSidebar"] {
  background: var(--bg-sidebar) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stMainBlockContainer"] {
  background: transparent;
}

/* ── Header Banner ────────────────────────────────────────────────── */
.main-header {
  background: linear-gradient(135deg, var(--accent-cta) 0%, #5C4FBF 100%);
  color: var(--text-on-accent);
  padding: 1.6rem 2rem;
  border-radius: 14px;
  margin-bottom: 1.6rem;
  text-align: center;
  box-shadow: 0 4px 24px var(--accent-cta-glow);
  position: relative;
  overflow: hidden;
}
.main-header::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(
      45deg,
      rgba(255,255,255,0.03) 0px,
      rgba(255,255,255,0.03) 1px,
      transparent 1px,
      transparent 14px
    );
}
.main-header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.main-header p {
  margin: .4rem 0 0;
  opacity: .88;
  font-size: .9rem;
  font-family: 'Roboto Mono', monospace;
  letter-spacing: 0.02em;
}

/* ── Step Cards (bước hướng dẫn) ─────────────────────────────────── */
.step-box {
  background: var(--step-bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--step-border);
  color: var(--step-text);
  padding: .85rem 1.1rem;
  border-radius: 0 10px 10px 0;
  margin-bottom: 1rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  box-shadow: var(--shadow-card);
}

/* ── Trạng thái ───────────────────────────────────────────────────── */
.success-box {
  background: var(--success-bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--success-border);
  color: var(--success-text);
  padding: .85rem 1.1rem;
  border-radius: 0 10px 10px 0;
  font-weight: 500;
}
.warn-box {
  background: var(--warn-bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--warn-border);
  color: var(--warn-text);
  padding: .85rem 1.1rem;
  border-radius: 0 10px 10px 0;
  margin-bottom: 1.2rem;
  font-weight: 500;
}

/* ── Card (ambiguous token) ───────────────────────────────────────── */
.ambig-card {
  background: var(--card-bg);
  border: 1.5px solid var(--warn-border);
  border-radius: 12px;
  padding: 1rem 1.2rem;
  margin-bottom: 1.1rem;
  box-shadow: var(--shadow-card);
  transition: box-shadow .18s ease;
}
.ambig-card:hover {
  box-shadow: var(--shadow-card-hover);
}
.ambig-token {
  font-family: 'Roboto Mono', monospace;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--warn-border);
  letter-spacing: 0.03em;
}
.ambig-ctx {
  font-size: .82rem;
  color: var(--text-muted);
  margin: .25rem 0 .5rem;
  font-style: italic;
}

/* ── Sidebar Help Sections ────────────────────────────────────────── */
.help-section {
  background: var(--help-bg);
  border: 1px solid var(--help-border);
  border-radius: 10px;
  padding: 1rem 1.2rem;
  margin-bottom: .9rem;
  font-size: .88rem;
  line-height: 1.65;
  color: var(--text-primary);
}
.help-section h4 {
  margin: 0 0 .55rem;
  font-size: .95rem;
  font-weight: 700;
  color: var(--step-border);
  letter-spacing: 0.01em;
}
.help-section ul {
  margin: .3rem 0 0 1.1rem;
  padding: 0;
}
.help-section li {
  margin: .28rem 0;
  color: var(--text-secondary);
}
.help-section code {
  background: var(--code-bg);
  color: var(--code-text);
  padding: .1rem .38rem;
  border-radius: 5px;
  font-family: 'Roboto Mono', monospace;
  font-size: .81rem;
  font-weight: 600;
}
.help-section table {
  width: 100%;
  border-collapse: collapse;
  font-size: .83rem;
  margin-top: .55rem;
}
.help-section th {
  text-align: left;
  padding: .35rem .55rem;
  font-weight: 700;
  background: var(--table-head-bg);
  color: var(--text-secondary);
  border-bottom: 2px solid var(--table-border);
  font-family: 'Roboto Mono', monospace;
  font-size: .80rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.help-section td {
  padding: .32rem .55rem;
  border-bottom: 1px solid var(--table-border);
  color: var(--text-primary);
}
.help-section tr:nth-child(even) td {
  background: var(--table-row-alt);
}

/* ── Tags ─────────────────────────────────────────────────────────── */
.tag {
  display: inline-block;
  padding: .1rem .5rem;
  border-radius: 20px;
  font-size: .76rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  font-family: 'Roboto Mono', monospace;
}
.tag-green  { background: var(--tag-green-bg);  color: var(--tag-green-fg);  }
.tag-blue   { background: var(--tag-blue-bg);   color: var(--tag-blue-fg);   }
.tag-orange { background: var(--tag-orange-bg); color: var(--tag-orange-fg); }

/* ── Example row ──────────────────────────────────────────────────── */
.example-row {
  font-family: 'Roboto Mono', monospace;
  font-size: .81rem;
  word-break: break-all;
  color: var(--code-text);
  background: var(--code-bg);
  padding: .35rem .6rem;
  border-radius: 6px;
  border-left: 3px solid var(--accent-cta);
}

/* ── Streamlit widget overrides ───────────────────────────────────── */
/* Nút primary – high contrast CTA */
[data-testid="stBaseButton-primary"] {
  background: var(--accent-cta) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 700 !important;
  letter-spacing: 0.02em !important;
  box-shadow: 0 2px 14px var(--accent-cta-glow) !important;
  transition: background .18s ease, box-shadow .18s ease, transform .12s ease !important;
}
[data-testid="stBaseButton-primary"]:hover {
  background: var(--accent-cta-hover) !important;
  box-shadow: 0 4px 22px var(--accent-cta-glow) !important;
  transform: translateY(-1px) !important;
}
/* Nút secondary */
[data-testid="stBaseButton-secondary"] {
  border: 1.5px solid var(--border-strong) !important;
  border-radius: 8px !important;
  color: var(--text-primary) !important;
  background: var(--bg-card) !important;
}
/* Expander */
[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  background: var(--bg-card) !important;
  box-shadow: var(--shadow-card) !important;
  margin-bottom: .6rem;
}
[data-testid="stExpander"] summary {
  font-weight: 600 !important;
  color: var(--text-primary) !important;
}
/* Radio button */
[data-testid="stRadio"] label {
  color: var(--text-primary) !important;
}
/* Selectbox */
[data-testid="stSelectbox"] > div > div {
  border: 1.5px solid var(--border) !important;
  border-radius: 8px !important;
  background: var(--bg-card) !important;
  color: var(--text-primary) !important;
}
/* File uploader */
[data-testid="stFileUploader"] {
  border: 2px dashed var(--border-strong) !important;
  border-radius: 12px !important;
  background: var(--step-bg) !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent-cta) !important;
  background: var(--accent-cta-light) !important;
}
/* Progress bar */
[data-testid="stProgressBar"] > div > div {
  background: var(--accent-cta) !important;
  border-radius: 4px;
}
/* Alerts */
[data-testid="stAlert"] {
  border-radius: 10px !important;
}
/* Code block log area */
[data-testid="stCode"] {
  border-radius: 10px !important;
  border: 1px solid var(--border) !important;
  font-family: 'Roboto Mono', monospace !important;
}
/* Markdown text */
.stMarkdown, .stText, label {
  color: var(--text-primary) !important;
}
/* Sidebar labels */
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label {
  color: var(--text-primary) !important;
}
/* Scrollbar (Webkit) */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: var(--bg-page); }
::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📖 Hướng dẫn sử dụng")

    with st.expander("📁  1. Chuẩn bị file đầu vào", expanded=False):
        st.markdown("""
<div class="help-section">
<h4>Yêu cầu file Excel</h4>
<ul>
  <li>Định dạng: <code>.xlsx</code>, <code>.xls</code>, <code>.xlsm</code></li>
  <li>Phải có sheet tên <b>Data</b> (không phân biệt hoa/thường)</li>
  <li>Nếu không có sheet Data, sheet đầu tiên sẽ được dùng</li>
</ul>
<h4>Các cột bắt buộc trong sheet Data</h4>
<table>
  <tr><th>Cột</th><th>Tên chấp nhận được</th></tr>
  <tr><td><span class="tag tag-blue">Họ tên</span></td><td>Họ tên, Họ và tên, Giáo viên…</td></tr>
  <tr><td><span class="tag tag-blue">PCCM</span></td><td>PCCM, Phân công, Môn học giảng dạy…</td></tr>
  <tr><td><span class="tag tag-orange">GVCN</span></td><td>GVCN, Chủ nhiệm, Chủ nhiệm lớp, CN…</td></tr>
</table>
<h4>Vai trò của cột GVCN</h4>
<ul>
  <li>Điền vào cột <b>CN</b> trong file output</li>
  <li>Xây dựng <b>danh sách lớp hợp lệ</b> để tách PCCM chính xác</li>
  <li>Khi gặp chuỗi có nhiều cách tách, hệ thống sẽ <b>hỏi người dùng</b></li>
</ul>
</div>
""", unsafe_allow_html=True)

    with st.expander("🏫  2. Mã môn học theo khối", expanded=False):
        st.markdown("""
<div class="help-section">
<h4>Tự động tra mã môn theo khối lớp</h4>
<p>Hệ thống tự động áp dụng bảng mã môn phù hợp dựa trên số khối của lớp — không cần chọn cấp học thủ công.</p>
<table>
  <tr><th>Khối</th><th>Cấp</th><th>Ví dụ mã môn đặc trưng</th></tr>
  <tr><td><b>1–3</b></td><td>Tiểu học</td><td>TIENGVIET, TUNHIENVAXAHOI, DAODUC, HDTN<br><i>GVCN tự động nhận: TOAN, TIENGVIET, TUNHIENVAXAHOI, DAODUC, HDTN</i></td></tr>
  <tr><td><b>4–5</b></td><td>Tiểu học</td><td>TIENGVIET, KHOAHOC, LICHSUDIALI, DAODUC, HDTN<br><i>GVCN tự động nhận: TOAN, TIENGVIET, KHOAHOC, LICHSUDIALI, DAODUC, HDTN</i></td></tr>
  <tr><td><b>6–9</b></td><td>THCS</td><td>KHTN(VATLY), KHTN(HOAHOC), KHTN(SINH), LICHSUDIALI(SU), LICHSUDIALI(DIA), GDCD, TNHN</td></tr>
  <tr><td><b>10–12</b></td><td>THPT</td><td>VATLY, HOAHOC, SINH, LICHSU, DIALY, GDKTPL, TNHN</td></tr>
</table>
<h4>Ví dụ cùng tên môn, khác mã theo khối</h4>
<ul>
  <li>Vật lý lớp <b>8A</b> → <code>KHTN(VATLY)</code> &nbsp;|&nbsp; lớp <b>11A</b> → <code>VATLY</code></li>
  <li>Lịch sử lớp <b>7A</b> → <code>LICHSUDIALI(SU)</code> &nbsp;|&nbsp; lớp <b>10A</b> → <code>LICHSU</code></li>
  <li>Hoạt động TN lớp <b>6A</b> → <code>TNHN</code> &nbsp;|&nbsp; lớp <b>2A</b> → <code>HDTN</code></li>
</ul>
</div>
""", unsafe_allow_html=True)

    with st.expander("✍️  2. Chú ý về cột PCCM", expanded=False):
        st.markdown("""
<div class="help-section">
<h4>Cấu trúc cơ bản</h4>
<p>Dữ liệu theo dạng <b>Tên môn: danh sách lớp</b>, nhiều môn ngăn cách bằng <code>+</code></p>
<div class="example-row">Hóa: 10A1, 10A2 + Sử: 10D1, 10D2</div>

<h4>Tách lớp thông minh nhờ cột GVCN</h4>
<p>Khi có cột GVCN, hệ thống xây dựng danh sách lớp hợp lệ. Nếu một chuỗi có <b>nhiều cách tách hợp lệ</b>, hệ thống hiển thị hộp hỏi để bạn chọn.</p>
<table>
  <tr><th>Chuỗi</th><th>known = {10A1…10A12}</th></tr>
  <tr><td><code>10A123</code></td><td>⚠️ Hỏi: [10A1,2,3] hay [10A12,3]?</td></tr>
  <tr><td><code>10A12</code></td><td>→ 10A12 ✅ (chỉ 1 cách)</td></tr>
  <tr><td><code>10A1-10A5</code></td><td>→ 10A1..10A5 (range rõ ràng)</td></tr>
  <tr><td><code>10ABC, 10A,B,C</code></td><td><b>Chưa phâm biệt được chữ, cần thêm lớp ở trước!</b></td></tr>
</table>

<h4>Các định dạng lớp được hỗ trợ</h4>
<table>
  <tr><th>Dạng viết</th><th>Kết quả</th></tr>
  <tr><td><code>10A1, 10A2, 10A3</code></td><td>Liệt kê thường</td></tr>
  <tr><td><code>10A123</code></td><td>→ tách theo known (hoặc hỏi)</td></tr>
  <tr><td><code>10A1-10A5</code></td><td>→ 10A1 đến 10A5</td></tr>
  <tr><td><code>11A3,4</code></td><td>→ 11A3, 11A4</td></tr>
  <tr><td><code>11A1(52)</code></td><td>→ 11A1 (bỏ sĩ số)</td></tr>
</table>
</div>
""", unsafe_allow_html=True)

#     with st.expander("🔤  3. Nhận diện tên môn học", expanded=False):
#         st.markdown("""
# <div class="help-section">
# <h4>Bảng mã môn học</h4>
# <table>
#   <tr><th>Tên môn</th><th>Mã</th></tr>
#   <tr><td>Ngữ văn / Văn</td><td><code>NGUVAN</code></td></tr>
#   <tr><td>Toán / Toán học</td><td><code>TOAN</code></td></tr>
#   <tr><td>Tiếng Anh / Anh / NN1</td><td><code>ANH</code></td></tr>
#   <tr><td>Lịch sử / Sử</td><td><code>LICHSU</code></td></tr>
#   <tr><td>Địa lý / Địa</td><td><code>DIALY</code></td></tr>
#   <tr><td>Vật lý / Lý</td><td><code>VATLY</code></td></tr>
#   <tr><td>Hóa học / Hóa</td><td><code>HOAHOC</code></td></tr>
#   <tr><td>Sinh học / Sinh</td><td><code>SINH</code></td></tr>
#   <tr><td>Tin học / Tin</td><td><code>TINHOC</code></td></tr>
#   <tr><td>GDTC / Thể dục</td><td><code>GDTC</code></td></tr>
#   <tr><td>GDQP / Quốc phòng</td><td><code>GDQP</code></td></tr>
#   <tr><td>KTPL / GDKTPL</td><td><code>GDKTPL</code></td></tr>
#   <tr><td>GDĐP / GDDP</td><td><code>NDGDDP</code></td></tr>
#   <tr><td>HĐTN / TNHN</td><td><code>TNHN</code></td></tr>
#   <tr><td>Công nghệ</td><td><code>CONGNGHE</code></td></tr>
#   <tr><td>KHTN</td><td><code>KHTN</code></td></tr>
#   <tr><td>Lịch sử &amp; Địa lý</td><td><code>LICHSUDIALI</code></td></tr>
# </table>
# </div>
# """, unsafe_allow_html=True)

#     with st.expander("📊  4. Cấu trúc file đầu ra", expanded=False):
#         st.markdown("""
# <div class="help-section">
# <h4>File output gồm 3 sheet</h4>
# <p><span class="tag tag-blue">Sheet 1: Class</span> — danh sách lớp, sắp theo khối</p>
# <p><span class="tag tag-green">Sheet 2: Teachers</span></p>
# <table>
#   <tr><th>Cột</th><th>Nội dung</th></tr>
#   <tr><td>STT</td><td>Số thứ tự</td></tr>
#   <tr><td>Họ tên</td><td>Tên giáo viên</td></tr>
#   <tr><td>Ngày sinh</td><td>dd/mm/yyyy</td></tr>
#   <tr><td>SĐT</td><td>Để trống</td></tr>
#   <tr><td>Môn dạy</td><td>Mã môn, cách nhau dấu phẩy</td></tr>
#   <tr><td>TBM</td><td>Để trống</td></tr>
#   <tr><td>CN</td><td>Lớp chủ nhiệm (từ cột GVCN)</td></tr>
#   <tr><td>PCCM</td><td><code>10A1-TOAN,11B2-ANH</code></td></tr>
# </table>
# <p><span class="tag tag-orange">Sheet 3: Students</span> — tiêu đề cố định, dữ liệu trống</p>
# </div>
# """, unsafe_allow_html=True)

#     with st.expander("⚠️  5. Xử lý trùng lặp & lưu ý", expanded=False):
#         st.markdown("""
# <div class="help-section">
# <h4>Xử lý tổ hợp môn-lớp trùng</h4>
# <ul>
#   <li><b>Trùng trong cùng 1 GV:</b> bỏ tự động</li>
#   <li><b>Trùng giữa 2+ GV:</b> thêm tên GV để phân biệt</li>
# </ul>
# <div class="example-row">12A2-HOAHOC(Nguyễn Tuấn Anh)<br>12A2-HOAHOC(Đoàn Văn Chiến)</div>
# <h4>Không có cột GVCN</h4>
# <ul>
#   <li>Cột CN trong output để trống</li>
#   <li>Không có từ điển lớp → không hỏi ambiguous, dùng logic tách cũ</li>
# </ul>
# </div>
# """, unsafe_allow_html=True)


# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("phase","upload"),("ambig_list",[]),("resolved",{}),
             ("unknown_list",[]),("resolved_subjects",{}),
             ("raw_bytes",None),("nien_khoa",NIEN_KHOA_OPTIONS[0]),
             ("known_classes",set()),("result_bytes",None),("result_filename","")]:
    if k not in st.session_state:
        st.session_state[k] = v


def _reset():
    for k in ["phase","ambig_list","resolved","unknown_list","resolved_subjects",
              "raw_bytes","nien_khoa","known_classes","result_bytes","result_filename"]:
        st.session_state.pop(k, None)
    st.rerun()


def _load_df_and_known(raw_bytes):
    import re
    from teacher_core import expand_class_range, _preprocess_alpha_suffixes
    xl  = pd.ExcelFile(io.BytesIO(raw_bytes))
    sn  = next((s for s in xl.sheet_names if s.strip().lower()=="data"), xl.sheet_names[0])
    rdf = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=sn, header=None)
    hri = detect_header_row(rdf)
    df  = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=sn, header=hri)
    df.columns = [str(c).strip() for c in df.columns]
    col_gvcn = find_column(df, ["gvcn","chủ nhiệm","chu nhiem","chủ nhiệm lớp",
                                 "chu nhiem lop","lớp chủ nhiệm","lop chu nhiem","cn"])
    known = set()
    if col_gvcn:
        # Pass 1: chỉ bắt lớp nguyên tử (1 chữ cái đơn ± số, hoặc nhiều chữ+số)
        # KHÔNG bắt dạng compact alpha thuần như "7ABCD" (nhiều chữ, không có số)
        _atomic_pat = re.compile(
            r'(?:0?[1-9]|1[0-2])'
            r'(?:'
                r'[A-Za-zÀ-ỹ]\d+'              # 1 chữ + số: 7A1, 10A12
                r'|[A-Za-zÀ-ỹ](?![A-Za-zÀ-ỹ])'  # 1 chữ không theo sau bởi chữ: 7A
                r'|[A-Za-zÀ-ỹ]{2,}\d+'          # nhiều chữ + số: 10AB1
            r')',
            re.UNICODE
        )
        known_pass1 = set()
        # Pattern bắt compact alpha liền (7ABCD) để tách thành atoms
        _compact_alpha_scan = re.compile(
            r'(?<![A-Za-z\d])(0?[1-9]|1[0-2])([A-Za-zÀ-ỹ]{2,})(?!\d)', re.UNICODE)
        for val in df[col_gvcn]:
            if pd.notna(val) and str(val).strip():
                # Tiền xử lý 7A,B,C,D → 7A,7B,7C,7D trước khi bắt lớp nguyên tử
                val_pre = _preprocess_alpha_suffixes(str(val).strip())
                for c in _atomic_pat.findall(val_pre):
                    known_pass1.add(c.strip())
                # Bắt thêm compact alpha liền (7ABCD → 7A,7B,7C,7D)
                for m in _compact_alpha_scan.finditer(str(val).strip()):
                    grade, alphas = m.group(1), m.group(2)
                    for ch in alphas:
                        known_pass1.add(f"{grade}{ch}")
        # Pass 2: expand compact alpha "7ABCD" → [7A,7B,7C,7D] dùng known_pass1
        for val in df[col_gvcn]:
            if pd.notna(val) and str(val).strip():
                expanded = expand_class_range(str(val).strip(), known_pass1 if known_pass1 else None)
                for c in expanded:
                    known.add(c.strip())
                for c in known_pass1:
                    known.add(c)
        if not known:
            known = known_pass1
    return df, col_gvcn, known


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🍹 Tạo file Import PCCM</h1>
  <p>File Input cần có sheet <b>Data</b> (hoặc sẽ lấy sheet đầu tiên của file)</p>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PHASE 1 — UPLOAD
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.phase == "upload":

    st.markdown('<div class="step-box"><b>1️⃣</b> Tải lên file cần chuyển đổi PCCM</div>',
                unsafe_allow_html=True)
    uploaded = st.file_uploader("Chọn file Excel", type=["xlsx","xls","xlsm"],
                                 label_visibility="collapsed")

    st.markdown('<div class="step-box"><b>2️⃣</b> Chọn niên khóa</div>', unsafe_allow_html=True)
    nien_khoa = st.selectbox("Niên khóa", options=NIEN_KHOA_OPTIONS, label_visibility="collapsed")

    st.markdown('<div class="step-box"><b>3️⃣</b> Nhấn <code><b>Chuyển đổi</b></code> để xử lý</div>', unsafe_allow_html=True)
    run_btn = st.button("▶  Chuyển đổi", type="primary", use_container_width=True,
                        disabled=(uploaded is None))

    if uploaded is None:
        st.info("✌️ Vui lòng tải lên file Excel đầu vào ✌️")

    if run_btn and uploaded:
        raw_bytes = uploaded.read()
        fname     = uploaded.name.rsplit(".",1)[0]

        with st.spinner("Đang phân tích file..."):
            try:
                df, col_gvcn, known = _load_df_and_known(raw_bytes)
                col_pccm = find_column(df, ["pccm","phân công chuyên môn","phân công",
                                             "giảng dạy lớp","môn học giảng dạy","pcan cong","giang day"])
                ambig_list   = []
                unknown_list = []
                if col_pccm:
                    if known:
                        ambig_list = detect_ambiguous_in_data(df, col_pccm, col_gvcn, known)
                    unknown_list = detect_unknown_subjects(df, col_pccm)
            except Exception as e:
                st.error(f"❌ Lỗi đọc file: {e}")
                st.stop()

        st.session_state.raw_bytes       = raw_bytes
        st.session_state.nien_khoa       = nien_khoa
        st.session_state.known_classes   = known
        st.session_state.result_filename = f"Import_{fname}.xlsx"

        if ambig_list:
            st.session_state.ambig_list    = ambig_list
            st.session_state.unknown_list  = unknown_list
            st.session_state.resolved      = {}
            st.session_state.phase         = "confirm_ambig"
        elif unknown_list:
            st.session_state.ambig_list    = []
            st.session_state.unknown_list  = unknown_list
            st.session_state.resolved_subjects = {}
            st.session_state.phase         = "confirm_subjects"
        else:
            st.session_state.ambig_list    = []
            st.session_state.unknown_list  = []
            st.session_state.phase         = "processing"
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# PHASE 2 — HỎI AMBIGUOUS
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "confirm_ambig":
    ambig_list = st.session_state.ambig_list

    st.markdown(f"""
<div class="warn-box">
⚠️ <b>Phát hiện {len(ambig_list)} chuỗi lớp có thể tách theo nhiều cách.</b><br>
Vui lòng chọn cách tách đúng cho từng chuỗi bên dưới, sau đó nhấn <b>Xác nhận & Tiếp tục</b>.
</div>
""", unsafe_allow_html=True)

    choices = {}

    for item in ambig_list:
        token  = item["token"]
        splits = item["splits"]
        occs   = item["occurrences"]
        option_labels = [", ".join(s) for s in splits]

        ctx_text = " &nbsp;|&nbsp; ".join(occs[:3]) + ("…" if len(occs) > 3 else "")
        st.markdown(f"""
<div class="ambig-card">
  <div>Chuỗi gốc: <span class="ambig-token">{token}</span></div>
  <div class="ambig-ctx">📍 {ctx_text}</div>
</div>
""", unsafe_allow_html=True)

        chosen = st.radio(
            f"**`{token}`** là:",
            options=option_labels,
            key=f"radio_{token}",
            horizontal=len(option_labels) <= 4,
        )
        choices[token] = splits[option_labels.index(chosen)]
        st.markdown("---")

    col_back, col_confirm = st.columns([1, 3])
    with col_back:
        if st.button("← Quay lại", use_container_width=True):
            _reset()
    with col_confirm:
        if st.button("✅  Xác nhận & Tiếp tục", type="primary", use_container_width=True):
            st.session_state.resolved = choices
            # Sau ambig → kiểm tra xem có môn không nhận ra không
            if st.session_state.get("unknown_list"):
                st.session_state.resolved_subjects = {}
                st.session_state.phase = "confirm_subjects"
            else:
                st.session_state.phase = "processing"
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# PHASE 2b — HỎI MÔN KHÔNG NHẬN RA
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "confirm_subjects":
    unknown_list = st.session_state.unknown_list
    # Hiển thị tất cả mã môn từ cả 3 cấp
    KEEP_RAW = "— Giữ nguyên (không map) —"
    code_options = [KEEP_RAW] + sorted(set(_ALL_CODES))

    st.markdown(f"""
<div class="warn-box">
⚠️ <b>Phát hiện {len(unknown_list)} tên môn chưa nhận diện được.</b><br>
Vui lòng chọn mã môn tương ứng cho từng tên bên dưới, sau đó nhấn <b>Xác nhận & Tiếp tục</b>.
</div>
""", unsafe_allow_html=True)

    subj_choices = {}  # raw_lower → code

    for item in unknown_list:
        raw        = item["raw"]
        suggestion = item["suggestion"]
        occs       = item["occurrences"]

        # Index mặc định: dùng gợi ý nếu có
        default_idx = code_options.index(suggestion) if suggestion and suggestion in code_options else 0

        ctx_text = " &nbsp;|&nbsp; ".join(occs[:3]) + ("…" if len(occs) > 3 else "")
        st.markdown(f"""
<div class="ambig-card">
  <div>Tên môn gốc: <span class="ambig-token">{raw}</span>
    {"&nbsp; 💡 Gợi ý: <b>" + suggestion + "</b>" if suggestion else ""}
  </div>
  <div class="ambig-ctx">📍 {ctx_text}</div>
</div>
""", unsafe_allow_html=True)

        chosen = st.selectbox(
            f"Mã môn cho **\"{raw}\"**:",
            options=code_options,
            index=default_idx,
            key=f"subj_{raw}",
        )
        subj_choices[raw.lower().strip()] = None if chosen == KEEP_RAW else chosen
        st.markdown("---")

    col_back, col_confirm = st.columns([1, 3])
    with col_back:
        if st.button("← Quay lại", use_container_width=True):
            # Nếu trước đó có ambig thì về confirm_ambig, không thì về upload
            if st.session_state.get("ambig_list"):
                st.session_state.phase = "confirm_ambig"
            else:
                _reset()
            st.rerun()
    with col_confirm:
        if st.button("✅  Xác nhận & Tiếp tục", type="primary", use_container_width=True):
            # Chỉ lưu những môn đã chọn mã (bỏ qua KEEP_RAW)
            st.session_state.resolved_subjects = {
                k: v for k, v in subj_choices.items() if v is not None
            }
            st.session_state.phase = "processing"
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# PHASE 3 — XỬ LÝ
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "processing":
    log_area  = st.empty()
    prog_bar  = st.progress(0)
    log_lines = []

    raw_bytes = st.session_state.raw_bytes
    nien_khoa = st.session_state.nien_khoa
    resolved          = st.session_state.get("resolved", {})
    resolved_subjects = st.session_state.get("resolved_subjects", {})

    try:
        _xl  = pd.ExcelFile(io.BytesIO(raw_bytes))
        _sn  = next((s for s in _xl.sheet_names if s.strip().lower()=="data"), _xl.sheet_names[0])
        _rdf = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=_sn, header=None)
        _hri = detect_header_row(_rdf)
        _df  = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=_sn, header=_hri)
        _df.columns = [str(c).strip() for c in _df.columns]
        _ch  = find_column(_df, ["họ tên","họ và tên","tên","giáo viên","ho ten"])
        total_t = len(_df[_df[_ch].notna()]) if _ch else 1
    except Exception:
        total_t = 1

    processed = [0]
    def progress_cb(msg):
        log_lines.append(msg)
        log_area.code("\n".join(log_lines[-20:]), language=None)
        if "Xử lý giáo viên" in msg:
            processed[0] += 1
            prog_bar.progress(min(int(processed[0]/total_t*90), 90))

    try:
        result_bytes = process_data(
            io.BytesIO(raw_bytes), nien_khoa,
            progress_cb=progress_cb,
            resolved_ambiguities=resolved,
            resolved_subjects=resolved_subjects,
        )
        prog_bar.progress(100)
        st.session_state.result_bytes = result_bytes
        st.session_state.phase        = "done"
        st.rerun()
    except Exception as e:
        prog_bar.empty()
        st.error(f"❌ Lỗi: {e}")
        if st.button("← Làm lại từ đầu"):
            _reset()


# ════════════════════════════════════════════════════════════════════════════
# PHASE 4 — DONE
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "done":
    _nk_done = st.session_state.get("nien_khoa", "")

    summary_lines = []
    if st.session_state.get("resolved"):
        for tok, cls_list in st.session_state.resolved.items():
            summary_lines.append(f"• Lớp `{tok}` → **{', '.join(cls_list)}**")
    if st.session_state.get("resolved_subjects"):
        for raw, code in st.session_state.resolved_subjects.items():
            summary_lines.append(f"• Môn **\"{raw}\"** → `{code}`")
    if summary_lines:
        with st.expander(f"ℹ️ {len(summary_lines)} mục đã xác nhận thủ công", expanded=False):
            st.markdown("\n".join(summary_lines))

    st.markdown(f'<div class="success-box">✅ <b>Chuyển đổi thành công!</b>'
                f' &nbsp;|&nbsp; Niên khóa: <b>{_nk_done}</b></div>',
                unsafe_allow_html=True)
    st.download_button(
        "⬇️  Tải xuống file Excel",
        data=st.session_state.result_bytes,
        file_name=st.session_state.result_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    st.markdown("---")
    if st.button("🔄  Chuyển đổi file khác", use_container_width=True):
        _reset()
