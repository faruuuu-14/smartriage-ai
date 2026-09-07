"""
Modul Patient Safety & Drug Contraindication Engine
Mengevaluasi kontraindikasi obat dan peringatan bahaya klinis berdasarkan:
1. Kondisi patologis yang terdeteksi
2. Kelompok demografi pasien (Dewasa, Anak-Anak, Bayi, Ibu Hamil/Menyusui)
"""

from typing import List, Dict, Any

def evaluate_drug_safety(condition_key: str, patient_group: str = "DEWASA") -> List[Dict[str, Any]]:
    """
    Menghasilkan daftar peringatan keselamatan farmakologis dan kontraindikasi medis.
    """
    warnings: List[Dict[str, Any]] = []
    group = patient_group.upper()

    # 1. KONTRAINDIKASI MUTLAK: CACAR AIR + ANAK/BAYI (SINDROM REYE)
    if condition_key in ["CACAR_AIR_VARICELLA", "HERPES_ZOSTER"]:
        if group in ["ANAK", "BAYI"]:
            warnings.append({
                "category": "KONTRAINDIKASI_MUTLAK",
                "title": "BAHAYA FATAL: DILARANG MENGGUNAKAN ASPIRIN & IBUPROFEN",
                "warning_message": (
                    "Dilarang keras memberikan obat penurun panas turunan Aspirin atau Ibuprofen pada anak/bayi penderita cacar air. "
                    "Kombinasi ini berisiko fatal memicu Sindrom Reye (pembengkakan otak akut dan kegagalan fungsi hati mendadak) "
                    "serta meningkatkan risiko infeksi bakteri invasif sekunder (fasciitis nekrotikans). "
                    "Gunakan HANYA Paracetamol murni sesuai dosis berat badan anak!"
                ),
                "severity": "BAHAYA_TINGGI"
            })
        warnings.append({
            "category": "LARANGAN_TINDAKAN",
            "title": "Jangan Memecahkan Lenting Berair",
            "warning_message": (
                "Hindari memencet atau menggaruk lenting gelembung air karena cairan di dalamnya sangat menular dan "
                "dapat meninggalkan bekas bopeng permanen serta memicu infeksi bakteri sekunder bernanah (impetigo)."
            ),
            "severity": "PERINGATAN_SEDANG"
        })

    # 2. KONTRAINDIKASI STEROID PADA INFEKSI JAMUR (TINEA INCOGNITO)
    if condition_key in ["KURAP_KADAS", "PANU", "JAMUR_KUKU_ONIKOMIKOSIS"]:
        warnings.append({
            "category": "KONTRAINDIKASI_MUTLAK",
            "title": "Dilarang Menggunakan Salep Kortikosteroid (Tinea Incognito)",
            "warning_message": (
                "Jangan mengoleskan salep steroid (seperti Hidrokortison, Betametason, atau Deksametason) pada infeksi jamur. "
                "Steroid akan menekan imunitas lokal kulit dan justru menyuburkan jamur sehingga ruam menyebar luas tak terkendali "
                "(Tinea Incognito). Gunakan salep antijamur murni seperti Miconazole atau Clotrimazole."
            ),
            "severity": "BAHAYA_TINGGI"
        })

    # 3. KONTRAINDIKASI ZAT BERBAHAYA PADA LUKA TERBUKA & TRAUMA
    if condition_key in [
        "LUKA_TUSUK_PUNCTURE", "LUKA_GIGITAN_HEWAN", "LUKA_ROBEK", 
        "LUKA_LECET", "LUKA_SAYAT_IRIS", "LUKA_TEKAN_DEKUBITUS"
    ]:
        warnings.append({
            "category": "LARANGAN_P3K",
            "title": "Pantangan Zat Berbahaya pada Rongga Luka Terbuka",
            "warning_message": (
                "Dilarang keras menaburkan bubuk kopi, minyak tanah, abu gosok, getah pohon, pasta gigi, atau menuangkan alkohol 70% langsung "
                "ke dalam rongga luka terbuka. Zat-zat ini merusak jaringan granulasi sehat, memperparah nyeri, memicu reaksi benda asing, "
                "dan meningkatkan risiko infeksi tetanus/sepsis."
            ),
            "severity": "BAHAYA_TINGGI"
        })
        if condition_key == "LUKA_TUSUK_PUNCTURE":
            warnings.append({
                "category": "LARANGAN_P3K",
                "title": "Jangan Menutup Luka Tusuk Terlalu Rapat",
                "warning_message": (
                    "Bakteri tetanus (Clostridium tetani) adalah bakteri anaerob yang berkembang biak pesat dalam kondisi tanpa oksigen. "
                    "Tutup luka dengan kassa longgar yang steril, jangan diplester kedap udara."
                ),
                "severity": "PERINGATAN_SEDANG"
            })

    # 4. KONTRAINDIKASI LUKA BAKAR
    if condition_key in ["LUKA_BAKAR", "LUKA_BAKAR_BERAT_DERAJAT_3"]:
        warnings.append({
            "category": "LARANGAN_P3K",
            "title": "Dilarang Menggunakan Es Batu atau Pasta Gigi",
            "warning_message": (
                "Jangan menempelkan es batu langsung ke luka bakar karena memicu vasokonstriksi mendadak dan kerusakan jaringan akibat radang dingin (frostbite). "
                "Jangan mengoleskan odol/mentega/kecap karena memerangkap panas di dalam kulit dan memicu kolonisasi kuman. "
                "Gunakan air mengalir suhu ruang selama 15-20 menit."
            ),
            "severity": "BAHAYA_TINGGI"
        })

    # 5. KONTRAINDIKASI LUKA MEMAR
    if condition_key == "LUKA_MEMAR_KONTUSIO":
        warnings.append({
            "category": "LARANGAN_P3K",
            "title": "Dilarang Memijat atau Mengurut Area Memar Baru",
            "warning_message": (
                "Memijat atau mengurut luka lebam/memar baru (< 48 jam) dapat memecahkan lebih banyak kapiler darah, "
                "memperluas perdarahan internal (hematoma), dan meningkatkan risiko kalsifikasi otot abnormal (myositis ossificans). "
                "Cukup kompres dingin (es dibalut handuk) selama 15 menit."
            ),
            "severity": "PERINGATAN_SEDANG"
        })

    # 6. FILTER KHUSUS IBU HAMIL & MENYUSUI
    if group == "HAMIL_MENYUSUI":
        warnings.append({
            "category": "PERINGATAN_KEHAMILAN",
            "title": "Peringatan Keamanan Janin & ASI",
            "warning_message": (
                "Hindari konsumsi obat oral sistemik (terutama antijamur Ketoconazole/Griseofulvin oral, antibiotik tetrasiklin, "
                "dan obat antihistamin tertentu) tanpa resep dokter spesialis kandungan (Sp.O.G). "
                "Pilihlah obat oles topikal dengan penyerapan sistemik minimal."
            ),
            "severity": "BAHAYA_TINGGI"
        })

    # 7. FILTER KHUSUS BAYI (< 1 TAHUN)
    if group == "BAYI":
        warnings.append({
            "category": "PERINGATAN_USIA",
            "title": "Sensitivitas Kulit Bayi",
            "warning_message": (
                "Kulit bayi 30% lebih tipis daripada kulit dewasa sehingga sangat cepat menyerap obat topikal ke aliran darah. "
                "Hindari penggunaan salep kortikosteroid potensi sedang-tinggi atau losion kutu Permethrin tanpa pengawasan dokter spesialis anak."
            ),
            "severity": "PERINGATAN_SEDANG"
        })

    return warnings
