"""
Modul Aturan Triase Cerdas (Triage Rule Engine)
Mengklasifikasikan tingkat kegawatdaruratan menjadi sistem lampu lalu lintas:
- 🟢 HIJAU: Aman dirawat mandiri di rumah dengan pertolongan pertama & obat bebas.
- 🟡 KUNING: Memerlukan pemeriksaan tenaga medis/klinik dalam 1x24 jam.
- 🔴 MERAH: Kondisi gawat darurat, harus segera ke IGD / Rumah Sakit terdekat!
"""

from enum import Enum
from typing import Dict, Any, Optional

class TriageLevel(str, Enum):
    GREEN = "HIJAU"
    YELLOW = "KUNING"
    RED = "MERAH"

def evaluate_triage(
    condition_key: str,
    confidence: float,
    has_tetanus_risk: bool = False,
    is_bleeding_uncontrolled: bool = False,
    is_deep_cut: bool = False,
    is_face_or_joint: bool = False,
    has_fever: bool = False,
    pain_level: int = 3,
    has_breathing_difficulty: bool = False
) -> Dict[str, Any]:
    """
    Mengevaluasi tingkat triase berdasarkan kondisi terdeteksi dan faktor risiko klinis.
    """
    level = TriageLevel.GREEN
    alasan: list[str] = []
    rekomendasi_tindakan: str = ""

    # 1. Evaluasi Bendera Merah Mutlak (Absolute Red Flags)
    if is_bleeding_uncontrolled:
        level = TriageLevel.RED
        alasan.append("Pendarahan aktif deras yang tidak berhenti setelah ditekan 10 menit.")
        rekomendasi_tindakan = "SEGERA KE IGD! Tekan luka dengan kain bersih secara terus-menerus selama perjalanan."
    
    elif condition_key == "LUKA_ROBEK" and is_deep_cut:
        level = TriageLevel.RED
        alasan.append("Luka robek dalam (>0.5 cm atau tampak lapisan lemak/otot), butuh penjahitan sebelum 6 jam.")
        rekomendasi_tindakan = "SEGERA KE IGD / PUSKESMAS untuk penjahitan luka (hecting) dan pencegahan infeksi."

    elif has_tetanus_risk:
        level = TriageLevel.RED
        alasan.append("Luka kotor berisiko tetanus (misal terkena paku/besi berkarat atau tercampur tanah).")
        rekomendasi_tindakan = "SEGERA KE PUSKESMAS / IGD untuk mendapatkan suntikan serum Anti-Tetanus (ATS) atau vaksin TT."

    elif has_breathing_difficulty or (condition_key == "BIDURAN_URTIKARIA" and (is_face_or_joint or pain_level >= 8)):
        level = TriageLevel.RED
        alasan.append("Reaksi alergi berat dengan pembengkakan area wajah/bibir atau risiko anafilaksis pernapasan.")
        rekomendasi_tindakan = "SEGERA KE IGD! Waspada reaksi syok anafilaksis yang mengancam jalan napas."

    elif condition_key == "LUKA_GIGITAN_HEWAN":
        level = TriageLevel.RED
        alasan.append("Gigitan/cakaran hewan berisiko tinggi penularan virus Rabies fatal (tingkat kematian 99.9% tanpa vaksin).")
        rekomendasi_tindakan = "SEGERA KE FASKES / RABIES CENTER! Cuci luka dengan air mengalir & sabun 15 menit, lalu dapatkan suntikan VAR & SAR."

    elif condition_key == "LUKA_BAKAR_BERAT_DERAJAT_3":
        level = TriageLevel.RED
        alasan.append("Luka bakar derajat 3 (seluruh ketebalan kulit hangus/putih lilin mati rasa) berisiko syok hipovolemik fatal.")
        rekomendasi_tindakan = "DARURAT IGD SEGERA! Tutup dengan kain steril kering (jangan basahi), jaga suhu tubuh, dan segera ke Unit Luka Bakar RS."

    elif condition_key == "LUKA_TUSUK_PUNCTURE" and (has_tetanus_risk or is_deep_cut or pain_level >= 7):
        level = TriageLevel.RED
        alasan.append("Luka tusuk dalam berisiko infeksi tetanus anaerobik Clostridium tetani atau benda asing tertinggal.")
        rekomendasi_tindakan = "SEGERA KE IGD / PUSKESMAS untuk penyuntikan Serum Anti-Tetanus (ATS) dan pembersihan luka steril."

    elif condition_key == "LUKA_TEKAN_DEKUBITUS" and (has_fever or pain_level >= 7 or is_deep_cut):
        level = TriageLevel.RED
        alasan.append("Borok dekubitus dalam dengan tanda komplikasi sistemik atau risiko sepsis jaringan.")
        rekomendasi_tindakan = "SEGERA KE RUMAH SAKIT / KLINIK SPESIALIS BEDAH untuk debridemen jaringan nekrotik dan antibiotik."

    elif condition_key == "HERPES_ZOSTER" and is_face_or_joint:
        level = TriageLevel.RED
        alasan.append("Herpes zoster di area wajah dekat mata berisiko kebutaan permanen (Herpes Zoster Ophthalmicus).")
        rekomendasi_tindakan = "SEGERA KE IGD / DOKTER SPESIALIS MATA untuk mencegah kerusakan kornea."

    elif condition_key == "HEMATOMA_KUKU_KEJEPIT" and (pain_level >= 8 or is_face_or_joint):
        level = TriageLevel.RED
        alasan.append("Kuku terjepit trauma dengan nyeri ekstrem berisiko fraktur tulang jari atau penumpukan darah >50%.")
        rekomendasi_tindakan = "SEGERA KE IGD / KLINIK untuk rontgen jari dan evakuasi bekuan darah (trepanasi kuku)."

    elif condition_key == "CANTENGAN_PARONIKIA" and (has_fever or pain_level >= 8):
        level = TriageLevel.RED
        alasan.append("Cantengan dengan tanda infeksi menjalar (selulitis) atau nyeri hebat berdenyut.")
        rekomendasi_tindakan = "SEGERA KE KLINIK / IGD untuk tindakan drainase nanah dan antibiotik oral."

    # 2. Evaluasi Bendera Kuning (Moderate Urgency)
    elif condition_key in ["CACAR_AIR_VARICELLA", "HERPES_ZOSTER"]:
        level = TriageLevel.YELLOW
        alasan.append("Infeksi virus herpes/cacar air; obat antivirus (Acyclovir) sangat efektif jika diminum dalam 72 jam pertama.")
        rekomendasi_tindakan = "KONSULTASI DOKTER / KLINIK untuk mendapatkan resep obat antivirus dan pereda gatal."

    elif condition_key == "LUKA_TUSUK_PUNCTURE":
        level = TriageLevel.YELLOW
        alasan.append("Luka tusuk benda runcing memerlukan konfirmasi status vaksinasi tetanus booster (TT) dalam 48 jam.")
        rekomendasi_tindakan = "KUNJUNGI PUSKESMAS / KLINIK untuk evaluasi pencegahan tetanus dan pembersihan lubang tusukan."

    elif condition_key == "LUKA_TEKAN_DEKUBITUS":
        level = TriageLevel.YELLOW
        alasan.append("Borok dekubitus tirah baring membutuhkan balutan luka modern (foam/hidrogel) dan repositioning terjadwal.")
        rekomendasi_tindakan = "KONSULTASI KLINIK / PERAWAT SPESIALIS LUKA (WOCN) untuk evaluasi perawatan luka lembap."

    elif condition_key == "LUKA_SAYAT_IRIS" and (is_face_or_joint or pain_level >= 6):
        level = TriageLevel.YELLOW
        alasan.append("Luka sayat di area sendi/wajah atau menganga >1-2 cm berisiko parut tebal atau butuh jahitan.")
        rekomendasi_tindakan = "KUNJUNGI PUSKESMAS / KLINIK dalam 6 jam untuk evaluasi penjahitan luka (hecting)."

    elif condition_key == "LUKA_MEMAR_KONTUSIO" and (pain_level >= 8 or is_face_or_joint):
        level = TriageLevel.YELLOW
        alasan.append("Benturan tumpul dengan nyeri berat atau bengkak sendi berisiko dislokasi atau retak tulang.")
        rekomendasi_tindakan = "KONSULTASI DOKTER / FASKES untuk evaluasi rontgen jika nyeri tidak membaik dalam 24 jam."

    elif condition_key == "CANTENGAN_PARONIKIA":
        level = TriageLevel.YELLOW
        alasan.append("Cantengan / kuku menusuk daging berisiko infeksi kronis dan pembentukan granuloma.")
        rekomendasi_tindakan = "KONSULTASI KLINIK / DOKTER UMUM untuk evaluasi ekstraksi kuku parsial jika nyeri tidak membaik."

    elif condition_key == "JAMUR_KUKU_ONIKOMIKOSIS":
        level = TriageLevel.YELLOW
        alasan.append("Jamur kuku kronis membutuhkan evaluasi obat antijamur khusus (kutek medis/tablet) oleh dokter.")
        rekomendasi_tindakan = "KONSULTASI KLINIK / DOKTER KULIT untuk konfirmasi mikrobiologi kerokan kuku dan terapi antijamur jangka panjang."

    elif condition_key == "ALOPECIA_KEBOTAKAN":
        level = TriageLevel.YELLOW
        alasan.append("Kebotakan koin pitak merupakan gangguan autoimun folikel rambut; terapi dini sangat menentukan hasil.")
        rekomendasi_tindakan = "KONSULTASI DOKTER SPESIALIS KULIT (Sp.D.V.E) untuk terapi kortikosteroid intralesi."

    elif condition_key == "BISUL" and (is_face_or_joint or has_fever):
        level = TriageLevel.YELLOW
        alasan.append("Bisul berlokasi di area wajah atau disertai gejala demam sistemik.")
        rekomendasi_tindakan = "KONSULTASI DOKTER dalam 1x24 jam untuk evaluasi antibiotik oral sebelum infeksi meluas."

    elif condition_key in ["LUKA_BAKAR", "LUKA_BAKAR_RINGAN"] and (is_face_or_joint or pain_level >= 7):
        level = TriageLevel.YELLOW
        alasan.append("Luka bakar di area fungsional (sendi/wajah) atau nyeri berat.")
        rekomendasi_tindakan = "KONSULTASI DOKTER / KLINIK untuk perawatan steril dan pencegahan kontraktur jaringan."

    elif has_fever:
        level = TriageLevel.YELLOW
        alasan.append("Terdapat gejala demam yang mengindikasikan infeksi sekunder sistemik.")
        rekomendasi_tindakan = "KUNJUNGI KLINIK / DOKTER UMUM untuk evaluasi infeksi."

    elif condition_key == "KUDIS_SKABIES":
        level = TriageLevel.YELLOW
        alasan.append("Penyakit parasit menular pada keluarga; membutuhkan terapi skabisida terpadu.")
        rekomendasi_tindakan = "KONSULTASI PUSKESMAS/KLINIK untuk resep krim Permethrin bagi seluruh anggota rumah."

    # 3. Kategori Hijau (Rawat Mandiri Aman)
    else:
        level = TriageLevel.GREEN
        if condition_key == "KULIT_NORMAL":
            alasan.append("Kulit sehat dan intak tanpa tanda infeksi atau trauma patologis.")
            rekomendasi_tindakan = "Pertahankan kesehatan kulit dengan pelembap dan tabir surya harian."
        elif condition_key == "KETOMBE_SEBOROIK":
            alasan.append("Dermatitis seboroik ringan dapat ditangani secara mandiri dengan sampo terapeutik (Ketoconazole / Selenium Sulfide).")
            rekomendasi_tindakan = "Gunakan sampo terapeutik 2-3 kali seminggu, diamkan busa 5 menit sebelum dibilas bersih."
        elif condition_key == "KUTU_RAMBUT_PEDIKULOSIS":
            alasan.append("Infeksi kutu rambut dapat diobati mandiri menggunakan losion Permethrin 1% dan sisir serit.")
            rekomendasi_tindakan = "Oleskan losion Permethrin 1%, sisir rambut dengan serit rapat, dan rendam air panas seluruh perlengkapan tidur."
        elif condition_key == "HEMATOMA_KUKU_KEJEPIT":
            alasan.append("Bercak darah di bawah kuku akibat cedera trauma tumpul ringan tanpa patah tulang.")
            rekomendasi_tindakan = "Kompres dingin 15 menit dan istirahatkan jari; bercak darah akan memudar mengikuti pertumbuhan kuku."
        elif condition_key == "LUKA_MEMAR_KONTUSIO":
            alasan.append("Memar trauma tumpul ringan tanpa tanda retak tulang atau kerusakan organ.")
            rekomendasi_tindakan = "Lakukan protokol R.I.C.E (kompres es 15 menit, istirahatkan), oleskan gel Heparin (Thrombophob), dan hindari pijatan."
        elif condition_key == "LUKA_SAYAT_IRIS":
            alasan.append("Luka sayat bersih dan dangkal (<1-2 cm) dengan pendarahan yang telah terkontrol.")
            rekomendasi_tindakan = "Bersihkan luka dengan air mengalir, disinfeksi Povidone Iodine, dan rekatkan dengan plester strip/kupu-kupu."
        else:
            alasan.append("Kondisi sistem integumen (kulit/kuku/rambut) ringan tanpa komplikasi kegawatdaruratan.")
            rekomendasi_tindakan = "Lakukan langkah perawatan mandiri di rumah dan gunakan obat bebas yang direkomendasikan."

    return {
        "level": level.value,
        "badge_color": "#22c55e" if level == TriageLevel.GREEN else ("#eab308" if level == TriageLevel.YELLOW else "#ef4444"),
        "reasons": alasan,
        "action_instruction": rekomendasi_tindakan
    }
