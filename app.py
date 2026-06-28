import streamlit as st
import pandas as pd
import json
from PIL import Image
import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from google import genai

# CONFIG
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Analisis Label Gizi",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background Utama Gelap */
.stApp { background: #0f172a; color: #e2e8f0; }

/* Hero Section */
.hero { background: linear-gradient(135deg, #1e293b 0%, #020617 100%); border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem; border: 1px solid #334155; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5); }
.hero h1 { font-size: 2.2rem; font-weight: 700; color: #f8fafc; margin: 0 0 0.5rem 0; letter-spacing: -0.5px; }
.hero p  { color: #94a3b8; font-size: 1rem; margin: 0; }
.hero-badge { display: inline-block; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 20px; padding: 4px 14px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 1rem; font-family: 'JetBrains Mono', monospace; }

/* Typography & Titles */
.section-title { font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.2px; margin: 2rem 0 1rem 0; display: flex; align-items: center; gap: 0.5rem; }
.section-title::after { content: ''; flex: 1; height: 1px; background: #334155; }

/* Profile Card */
.profile-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.profile-info { display: flex; gap: 2.5rem; }
.profile-item { display: flex; flex-direction: column; }
.profile-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 0.3rem;}
.profile-value { font-size: 1.25rem; font-weight: 700; color: #f8fafc; }

/* Data Table */
.data-table-container { background: #1e293b; border: 1px solid #334155; border-radius: 12px; overflow-x: auto; margin-bottom: 2rem; -webkit-overflow-scrolling: touch; }
.modern-table { width: 100%; border-collapse: collapse; text-align: left; white-space: nowrap; }
.modern-table th { background: #0f172a; padding: 1rem; font-size: 0.75rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #334155; }
.modern-table td { padding: 1rem; border-bottom: 1px solid #334155; font-size: 0.95rem; color: #e2e8f0; vertical-align: middle; }
.modern-table tr:last-child td { border-bottom: none; }
.modern-table tr:hover { background: #334155; }
.col-komponen { font-weight: 600; color: #f8fafc; }
.col-number { font-family: 'JetBrains Mono', monospace; font-weight: 500; }

/* Status Badges */
.status-badge { display: inline-flex; align-items: center; justify-content: center; padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; min-width: 80px; text-align: center; }
.status-rendah { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.status-sedang { background: rgba(234, 179, 8, 0.15); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.3); }
.status-tinggi { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
.status-unknown{ background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.3); }

/* AI Box */
.ai-box { background: linear-gradient(to right, #1e3a8a, #0f172a); border-left: 4px solid #3b82f6; border-radius: 8px; padding: 1.5rem; line-height: 1.6; color: #e2e8f0; font-size: 1rem; border: 1px solid #334155; }
.ai-title { font-size: 0.85rem; color: #60a5fa; font-weight: 700; letter-spacing: 1px; margin-bottom: 0.8rem; text-transform: uppercase; display: flex; align-items: center; gap: 0.5rem; }

/* Kotak Preview Gambar Pasti (Fixed Image Box) */
[data-testid="stImage"] img { max-height: 320px !important; width: auto !important; margin: 0 auto; display: block; object-fit: contain; border-radius: 8px; border: 1px solid #334155; background-color: #1e293b; padding: 4px; }

/* Buttons */
.stButton > button { background: #3b82f6 !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; padding: 0.6rem 1.5rem !important; transition: all 0.2s ease; z-index: 1;}
.stButton > button:hover { background: #2563eb !important; transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
.btn-secondary > button { background: #1e293b !important; color: #cbd5e1 !important; border: 1px solid #334155 !important; }
.btn-secondary > button:hover { background: #334155 !important; color: white !important; }

/* Adaptasi Perangkat Mobile */
@media (max-width: 768px) {
    .hero { padding: 1.5rem 1rem; }
    .hero h1 { font-size: 1.5rem; }
    .profile-card { flex-direction: column; align-items: flex-start; gap: 1rem; }
    .profile-info { flex-direction: column; gap: 1rem; width: 100%; }
    .modern-table th, .modern-table td { padding: 0.75rem 0.5rem; font-size: 0.85rem; }
    [data-testid="stImage"] img { max-height: 250px !important; }
}
</style>
""", unsafe_allow_html=True)

# LOAD AKG
@st.cache_data
def load_akg():
    try:
        df = pd.read_csv("knowledge_gizi.csv")
        df.columns = df.columns.str.lower()
        return df
    except FileNotFoundError:
        st.error("❌ File tidak ditemukan! Pastikan file tersebut ada di folder yang sama.")
        st.stop()
akg_df = load_akg()

def get_akg(umur: int, gender: str):
    data = akg_df[
        (akg_df["umur_min"] <= umur) & (akg_df["umur_max"] >= umur) &
        (akg_df["jenis_kelamin"].str.lower() == gender.lower())
    ]
    if not data.empty:
        row = data.iloc[0]
        return {
            "energi":      row.get("energi_kalori"),
            "protein":     row.get("protein_g"),
            "karbohidrat": row.get("karbohidrat_g"),
            "gula":        row.get("gula_g"),
            "natrium":     row.get("natrium_mg")
        }
    return None

# EKSTRAKSI CITRA DENGAN DEMINI

def extract_nutrition_with_gemini(img: Image.Image, retries=3) -> tuple[dict, str]:
    prompt = """
    Tugas Anda adalah membaca tabel Informasi Nilai Gizi pada gambar ini. 
    Ekstrak angkanya dan kembalikan HANYA dalam format JSON. 
    
    PENTING:
    - Cari keterangan "Jumlah Sajian per Kemasan" atau "Servings per Container". 
    - Jika tidak ada keterangan tersebut, maka isi "jumlah_sajian" dengan angka 1.
    - Ambil nilai gizi HANYA berdasarkan takaran PER SAJIAN (bukan per 100g).
    
    Gunakan tepat struktur kunci (key) berikut:
    {
        "jumlah_sajian": angka,
        "energi": angka,
        "protein": angka,
        "karbohidrat": angka,
        "gula": angka,
        "natrium": angka
    }
    Jika sebuah nilai tidak tercantum, isi dengan null. Jangan tambahkan markdown seperti ```json.
    """
    for attempt in range(retries):
        try:
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[img, prompt]
            )
            text_response = response.text.strip()
            
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
            parsed_json = json.loads(text_response.strip())
            return parsed_json, text_response
        except Exception as e:
            err_msg = str(e)
            if "503" in err_msg and attempt < retries - 1:
                time.sleep(2)
                continue
            return {}, f"Gagal mengekstrak data setelah {attempt + 1} percobaan. Pesan Error: {err_msg}"
    return {}, "Gagal mengekstrak data. Server API mungkin sedang sibuk."

# KALKULASI DAN INTERPRETASI

def kategori(p: float) -> str:
    if p <= 5:  return "Rendah"
    if p <= 20: return "Sedang"
    return "Tinggi"
DISPLAY_KEYS = ["energi", "protein", "karbohidrat", "gula", "natrium"]
UNIT_MAP = {"energi":"kkal", "protein":"g", "karbohidrat":"g", "gula":"g", "natrium":"mg"}
LABEL_MAP = {"energi":"Energi", "protein":"Protein", "karbohidrat":"Karbohidrat", "gula":"Gula", "natrium":"Natrium"}

def calculate(data: dict, akg: dict) -> dict:
    jumlah_sajian = data.get("jumlah_sajian")
    if jumlah_sajian is None or jumlah_sajian <= 0:
        jumlah_sajian = 1
    result = {}
    for key in DISPLAY_KEYS:
        nilai_per_saji = data.get(key)
        if nilai_per_saji is None:
            result[key] = {"persen": None, "kategori": None, "raw_total": None, "per_saji": None, "akg_target": akg.get(key)}
            continue
        total_1_kemasan = nilai_per_saji * jumlah_sajian
        kebutuhan_akg = akg.get(key)
        if kebutuhan_akg and kebutuhan_akg > 0:
            persen = round((total_1_kemasan / kebutuhan_akg) * 100, 1)
            result[key] = {
                "persen": persen, 
                "kategori": kategori(persen), 
                "raw_total": round(total_1_kemasan, 1),
                "per_saji": round(nilai_per_saji, 1),
                "akg_target": kebutuhan_akg
            }
        else:
            result[key] = {
                "persen": None, 
                "kategori": None, 
                "raw_total": round(total_1_kemasan, 1),
                "per_saji": round(nilai_per_saji, 1),
                "akg_target": kebutuhan_akg
            }
    return result

def generate_analysis(result: dict, umur: int, gender: str, jumlah_sajian: float) -> str:
    lines = [f"- {LABEL_MAP.get(k)}: {v['persen']}% dari batas harian" for k, v in result.items() if v["persen"] is not None]
    if not lines: return "Tidak cukup data untuk memberikan kesimpulan."
    prompt = f"""
    Pengguna adalah seorang {gender} berusia {umur} tahun.
    Mereka sedang melihat informasi gizi sebuah produk pangan kemasan dengan total {jumlah_sajian} sajian di dalam 1 kemasan.
    Jika mereka MENGKONSUMSI SELURUH KEMASAN SEKALIGUS, ini adalah persentase pemenuhan batas gizi harian mereka:
    {chr(10).join(lines)}
    TUGAS ANDA:
        Buatlah 1 paragraf kesimpulan singkat (maksimal 4-5 kalimat) yang mengalir, ramah, to-the-point, dan sangat mudah dipahami orang awam. 
        Beritahu secara langsung apakah aman mengkonsumsi seluruh kemasan ini sekaligus, atau berapa porsi maksimal yang disarankan agar batas gizi harian tidak berlebihan (terutama untuk metrik yang tinggi).    
        ATURAN MUTLAK:
        1. WAJIB menggunakan format teks biasa (plain text).
        2. DILARANG KERAS menggunakan simbol Markdown seperti asterisk (*), bold (**), hashtag (#), atau bullet points.
        3. DILARANG membuat daftar (list), gabungkan semuanya ke dalam satu paragraf utuh.
        4. DILARANG menggunakan istilah medis atau teknis yang kaku.
    """
    try:
        res = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250, temperature=0.6,
        )
        if res.choices and res.choices[0].message and res.choices[0].message.content:
            return res.choices[0].message.content.strip()
        else:
            return "⚠️ Kesimpulan AI sedang tidak tersedia (Server respons kosong)."
            
    except Exception as e:
        return f"⚠️ Kesimpulan AI sedang tidak tersedia saat ini. (Error: {str(e)})"

# FUNGSI UI LOADING

def get_overlay_html(text: str) -> str:
    return f"""
    <style>
    .loading-overlay {{
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(8px);
        z-index: 999999;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        color: white;
    }}
    .loader-ring {{
        display: inline-block; width: 64px; height: 64px; margin-bottom: 20px;
    }}
    .loader-ring:after {{
        content: " "; display: block; width: 48px; height: 48px;
        margin: 8px; border-radius: 50%;
        border: 4px solid #fff;
        border-color: #3b82f6 transparent #3b82f6 transparent;
        animation: loader-ring 1.2s linear infinite;
    }}
    @keyframes loader-ring {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    .loading-title {{ font-family: 'Inter', sans-serif; font-size: 1.5rem; font-weight: 700; margin: 0; color: #f8fafc; }}
    .loading-subtitle {{ font-family: 'Inter', sans-serif; color: #94a3b8; margin-top: 10px; font-size: 1rem; text-align: center; max-width: 80%; line-height: 1.5; }}
    </style>
    <div class="loading-overlay">
        <div class="loader-ring"></div>
        <div class="loading-title">Sistem Sedang Bekerja</div>
        <div class="loading-subtitle">{text}</div>
    </div>
    """

# STATE MANAGEMENT

if "page" not in st.session_state:
    st.session_state.page = "input"

def go_result(): st.session_state.page = "result"
def reset():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.session_state.page = "input"

# PAGE INPUT

if st.session_state.page == "input":

    overlay_placeholder = st.empty()

    st.markdown("""
<div class="hero">
<div class="hero-badge">Sistem Analisis Label Gizi Produk Pangan Kemasan</div>
<h1>Kenali Gizi dengan Cerdas</h1>
<p>Unggah label informasi nilai gizi pada produk pangan kemasan untuk melihat batas aman konsumsi yang disesuaikan secara otomatis berdasarkan umur & jenis kelamin Anda.</p>
</div>
    """, unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1.4], gap="large")
    with col_left:
        st.markdown('<div class="section-title">👤 Profil Pengguna</div>', unsafe_allow_html=True)
        c_umur, c_gender = st.columns(2)
        with c_umur:
            umur = st.number_input("Umur (Tahun)", min_value=1, max_value=100, value=22)
        with c_gender:
            gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"])
        st.markdown('<div class="section-title">📋 Metode Input</div>', unsafe_allow_html=True)
        metode = st.radio("Pilih cara input", ["🖼️ Upload Gambar", "📸 Buka Kamera", "✏️ Input Manual"], horizontal=True, label_visibility="collapsed")
    with col_right:
        data  = {}
        image = None
        if metode == "🖼️ Upload Gambar":
            st.markdown('<div class="section-title">🖼️ Upload Label Gizi</div>', unsafe_allow_html=True)
            file = st.file_uploader("Unggah foto label", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
            if file:
                image = Image.open(file)
                st.image(image, caption="Preview Foto Label", use_container_width=True)
                
        elif metode == "📸 Buka Kamera":
            st.markdown('<div class="section-title">📸 Ambil Foto Langsung</div>', unsafe_allow_html=True)
            camera_file = st.camera_input("Posisikan tabel gizi di tengah layar", label_visibility="collapsed")
            if camera_file:
                image = Image.open(camera_file)
                
        else:
            st.markdown('<div class="section-title">✏️ Input Manual</div>', unsafe_allow_html=True)
            data["jumlah_sajian"] = st.number_input("Jumlah Sajian per Kemasan", min_value=1.0, value=1.0)
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                data["energi"]        = st.number_input("Energi (kkal)", min_value=0.0, value=0.0)
                data["protein"]       = st.number_input("Protein (g)", min_value=0.0, value=0.0)
                data["karbohidrat"]   = st.number_input("Karbohidrat (g)", min_value=0.0, value=0.0)
            with c2:
                data["gula"]          = st.number_input("Gula (g)", min_value=0.0, value=0.0)
                data["natrium"]       = st.number_input("Natrium (mg)", min_value=0.0, value=0.0)

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        if st.button("🔍 Jalankan Analisis", use_container_width=True):
            st.session_state.umur   = umur
            st.session_state.gender = gender

# VALIDASI INPUT KOSONG
            
            if metode in ["🖼️ Upload Gambar", "📸 Buka Kamera"]:
                if image is None:
                    st.warning("⚠️ Perhatian: Anda belum melampirkan gambar. Harap unggah atau potret label gizi terlebih dahulu sebelum menjalankan analisis!")
                    st.stop()
            else:
# Cek jika seluruh data komponen gizi (selain sajian) masih bernilai 0.0
                if data["energi"] == 0 and data["protein"] == 0 and data["karbohidrat"] == 0 and data["gula"] == 0 and data["natrium"] == 0:
                    st.warning("⚠️ Perhatian: Seluruh nilai komponen gizi masih kosong (0). Harap isi minimal satu data gizi secara manual!")
                    st.stop()
# Lanjut ke proses ekstraksi jika validasi terpenuhi
            if metode in ["🖼️ Upload Gambar", "📸 Buka Kamera"]:
#Mengubah elemen placeholder menjadi Blur Full Screen + Teks Tahap 1
                overlay_placeholder.markdown(get_overlay_html("Tahap 1/3: Mengekstrak angka gizi dari gambar menggunakan Vision Model AI..."), unsafe_allow_html=True)
                parsed_data, raw_resp = extract_nutrition_with_gemini(image)
                st.session_state.data = parsed_data
            else:
                st.session_state.data = {k: (v if v > 0 else None) for k, v in data.items()}
#Teks Tahap 2
            overlay_placeholder.markdown(get_overlay_html("Tahap 2/3: Mencocokkan dengan standar Angka Kecukupan Gizi (AKG) berdasarkan profil pengguna..."), unsafe_allow_html=True)
            jumlah_saji = st.session_state.data.get("jumlah_sajian", 1)
            if jumlah_saji <= 0: jumlah_saji = 1
            akg = get_akg(umur, gender)
            if not akg:
#Jika error, overlay akan hilang agar user bisa melihat pesan galat
                overlay_placeholder.empty()
                st.error("❌ Data AKG tidak ditemukan di basis data.")
                st.stop()
            result = calculate(st.session_state.data, akg)
            st.session_state.result = result
#Teks Tahap 3
            overlay_placeholder.markdown(get_overlay_html("Tahap 3/3: AI sedang menyusun rekomendasi dan batas porsi yang aman (Membutuhkan sedikit waktu)..."), unsafe_allow_html=True)
            ai_text = generate_analysis(result, umur, gender, jumlah_saji)
            st.session_state.ai_text = ai_text
#Saat selesai overlay hilang dan pindah halaman
            overlay_placeholder.markdown(get_overlay_html("✅ Selesai! Mengarahkan ke Dashboard Hasil..."), unsafe_allow_html=True)
            time.sleep(0.5) 
            go_result()
            st.rerun()

# PAGE 2 — Dasbor hasil Analisis Gizi

elif st.session_state.page == "result":
    data        = st.session_state.data
    umur        = st.session_state.umur
    gender = st.session_state.gender
    result      = st.session_state.result
    ai_text     = st.session_state.ai_text
    jumlah_saji = data.get("jumlah_sajian")
    if jumlah_saji is None or jumlah_saji <= 0: jumlah_saji = 1

    st.markdown("""
<div class="hero" style="padding: 1.5rem 2.5rem; margin-bottom: 1.5rem;">
<h1 style="font-size: 1.8rem;">Laporan Analisis Gizi</h1>
<p>Ringkasan hasil analisis gizi produk pangan kemasan berdasarkan kebutuhan nutrisi Anda.</p>
</div>
    """, unsafe_allow_html=True)
    # 1. Menampilkan Profil Pengguna
    st.markdown(f"""
<div class="profile-card">
<div class="profile-info">
<div class="profile-item">
<span class="profile-label">Profil Pengguna</span>
<span class="profile-value">{gender}, {umur} Tahun</span>
</div>
<div class="profile-item">
<span class="profile-label">Ukuran Porsi Produk Pangan Kemasan</span>
<span class="profile-value">{jumlah_saji} Sajian / Kemasan</span>
</div>
</div>
</div>
    """, unsafe_allow_html=True)
    # 2. Tabel Data Analis Terintegrasi
    st.markdown('<div class="section-title">📊 Tabel Metrik Gizi</div>', unsafe_allow_html=True)
    table_html = """<div class="data-table-container">
<table class="modern-table">
<thead>
<tr>
<th>Komponen Gizi</th>
<th>Nilai Per Sajian</th>
<th>Total (1 Kemasan)</th>
<th>Target Angka Kecukupan Gizi Harian</th>
<th>% Pemenuhan Harian</th>
<th>Indikator Konsumsi</th>
</tr>
</thead>
<tbody>"""
    for k in DISPLAY_KEYS:
        v = result[k]
        komponen = LABEL_MAP[k]
        unit = UNIT_MAP[k]
        
        if v["per_saji"] is None:
            table_html += f"""
<tr>
<td class="col-komponen">{komponen}</td>
<td class="col-number">—</td>
<td class="col-number">—</td>
<td class="col-number">{v['akg_target']} {unit}</td>
<td class="col-number">—</td>
<td><span class="status-badge status-unknown">TIDAK ADA DATA</span></td>
</tr>"""
        else:
            kat = (v["kategori"] or "unknown").lower()
            persen_str = f"{v['persen']}%" if v["persen"] is not None else "—"
            table_html += f"""
<tr>
<td class="col-komponen">{komponen}</td>
<td class="col-number">{v['per_saji']} {unit}</td>
<td class="col-number" style="font-weight: 700;">{v['raw_total']} {unit}</td>
<td class="col-number">{v['akg_target']} {unit}</td>
<td class="col-number" style="font-weight: 700;">{persen_str}</td>
<td><span class="status-badge status-{kat}">{v["kategori"].upper()}</span></td>
</tr>"""
    table_html += """
</tbody>
</table>
</div>"""
    st.markdown(table_html, unsafe_allow_html=True)
    # 3. Kesimpulan Akhir AI
    st.markdown('<div class="section-title">💡 Kesimpulan & Rekomendasi</div>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="ai-box">
<div class="ai-title">Rangkuman hasil analisis</div>
{ai_text}
</div>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Tombol Pindai Ulang
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("🔄 Pindai Label Lain ?", use_container_width=True):
            reset()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)