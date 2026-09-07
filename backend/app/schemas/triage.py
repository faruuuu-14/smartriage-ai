"""
Pydantic Schemas untuk Request dan Response Triase Medis
Mencakup Analisis Klinis Jaringan (TIME Framework) dan Tingkat Keparahan
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class TissueAnalysis(BaseModel):
    granulation_percentage: float = Field(..., description="Persentase jaringan granulasi merah (sehat)")
    slough_percentage: float = Field(..., description="Persentase jaringan slough kuning (nanah/eksudat)")
    necrotic_percentage: float = Field(..., description="Persentase jaringan nekrotik hitam (jaringan mati)")
    estimated_area_cm2: float = Field(..., description="Estimasi luas permukaan luka dalam centimeter persegi")
    severity_classification: str = Field(..., description="Kategori keparahan ukuran luka")

class QualityValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Apakah citra memenuhi standar klinis minimal")
    quality_status: str = Field(..., description="Status kualitas: OPTIMAL, BURAM, TERLALU_GELAP, TERLALU_TERANG, BUKAN_KULIT")
    blur_score: float = Field(..., description="Skor ketajaman fokus (Laplacian Variance)")
    is_blurry: bool = Field(..., description="Apakah citra terdeteksi buram/goyang")
    mean_brightness: float = Field(..., description="Tingkat kecerahan citra (0 - 255)")
    skin_percentage: float = Field(..., description="Persentase area kulit/jaringan tubuh terdeteksi")
    is_human_tissue: bool = Field(..., description="Apakah citra teridentifikasi jaringan tubuh manusia")
    warning_message: Optional[str] = Field(None, description="Peringatan klinis terkait kualitas pengambilan foto")

class ABCDEAnalysis(BaseModel):
    has_pigmented_lesion: bool = Field(..., description="Apakah terdeteksi bercak lesi pigmentasi/tahi lalat")
    risk_level: str = Field(..., description="Klasifikasi risiko: RENDAH, SEDANG, atau TINGGI")
    asymmetry_score: float = Field(..., description="Skor asimetri sumbu X dan Y (0.0 - 1.0)")
    border_score: float = Field(..., description="Skor ketidakteraturan tepi lesi (0.0 - 1.0)")
    color_variation_score: float = Field(..., description="Variasi saturasi dan rona warna lesi (0.0 - 1.0)")
    diameter_mm: float = Field(..., description="Estimasi diameter lesi dalam milimeter")
    recommendation: str = Field(..., description="Saran tindak lanjut medis spesialis kulit")
    risk_points: int = Field(..., description="Akumulasi skor kriteria ABCDE")

class AdaptiveQuestion(BaseModel):
    id: str = Field(..., description="Pengenal unik pertanyaan")
    question: str = Field(..., description="Teks pertanyaan anamnesis terarah")
    options: List[str] = Field(..., description="Opsi jawaban yang disediakan")

class ProgressTrackingResponse(BaseModel):
    success: bool = True
    day1_area_cm2: float = Field(..., description="Luas luka hari awal/sebelumnya (cm2)")
    day2_area_cm2: float = Field(..., description="Luas luka hari pemantauan (cm2)")
    area_reduction_percentage: float = Field(..., description="Persentase penyusutan luas luka (%)")
    healing_status: str = Field(..., description="Kategori trajektori penyembuhan")
    healing_badge_color: str = Field(..., description="Warna badge indikator status pemulihan")
    clinical_evaluation: str = Field(..., description="Catatan evaluasi klinis dokter AI")
    day1_tissue: TissueAnalysis = Field(..., description="Komposisi jaringan luka awal")
    day2_tissue: TissueAnalysis = Field(..., description="Komposisi jaringan luka saat ini")
    recommendations: List[str] = Field(default_factory=list, description="Saran penanganan lanjutan")

class DifferentialDiagnosisItem(BaseModel):
    condition_key: str = Field(..., description="Kunci kode kondisi patologis")
    common_name: str = Field(..., description="Nama umum penyakit/luka")
    medical_name: str = Field(..., description="Istilah medis resmi")
    probability: float = Field(..., description="Probabilitas relatif (0.0 - 1.0)")
    percentage: str = Field(..., description="Persentase probabilitas relatif")
    clinical_rationale: str = Field(..., description="Alasan klinis diferensial dipertimbangkan")

class DrugSafetyWarning(BaseModel):
    category: str = Field(..., description="Kategori peringatan/kontraindikasi")
    title: str = Field(..., description="Judul peringatan ringkas")
    warning_message: str = Field(..., description="Penjelasan detail bahaya klinis")
    severity: str = Field(..., description="Tingkat keparahan: BAHAYA_TINGGI, PERINGATAN_SEDANG, INFORMASI")

class ChatConsultRequest(BaseModel):
    condition_key: str = Field(..., description="Kondisi yang sedang dianalisis")
    message: str = Field(..., description="Pertanyaan pasien")
    chat_history: List[dict] = Field(default_factory=list, description="Riwayat obrolan sebelumnya")
    gemini_api_key: Optional[str] = Field(None, description="API Key Gemini opsional")

class ChatConsultResponse(BaseModel):
    success: bool = True
    reply: str = Field(..., description="Jawaban konsultasi dokter AI")
    suggested_questions: List[str] = Field(default_factory=list, description="Saran pertanyaan lanjutan")

class TriageAnalysisResponse(BaseModel):
    success: bool = True
    condition_key: str = Field(..., description="Kunci kode kondisi luka/kulit")
    common_name: str = Field(..., description="Nama umum yang dipahami masyarakat")
    medical_name: str = Field(..., description="Istilah medis resmi")
    confidence: float = Field(..., description="Tingkat keyakinan model (0.0 - 1.0)")
    confidence_percentage: str = Field(..., description="Persentase keyakinan model")
    
    # Triase Lampu Lalu Lintas
    triage_level: str = Field(..., description="Level urgensi: HIJAU, KUNING, atau MERAH")
    triage_color: str = Field(..., description="Warna badge triase hex code")
    triage_action: str = Field(..., description="Instruksi tindakan utama berdasarkan level triase")
    triage_reasons: List[str] = Field(default_factory=list, description="Alasan klinis penentuan level triase")
    
    # Analisis Jaringan Klinis (TIME Framework)
    tissue_analysis: TissueAnalysis = Field(..., description="Analisis komposisi jaringan luka standar medis")
    pain_level: int = Field(default=3, description="Skala nyeri pasien (1-10)")

    # Panduan Klinis & P3K
    description: str = Field(..., description="Penjelasan singkat mengenai kondisi")
    first_aid_steps: List[str] = Field(default_factory=list, description="Langkah pertolongan pertama")
    recommended_otc_meds: List[str] = Field(default_factory=list, description="Obat bebas yang aman digunakan")
    myths_and_warnings: List[str] = Field(default_factory=list, description="Peringatan keras larangan dan mitos berbahaya")
    estimated_healing_time: str = Field(..., description="Estimasi durasi penyembuhan")
    red_flags: List[str] = Field(default_factory=list, description="Tanda bahaya yang mewajibkan ke faskes")
    
    # Visualisasi Explainable AI (XAI)
    heatmap_url: Optional[str] = Field(None, description="URL gambar visualisasi Grad-CAM Heatmap")
    heatmap_base64: Optional[str] = Field(None, description="Gambar Grad-CAM Heatmap dalam format Base64")

    # Fitur Lanjutan Baru
    quality_info: Optional[QualityValidationResult] = Field(None, description="Hasil validasi kualitas dan kelayakan citra")
    adaptive_questions: List[AdaptiveQuestion] = Field(default_factory=list, description="Pertanyaan anamnesis adaptif terarah (CDSS)")
    abcde_analysis: Optional[ABCDEAnalysis] = Field(None, description="Hasil skrining ABCDE jika dicurigai lesi pigmentasi")
    
    # Fitur Komprehensif Tambahan
    top3_differential: List[DifferentialDiagnosisItem] = Field(default_factory=list, description="Top-3 diagnosis banding komparatif")
    safety_warnings: List[DrugSafetyWarning] = Field(default_factory=list, description="Peringatan keselamatan obat & kontraindikasi")
    body_location: str = Field("AUTO", description="Lokasi anatomis lesi pada tubuh")
    morphology_features: dict = Field(default_factory=dict, description="Ekstraksi fitur morfologi lesi computer vision")

class ConditionDetail(BaseModel):
    key: str
    common_name: str
    medical_name: str
    description: str
    first_aid_steps: List[str]
    recommended_otc_meds: List[str]
    myths_and_warnings: List[str]
    estimated_healing_time: str
    red_flags: List[str]
