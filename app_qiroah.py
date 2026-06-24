import streamlit as st
from google import genai
from google.genai import types

# 1. KONFIGURASI HALAMAN STREAMLIT
st.set_page_config(page_title="Maharah Qiroah - Ustaz Izull", page_icon="📖", layout="centered")

# Custom CSS untuk mempercantik tampilan agar ramah anak sekolah
st.markdown("""
    <style>
    .stApp { background-color: #f7f9fa; }
    .main-title { text-align: center; color: #1E4620; font-family: 'Helvetica Neue', sans-serif; }
    .subtitle { text-align: center; color: #4A6B4C; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📖 Kelas Maharah Qiroah</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>Bersama Ustaz Izull 🕌✨</h3>", unsafe_allow_html=True)
st.caption("<center>Media Belajar Membaca & Memahami Teks Bahasa Arab - MTs Kelas 8</center>", unsafe_allow_html=True)
st.divider()

# =====================================================================
# SIDEBAR: INPUT DATA SISWA (NAMA & USERNAME) DAN API KEY
# =====================================================================
GEMINI_API_KEY = "KUNCI_API_GEMINI_ANDA_DI_SINI"  # <-- Masukkan API Key Anda di sini jika ingin otomatis

with st.sidebar:
    st.header("👤 Profil Siswa & Akses")
    
    # Input Nama dan Username di Sidebar
    nama_siswa = st.text_input("Nama Lengkap:", placeholder="Masukkan nama Anda...")
    username_siswa = st.text_input("Username:", placeholder="Masukkan username...")
    
    st.divider()
    
    # Pengecekan API Key via Sidebar jika belum diisi di kode utama
    if not GEMINI_API_KEY or GEMINI_API_KEY == "KUNCI_API_GEMINI_ANDA_DI_SINI":
        input_key = st.text_input("Masukkan API Key Gemini:", type="password", help="Dapatkan API Key di Google AI Studio")
        if input_key:
            GEMINI_API_KEY = input_key
        else:
            st.warning("⚠️ Silakan masukkan API Key terlebih dahulu untuk memulai kelas.")
            st.stop()

# Inisialisasi Google GenAI Client secara global agar tidak terputus (mencegah error di image_c0601b.png)
@st.cache_resource
def get_genai_client(api_key):
    return genai.Client(api_key=api_key)

try:
    client = get_genai_client(GEMINI_API_KEY)
except Exception as e:
    st.error(f"Gagal memuat API Key atau Client error: {e}")
    st.stop()

# Validasi pengisian profil sebelum mulai belajar
if not nama_siswa or not username_siswa:
    st.info("👋 **Ahlan!** Silakan isi **Nama Lengkap** dan **Username** Anda terlebih dahulu di bagian menu kiri (sidebar) untuk mulai belajar bersama Ustaz Izull.")
    st.stop()

# 2. ATURAN & PROFIL USTAZ IZULL (System Instruction)
system_prompt = f"""
Anda adalah "Ustaz Izull", seorang tutor AI yang ramah, berwibawa, dan suportif. Anda berperan sebagai teman praktik percakapan (Maharah Qiroah) bagi pelajar bahasa Arab tingkat Menengah, khususnya siswa MTS Kelas 8 di Indonesia.
Saat ini Anda sedang berbicara dengan siswa bernama {nama_siswa} (Username: {username_siswa}). Sapa siswa dengan namanya secara santun di beberapa kesempatan agar terasa akrab.

Tujuan Utama Anda:
Membantu pengguna melatih keberanian, kelancaran, dan rasa percaya diri dalam membaca serta memahami teks bahasa Arab melalui simulasi teks yang realistis dan kontekstual. Gunakan emoji Islami dan sekolah yang menarik untuk anak MTs.

Tugas dan Aturan Respons (WAJIB DIIKUTI SECARA KONSISTEN):
1. Format Bahasa: Tuliskan respons utama Anda menggunakan Bahasa Arab yang fasih dan wajib menyertakan HARAKAT lengkap agar mudah dibaca oleh siswa MTS Kelas 8. Tepat di bawah baris teks Arab tersebut, berikan terjemahan dalam Bahasa Indonesia (ditulis miring atau dalam tanda kurung) agar pengguna tetap memahami konteks alur percakapan.
2. Koreksi yang Lembut (Gentle Correction): Jika pengguna melakukan kesalahan tata bahasa (Nahwu/Sharaf), pilihan kata (diksi), atau struktur kalimat dalam membaca/merespons teks, JANGAN langsung menyalahkan atau memotong bacaan secara kaku. Berikan respons balasan yang benar terlebih dahulu dalam bahasa Arab yang natural. Kemudian, di bagian paling akhir pesan Anda, buatlah pembatas kecil bertuliskan "[Tips Ustaz Izull 📚✨]" dan jelaskan perbaikannya dengan bahasa Indonesia secara santun, edukatif, dan jelas.
3. Mendorong Partisipasi: Selalu akhiri setiap respons Anda dengan SATU pertanyaan terbuka yang relevan dalam bahasa Arab (beserta harakat dan terjemahannya) agar percakapan/bacaan terus berlanjut.
4. Gaya Bahasa Pedagogis: Gunakan bahasa-bahasa ekspresif yang sering digunakan dalam teks nyata (seperti: 'Ya salam!', 'Tayyib', 'Masyaallah'). Berikan pujian yang tulus (seperti: 'Nutquka jayyid jiddan!' atau 'Mumtaz!') jika pengguna mencoba membaca atau menggunakan kosakata baru dengan benar.

Mode/Topik Pembelajaran (Arahkan pengguna sesuai topik yang mereka pilih):
- Mode 1: At-Ta'aruf (Perkenalan) 🤝✨ - Simulasi berkenalan dengan orang atau teman baru di lingkungan sekolah.
- Mode 2: Fil Math'am (Di Restoran) 🍽️🥤 - Simulasi memesan makanan, minuman, dan berinteraksi dengan pelayan restoran.
- Mode 3: Al-Hiwayah (Hobi) ⚽🎨 - Percakapan santai dan hangat mengenai kegiatan positif di waktu luang.
"""

# 3. INISIALISASI SESI CHAT
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        )
    )

if "messages" not in st.session_state:
    greeting_message = f"""أَهْلًا وَسَهْلًا يَا {nama_siswa}! 👋✨ أَنَا أُسْتَاذُ إِيزُول، صَدِيقُكَ لِمُمَارَسَةِ الْمُحَادَثَةِ وَالْقِرَاءَةِ بِاللُّغَةِ الْعَرَبِيَّةِ لِتَكُونَ أَكْثَرَ طَلَاقَةً. 🌟
اَلْيَوْمَ نُرِيدُ أَنْ نَتَدَرَّبَ عَلَى الْقِرَاءَةِ وَالْكَلَامِ، أَيْنَ نَتَدَرَّبُ؟ اِخْتَرِ الْمَوْضُوعَ: 📚🤩

١. اَلتَّعَارُفُ (فِي الْمَدْرَسَةِ) 🤝✨
٢. فِي الْمَطْعَمِ (طَلَبُ الطَّعَامِ) 🍽️🥤
٣. الْهِوَايَةُ (الْأَنْشِطَةُ فِي وَقْتِ الْفَرَاغِ) ⚽🎨

*(Ahlan wa Sahlan ya {nama_siswa}! 👋✨ Saya Ustaz Izull, temanmu untuk melatih percakapan dan membaca bahasa Arab agar lebih lancar. 🌟 Hari ini kita mau latihan di mana? Pilih topiknya ya: 📚🤩 1. Perkenalan di sekolah 🤝✨, 2. Di Restoran 🍽️🥤, atau 3. Tentang Hobi ⚽🎨)*"""
    
    st.session_state.messages = [{"role": "assistant", "content": greeting_message}]

# 4. MENAMPILKAN RIWAYAT CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. INPUT DARI SISWA & RESPONS OTOMATIS
if user_input := st.chat_input("Ketik respons atau ketik nomor topik pilihanmu di sini..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Ustaz Izull sedang membaca pesanmu... 📝"):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                ai_reply = response.text
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                st.error(f"Terjadi kendala pada server AI: {e}")