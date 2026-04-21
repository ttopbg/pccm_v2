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
   Phong cách: Modern-Clean x Retro/Vintage
   Cấu trúc: Strict Grid & Card-based
═══════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
  /* ================= LIGHT MODE ================= */
  /* Nền Pastel hoài cổ - Sạch sẽ, dịu mắt */
  --bg-page:          #F7F5F0;          /* Kem ấm hoài cổ */
  --bg-card:          #FFFFFF;          /* Trắng tinh để tách biệt Card */
  --bg-card-hover:    #F0EBE1;
  --bg-sidebar:       #EFECE4;          /* Xám be nhạt */

  /* Text - Tương phản cực cao để dễ đọc */
  --text-primary:     #1A1A1A;          /* Đen tuyền */
  --text-secondary:   #4A4742;          /* Xám than */
  --text-muted:       #757169;
  --text-on-accent:   #FFFFFF;

  /* CTA (Call To Action) - Đỏ gạch/Cam đất Retro nổi bật */
  --accent-cta:       #D95A4E;          
  --accent-cta-hover: #C24A3E;
  --accent-cta-glow:  rgba(217, 90, 78, 0.25);
  
  /* Điểm nhấn phụ - Xanh Navy Retro */
  --accent-secondary: #2C435F;

  /* Card Borders - Viền rõ nét, nghiêm ngặt */
  --border:           #D6D2C4;
  --border-strong:    #A8A393;

  /* Trạng thái */
  --step-bg:          #FFFFFF;
  --step-border:      #2C435F;
  --step-text:        #2C435F;

  --success-bg:       #F0FDF4;
  --success-border:   #16A34A;
  --success-text:     #14532D;

  --warn-bg:          #FFFBEB;
  --warn-border:      #D97706;
  --warn-text:        #78350F;

  /* Help & Code */
  --help-bg:          #FFFFFF;
  --code-bg:          #F1F5F9;
  --code-text:        #0F172A;

  /* Tags */
  --tag-green-bg:     #DCFCE7;
  --tag-green-fg:     #166534;
  --tag-blue-bg:      #DBEAFE;
  --tag-blue-fg:      #1E40AF;
  --tag-orange-bg:    #FEF3C7;
  --tag-orange-fg:    #92400E;

  /* Thẩm mỹ Đổ bóng - Gọn gàng, phân lớp rõ */
  --shadow-card:      0 2px 4px rgba(0,0,0,0.04), 0 0 0 1px var(--border);
  --shadow-card-hover:0 4px 12px rgba(0,0,0,0.08), 0 0 0 1px var(--border-strong);
}

[data-theme="dark"] {
  /* ================= DARK MODE ================= */
  /* Nền tối có chiều sâu - Không dùng đen thui, dùng Xám than */
  --bg-page:          #1C1B19;          
  --bg-card:          #262522;          
  --bg-card-hover:    #302E2A;
  --bg-sidebar:       #21201D;          

  /* Text - Độ tương phản hoàn hảo trên nền tối */
  --text-primary:     #F2EFE9;          
  --text-secondary:   #BAB5AB;          
  --text-muted:       #858178;
  --text-on-accent:   #FFFFFF;

  /* CTA - Cam sáng bật tone trên nền tối */
  --accent-cta:       #E66E63;          
  --accent-cta-hover: #F28077;
  --accent-cta-glow:  rgba(230, 110, 99, 0.3);
  
  --accent-secondary: #5E81AC;

  --border:           #3D3A35;
  --border-strong:    #5E5A52;

  --step-bg:          #262522;
  --step-border:      #5E81AC;
  --step-text:        #A3BE8C;

  --success-bg:       rgba(22, 163, 74, 0.15);
  --success-border:   #4ADE80;
  --success-text:     #BBF7D0;

  --warn-bg:          rgba(217, 119, 6, 0.15);
  --warn-border:      #FBBF24;
  --warn-text:        #FDE68A;

  --help-bg:          #262522;
  --code-bg:          #111111;
  --code-text:        #E2E8F0;

  --tag-green-bg:     rgba(22, 163, 74, 0.2);
  --tag-green-fg:     #86EFAC;
  --tag-blue-bg:      rgba(30, 64, 175, 0.3);
  --tag-blue-fg:      #93C5FD;
  --tag-orange-bg:    rgba(146, 64, 14, 0.3);
  --tag-orange-fg:    #FCD34D;

  --shadow-card:      0 4px 6px rgba(0,0,0,0.3), 0 0 0 1px var(--border);
  --shadow-card-hover:0 6px 16px rgba(0,0,0,0.5), 0 0 0 1px var(--border-strong);
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

/* ── Header Banner - Phong cách Retro x Modern ────────────────────── */
.main-header {
  background: var(--bg-card);
  border: 2px solid var(--border-strong);
  color: var(--text-primary);
  padding: 1.5rem 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 4px 4px 0px var(--border-strong); /* Shadow mảng khối hoài cổ */
  text-align: left;
  border-left: 8px solid var(--accent-cta);
}
.main-header h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}
.main-header p {
  margin: .5rem 0 0;
  color: var(--text-secondary);
  font-size: 1rem;
  font-family: 'Roboto Mono', monospace;
}

/* ── Step Cards (Thẻ hướng dẫn) ──────────────────────────────────── */
.step-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 4px solid var(--step-border);
  color: var(--text-primary);
  padding: 1rem 1.2rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-weight: 600;
  box-shadow: var(--shadow-card);
}
.step-box b {
  color: var(--step-border);
  font-family: 'Roboto Mono', monospace;
  font-size: 1.1rem;
  margin-right: 8px;
}

/* ── Alert & Status Cards ─────────────────────────────────────────── */
.success-box, .warn-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 1rem 1.2rem;
  border-radius: 8px;
  margin-bottom: 1.2rem;
  font-weight: 500;
  box-shadow: var(--shadow-card);
}
.success-box {
  border-left: 5px solid var(--success-border);
  color: var(--success-text);
  background: var(--success-bg);
}
.warn-box {
  border-left: 5px solid var(--warn-border);
  color: var(--warn-text);
  background: var(--warn-bg);
}

/* ── Ambig Card (Thẻ hiển thị dữ liệu lỗi/chờ xử lý) ──────────────── */
.ambig-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.2rem;
  margin-bottom: 1.2rem;
  box-shadow: var(--shadow-card);
  transition: box-shadow .2s ease;
}
.ambig-card:hover {
  box-shadow: var(--shadow-card-hover);
}
.ambig-token {
  font-family: 'Roboto Mono', monospace;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--warn-border);
  background: var(--warn-bg);
  padding: 2px 8px;
  border-radius: 4px;
}
.ambig-ctx {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 0.8rem;
  padding-top: 0.8rem;
  border-top: 1px dashed var(--border);
  font-family: 'Roboto Mono', monospace;
}

/* ── Hướng dẫn Sidebar (Help Section) ─────────────────────────────── */
.help-section {
  background: var(--help-bg);
  border-radius: 6px;
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--text-secondary);
}
.help-section h4 {
  margin: 0 0 .8rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid var(--border);
  padding-bottom: 4px;
}
.help-section ul { padding-left: 1.2rem; margin-top: 0.5rem; }
.help-section li { margin-bottom: 0.4rem; }
.help-section code {
  background: var(--code-bg);
  color: var(--code-text);
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-family: 'Roboto Mono', monospace;
  border: 1px solid var(--border);
}
.help-section table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.8rem;
  background: var(--bg-card);
}
.help-section th {
  text-align: left;
  padding: 0.5rem;
  font-weight: 600;
  background: var(--bg-page);
  color: var(--text-primary);
  border: 1px solid var(--border);
  font-family: 'Roboto Mono', monospace;
  font-size: 0.75rem;
}
.help-section td {
  padding: 0.5rem;
  border: 1px solid var(--border);
  font-size: 0.8rem;
}

/* ── Tags ─────────────────────────────────────────────────────────── */
.tag {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  font-family: 'Roboto Mono', monospace;
}
.tag-green  { background: var(--tag-green-bg);  color: var(--tag-green-fg);  border: 1px solid var(--success-border);}
.tag-blue   { background: var(--tag-blue-bg);   color: var(--tag-blue-fg);   border: 1px solid var(--step-border);}
.tag-orange { background: var(--tag-orange-bg); color: var(--tag-orange-fg); border: 1px solid var(--warn-border);}

/* ── Streamlit Widget Overrides - Ép chuẩn Card-based ─────────────── */

/* Nút CTA (Chuyển đổi, Xác nhận) - High Contrast */
[data-testid="stBaseButton-primary"] {
  background: var(--accent-cta) !important;
  color: #FFFFFF !important;
  border: 2px solid var(--accent-cta) !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
  font-size: 1.05rem !important;
  padding: 0.6rem 1rem !important;
  box-shadow: 0 4px 14px var(--accent-cta-glow) !important;
  transition: all 0.2s ease !important;
}
[data-testid="stBaseButton-primary"]:hover {
  background: var(--accent-cta-hover) !important;
  border-color: var(--accent-cta-hover) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px var(--accent-cta-glow) !important;
}

/* Nút phụ (Quay lại) */
[data-testid="stBaseButton-secondary"] {
  border: 2px solid var(--border-strong) !important;
  border-radius: 6px !important;
  color: var(--text-primary) !important;
  background: var(--bg-card) !important;
  font-weight: 600 !important;
}
[data-testid="stBaseButton-secondary"]:hover {
  background: var(--bg-page) !important;
  border-color: var(--text-primary) !important;
}

/* Expander (Khối nội dung gập/mở) */
[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  background: var(--bg-card) !important;
  box-shadow: var(--shadow-card) !important;
  margin-bottom: 0.8rem;
}
[data-testid="stExpander"] summary {
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  padding: 0.5rem !important;
}

/* Radio button & Selectbox */
[data-testid="stRadio"] label, [data-testid="stSelectbox"] label {
  color: var(--text-primary) !important;
  font-weight: 600 !important;
}
[data-testid="stSelectbox"] > div > div {
  border: 1px solid var(--border-strong) !important;
  border-radius: 6px !important;
  background: var(--bg-card) !important;
  color: var(--text-primary) !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
  border: 2px dashed var(--border-strong) !important;
  border-radius: 8px !important;
  background: var(--bg-card) !important;
  padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent-cta) !important;
  background: var(--bg-page) !important;
}

/* Progress bar */
[data-testid="stProgressBar"] > div > div {
  background: var(--accent-cta) !important;
  border-radius: 4px;
}

/* Code block log area */
[data-testid="stCode"] {
  border-radius: 6px !important;
  border: 1px solid var(--border-strong) !important;
  background: var(--code-bg) !important;
}

/* Fix text colors globally */
.stMarkdown, .stText, label { color: var(--text-primary) !important; }
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label { color: var(--text-primary) !important; }

/* Scrollbar vuông vắn gọn gàng */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg-page); border-left: 1px solid var(--border); }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 0px; }
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
<code>Hóa: 10A1, 10A2 + Sử: 10D1, 10D2</code>

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
  <p>Hệ thống tự động chuẩn hóa dữ liệu & gán mã môn học</p>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PHASE 1 — UPLOAD
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.phase == "upload":

    st.markdown('<div class="step-box"><b>1</b> Chọn File đầu vào (Sheet: Data)</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Chọn file Excel", type=["xlsx","xls","xlsm"],
                                 label_visibility="collapsed")

    st.markdown('<div class="step-box"><b>2</b> Áp dụng niên khóa</div>', unsafe_allow_html=True)
    nien_khoa = st.selectbox("Niên khóa", options=NIEN_KHOA_OPTIONS, label_visibility="collapsed")

    st.markdown('<div class="step-box"><b>3</b> Tiến hành xử lý dữ liệu</div>', unsafe_allow_html=True)
    run_btn = st.button("▶ Chuyển đổi", type="primary", use_container_width=True,
                        disabled=(uploaded is None))

    if uploaded is None:
        st.info("✌️ Vui lòng tải lên file Excel đầu vào để bắt đầu quá trình.")

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
⚠️ <b>Phát hiện {len(ambig_list)} chuỗi lớp có nhiều cách hiểu.</b><br>
Vui lòng làm rõ định dạng tách đúng trước khi hệ thống tiếp tục.
</div>
""", unsafe_allow_html=True)

    choices = {}

    for item in ambig_list:
        token  = item["token"]
        splits = item["splits"]
        occs   = item["occurrences"]
        option_labels = [", ".join(s) for s in splits]

        ctx_text = " • ".join(occs[:3]) + ("…" if len(occs) > 3 else "")
        st.markdown(f"""
<div class="ambig-card">
  <div style="margin-bottom: 8px;">Chuỗi phát hiện: <span class="ambig-token">{token}</span></div>
  <div class="ambig-ctx">Ngữ cảnh: {ctx_text}</div>
</div>
""", unsafe_allow_html=True)

        chosen = st.radio(
            f"Vui lòng chọn cách hiểu đúng cho **`{token}`**:",
            options=option_labels,
            key=f"radio_{token}",
            horizontal=len(option_labels) <= 4,
        )
        choices[token] = splits[option_labels.index(chosen)]
        st.markdown("<br>", unsafe_allow_html=True)

    col_back, col_confirm = st.columns([1, 3])
    with col_back:
        if st.button("← Hủy và Quay lại", use_container_width=True):
            _reset()
    with col_confirm:
        if st.button("Xác nhận & Tiếp tục  ✅", type="primary", use_container_width=True):
            st.session_state.resolved = choices
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
    KEEP_RAW = "— Giữ nguyên (bỏ qua) —"
    code_options = [KEEP_RAW] + sorted(set(_ALL_CODES))

    st.markdown(f"""
<div class="warn-box">
⚠️ <b>Cần làm rõ mã cho {len(unknown_list)} tên môn học.</b><br>
Hệ thống không tìm thấy mã chuẩn cho các tên gọi dưới đây.
</div>
""", unsafe_allow_html=True)

    subj_choices = {}  

    for item in unknown_list:
        raw        = item["raw"]
        suggestion = item["suggestion"]
        occs       = item["occurrences"]

        default_idx = code_options.index(suggestion) if suggestion and suggestion in code_options else 0
        ctx_text = " • ".join(occs[:3]) + ("…" if len(occs) > 3 else "")
        
        st.markdown(f"""
<div class="ambig-card">
  <div style="margin-bottom: 8px;">Tên môn gốc: <span class="ambig-token">{raw}</span>
    {"<span style='margin-left: 10px; font-size: 0.9em; color: var(--success-border);'>💡 Gợi ý của hệ thống: <b>" + suggestion + "</b></span>" if suggestion else ""}
  </div>
  <div class="ambig-ctx">Ngữ cảnh: {ctx_text}</div>
</div>
""", unsafe_allow_html=True)

        chosen = st.selectbox(
            f"Chọn mã chuẩn cho môn **\"{raw}\"**:",
            options=code_options,
            index=default_idx,
            key=f"subj_{raw}",
        )
        subj_choices[raw.lower().strip()] = None if chosen == KEEP_RAW else chosen
        st.markdown("<br>", unsafe_allow_html=True)

    col_back, col_confirm = st.columns([1, 3])
    with col_back:
        if st.button("← Hủy và Quay lại", use_container_width=True):
            if st.session_state.get("ambig_list"):
                st.session_state.phase = "confirm_ambig"
            else:
                _reset()
            st.rerun()
    with col_confirm:
        if st.button("Xác nhận & Tiếp tục  ✅", type="primary", use_container_width=True):
            st.session_state.resolved_subjects = {
                k: v for k, v in subj_choices.items() if v is not None
            }
            st.session_state.phase = "processing"
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# PHASE 3 — XỬ LÝ
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "processing":
    st.markdown('<div class="step-box">⏳ Đang xử lý dữ liệu tự động...</div>', unsafe_allow_html=True)
    prog_bar  = st.progress(0)
    log_area  = st.empty()
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
        st.error(f"❌ Phát sinh lỗi trong quá trình xử lý: {e}")
        if st.button("← Quay lại từ đầu"):
            _reset()


# ════════════════════════════════════════════════════════════════════════════
# PHASE 4 — DONE
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "done":
    _nk_done = st.session_state.get("nien_khoa", "")

    st.markdown(f'<div class="success-box" style="font-size: 1.1rem; padding: 1.5rem;">✅ <b>HOÀN TẤT CHUYỂN ĐỔI!</b><br>'
                f'<span style="font-weight: normal; font-size: 0.95rem; color: var(--text-secondary);">Dữ liệu niên khóa <b>{_nk_done}</b> đã sẵn sàng.</span></div>',
                unsafe_allow_html=True)
                
    st.download_button(
        "⬇️  Lưu File Excel",
        data=st.session_state.result_bytes,
        file_name=st.session_state.result_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True,
    )
    
    summary_lines = []
    if st.session_state.get("resolved"):
        for tok, cls_list in st.session_state.resolved.items():
            summary_lines.append(f"- Lớp `{tok}` → **{', '.join(cls_list)}**")
    if st.session_state.get("resolved_subjects"):
        for raw, code in st.session_state.resolved_subjects.items():
            summary_lines.append(f"- Môn **\"{raw}\"** → `{code}`")
    if summary_lines:
        with st.expander(f"📋 Bảng tra soát thay đổi thủ công ({len(summary_lines)} mục)", expanded=False):
            st.markdown("\n".join(summary_lines))

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🔄 Bắt đầu lượt xử lý mới", use_container_width=True):
        _reset()
