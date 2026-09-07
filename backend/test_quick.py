"""
Skrip Uji Mandiri Cepat (Standalone Verification)
Memverifikasi modul pra-pemrosesan citra, model klasifikasi,
Explainable AI (Grad-CAM), dan aturan triase tanpa dependensi eksternal tambahan.
"""

import sys
import os
import io
import numpy as np
import cv2

# Tambahkan direktori saat ini ke sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.ml.model import classifier_instance
from app.ml.gradcam import GradCAMVisualizer
from app.core.triage_rules import evaluate_triage, TriageLevel
from app.core.first_aid_guide import CONDITIONS_KNOWLEDGE_BASE

def test_quick():
    print("==================================================")
    print("   MEMULAI VERIFIKASI MANDIRI BACKEND AI...")
    print("==================================================")

    # 1. Uji Basis Pengetahuan P3K
    print("\n[1/4] Menguji Basis Pengetahuan Medis...")
    assert len(CONDITIONS_KNOWLEDGE_BASE) >= 5, "Jumlah kondisi minimal 5"
    print("  -> Terdeteksi 5 kondisi:")
    for k, v in CONDITIONS_KNOWLEDGE_BASE.items():
        print(f"     - {k}: {v['nama_umum']}")

    # 2. Uji Aturan Triase Medis
    print("\n[2/4] Menguji Aturan Triase Medis (Lampu Lalu Lintas)...")
    res_red = evaluate_triage("LUKA_ROBEK", confidence=0.85, has_tetanus_risk=True)
    assert res_red["level"] == TriageLevel.RED.value, "Risiko tetanus harus menghasilkan level MERAH"
    print(f"  -> Uji Kasus Risiko Tetanus: Level {res_red['level']} ({res_red['badge_color']}) [OK]")

    res_green = evaluate_triage("LUKA_LECET", confidence=0.80)
    assert res_green["level"] == TriageLevel.GREEN.value, "Luka lecet ringan harus level HIJAU"
    print(f"  -> Uji Kasus Lecet Ringan: Level {res_green['level']} ({res_green['badge_color']}) [OK]")

    # 3. Uji Model Inferensi & Ekstraksi Fitur
    print("\n[3/4] Menguji Inferensi Citra Model...")
    # Buat gambar sintetis luka gores merah di atas kulit
    img = np.full((250, 250, 3), (160, 195, 235), dtype=np.uint8)
    cv2.circle(img, (125, 125), 35, (20, 20, 210), -1) # Darah merah
    cv2.line(img, (100, 110), (150, 140), (10, 10, 160), 4)

    best_class, conf, mask = classifier_instance.predict(img)
    print(f"  -> Hasil Prediksi: {best_class}")
    print(f"  -> Confidence: {conf * 100:.1f}%")
    assert best_class in CONDITIONS_KNOWLEDGE_BASE, "Kelas harus terdaftar di basis pengetahuan"

    # 4. Uji Explainable AI (Grad-CAM Heatmap)
    print("\n[4/4] Menguji Explainable AI (Grad-CAM Overlay)...")
    vis = GradCAMVisualizer()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    overlay, b64 = vis.generate_heatmap_overlay(img_rgb, salient_mask=mask)

    assert overlay.shape == img.shape, "Dimensi overlay harus sama dengan gambar asli"
    assert b64.startswith("data:image/jpeg;base64,"), "Base64 harus berawalan data URL valid"
    print(f"  -> Visualisasi Heatmap Berhasil: Ukuran {overlay.shape}, Base64 Length: {len(b64)} karakter")

    print("\n==================================================")
    print("   SEMUA PENGUJIAN LOGIKA & AI BERHASIL 100%!")
    print("==================================================")

if __name__ == "__main__":
    test_quick()
