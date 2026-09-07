# SmarTriage Clinical AI 🩺✨
> **Sistem Triase Cerdas, Pendukung Keputusan Klinis (CDSS), Integumen & Trajektori Luka Berbasis Hierarchical Vision AI & Explainable AI (Grad-CAM)**

---

## 📌 Gambaran Umum Proyek
**SmarTriage Clinical AI** adalah sistem berbasis kecerdasan buatan (*Computer Vision, Morphological Feature Extraction, & Explainable AI*) yang dirancang untuk membantu tenaga kesehatan dan masyarakat dalam triase darurat, diagnosis banding komparatif, analisis jaringan luka, dan pencegahan kontraindikasi obat yang membahayakan jiwa.

### 🌟 Fitur Unggulan Sistem:
1. **Hierarchical Two-Stage Vision AI (27 Kondisi Integumen & Luka)**:
   - **Domain Luka Fisik**: Luka Sayat/Robek, Luka Lecet, Luka Bakar (Derajat 1, 2, 3), Luka Tusuk (Risiko Tetanus), Gigitan Hewan (Risiko Rabies), Ulkus Dekubitus, dan Luka Memar/Lebam.
   - **Domain Dermatologi / Ruam Kulit**: Cacar Air (*Varicella*), Cacar Api (*Herpes Zoster*), Biduran (*Urtikaria*), Kudis (*Skabies*), Kurap (*Tinea Corporis*), Panu (*Tinea Versicolor*), Eksim (*Dermatitis Atopik*), Jerawat (*Acne*), dan Bisul (*Furuncle*).
   - **Domain Kuku**: Cantengan (*Ingrown Toenail / Paronikia*), Jamur Kuku (*Onikomikosis*), dan Hematoma Subungual.
   - **Domain Rambut & Kulit Kepala**: Ketombe Berkerak (*Dermatitis Seboroik*), Kebotakan Koin (*Alopecia Areata*), dan Kutu Kepala (*Pedikulosis Kapitis*).

2. **Deteksi Morfologi Khusus (Computer Vision Precision)**:
   - **Multi-Scale Specular Vesicle Detector**: Membedakan kubah lenting berair cacar air/herpes dari bentol biduran datar.
   - **Scab Texture Entropy & Roughness**: Mengukur derajat kekasaran krusta dan diskontinuitas luka lecet agar tidak tertukar dengan lenting infeksi.
   - **Annular Ring with Central Clearing**: Mengenali lesi melingkar cincin tepi merah aktif khas Kurap/Kadas.
   - **Punctate Depth Detector**: Mengenali luka tusuk terisolasi berkedalaman tinggi.

3. **Top-3 Differential Diagnosis (DDx)**:
   Menyajikan 3 diagnosis banding teratas dengan probabilitas *softmax-calibrated* dan penjelasan rasional medis klinis.

4. **Interactive Anatomical Body Map**:
   Peta tubuh interaktif (Wajah, Dada/Perut, Punggung, Sela Jari, Kaki/Siku, Kuku, Dermatom) untuk memperkuat akurasi klasifikasi berbasis lokasi lesi (*Bayesian context prior*).

5. **Patient Safety & Drug Contraindication Engine**:
   Mendeteksi profil demografi pasien (`DEWASA`, `ANAK`, `BAYI`, `HAMIL_MENYUSUI`):
   - 🚫 **Cacar Air pada Anak**: Larangan keras pemberian Aspirin/Ibuprofen untuk mencegah **Sindrom Reye** (kerusakan otak & hepar fatal).
   - 🚫 **Jamur Kulit**: Larangan salep steroid karena memicu **Tinea Incognito**.
   - 🚫 **Luka Terbuka & Bakar**: Larangan mitos berbahaya (odol, bubuk kopi, minyak tanah, getah).

6. **Analisis Jaringan TIME ($cm^2$) & Grad-CAM Heatmap**:
   Segmentasi komposisi jaringan (Granulasi merah, Slough kuning, Nekrotik hitam) serta transparansi visual *Explainable AI*.

7. **Telehealth Virtual Doctor Chatbot**:
   Asisten konsultasi interaktif untuk tanya jawab aturan mandi, pencegahan bopeng/bekas luka, pantangan makanan, dan aturan minum obat.

8. **Serial Wound Healing Trajectory Tracker**:
   Membandingkan foto hari awal (baseline) dengan hari pemantauan untuk mengukur reduksi luas luka ($\%$ delta) dan trajektori kesembuhan.

9. **Emergency Facility Locator (Level MERAH)**:
   Navigasi 1-klik Google Maps ke IGD Rumah Sakit terdekat dan panggilan cepat 119 saat terdeteksi kegawatdaruratan medis.

---

## 📂 Struktur Direktori Proyek

```
smartriage-ai/
├── backend/                         # Backend Python (FastAPI + AI Engine)
│   ├── app/
│   │   ├── main.py                  # Entrypoint FastAPI & static mount
│   │   ├── api/v1/
│   │   │   ├── endpoints/triage.py  # Endpoints: /analyze, /consult-chat, /track-progress
│   │   │   └── router.py            # API v1 Router
│   │   ├── core/
│   │   │   ├── config.py            # Konfigurasi aplikasi
│   │   │   ├── triage_rules.py      # Rule engine triase (Hijau/Kuning/Merah)
│   │   │   ├── safety_checker.py    # Mesin pencegah kontraindikasi obat demografis
│   │   │   └── first_aid_guide.py   # Basis pengetahuan medis 27 kondisi
│   │   ├── ml/
│   │   │   ├── model.py             # Model 2-tahap (Stage 1 & Stage 2)
│   │   │   ├── morphology.py        # Ekstraksi fitur visual morfologi
│   │   │   ├── gradcam.py           # Grad-CAM heatmap generator
│   │   │   └── preprocessor.py      # Quality gatekeeper & pra-pemrosesan citra
│   │   └── schemas/triage.py        # Pydantic schemas
│   ├── static/
│   │   ├── index.html               # Antarmuka Web Modern (Tailwind + Lucide)
│   │   └── heatmaps/                # Direktori penyimpanan cache Grad-CAM
│   └── tests/
│       └── test_triage.py           # 14 Unit & Integration Tests (100% Pass)
├── mobile_android/                  # Template Aplikasi Android (Kotlin/Gradle)
├── run_backend.bat                  # Script menjalankan server Windows
├── requirements.txt                 # Dependensi Python
└── README.md
```

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Prasyarat
- Python 3.10+ (disarankan Python 3.11 - 3.14)
- Git

### 2. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Backend & Web UI
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Atau cukup klik ganda file **`run_backend.bat`**.

### 4. Akses Web
- **Antarmuka Web Modern**: [http://localhost:8000](http://localhost:8000)
- **Dokumentasi Interaktif API (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Menjalankan Pengujian Otomatis
```bash
cd backend
python -m pytest tests -v
```
*(Seluruh 14 test suite terverifikasi lulus).*

---

## 📄 Format Cetak Rekam Medis (SOAP)
Sistem dilengkapi fitur cetak standar SOAP (*Subjective, Objective, Assessment, Plan*) yang siap dilampirkan dalam rekam medis faskes atau laporan klinis ilmiah.
