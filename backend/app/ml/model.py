"""
Modul Model Klasifikasi Dermatologi & Luka Komprehensif
Mendukung:
1. Analisis Vision AI Canggih (Gemini Multimodal Vision API via HTTP)
2. Ekstraksi Fitur Klinis Lokal (Computer Vision + Gejala Subjektif)
3. Deteksi Kulit Normal / Tanpa Kelainan (Mencegah false positive seperti salah tebak Panu)
"""

import os
import json
import base64
import numpy as np
import cv2
import httpx
from typing import Dict, Any, Tuple, Optional
from app.ml.gradcam import GradCAMVisualizer
from app.ml.preprocessor import extract_skin_mask
from app.ml.morphology import extract_morphology_features
from app.core.first_aid_guide import CONDITIONS_KNOWLEDGE_BASE

CLASSES = list(CONDITIONS_KNOWLEDGE_BASE.keys())

class WoundClassifier:
    def __init__(self, weights_path: str = None):
        self.weights_path = weights_path
        self.classes = CLASSES
        self.gradcam = GradCAMVisualizer()

    async def analyze_with_gemini(
        self,
        image_bytes: bytes,
        api_key: str,
        symptom_context: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Menggunakan Gemini Vision untuk menganalisis kelainan kulit / luka secara presisi tinggi.
        """
        if not api_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        b64_image = base64.b64encode(image_bytes).decode('utf-8')

        system_instruction = (
            "Anda adalah asisten triase medis dan dermatologi spesialis sistem integumen (kulit, kuku, rambut, dan luka traumatologi) bersertifikasi.\n"
            "Analisis foto yang diberikan dan klasifikasikan ke dalam SALAH SATU dari 27 kondisi berikut:\n"
            "1. LUKA FISIK & TRAUMA:\n"
            "   - 'LUKA_TUSUK_PUNCTURE' (tertusuk paku/duri/jarum, lubang tusukan dalam)\n"
            "   - 'LUKA_GIGITAN_HEWAN' (gigitan/cakaran anjing, kucing, kera, risiko rabies)\n"
            "   - 'LUKA_BAKAR_BERAT_DERAJAT_3' (kulit hangus hitam gosong atau putih lilin mati rasa)\n"
            "   - 'LUKA_BAKAR' / 'LUKA_BAKAR_RINGAN' (luka bakar derajat 1-2, melepuh gelembung bula air knalpot/minyak)\n"
            "   - 'LUKA_MEMAR_KONTUSIO' (benturan tumpul, lebam ungu/biru tanpa luka robek terbuka)\n"
            "   - 'LUKA_TEKAN_DEKUBITUS' (borok tirah baring/dekubitus pada tonjolan tulang/sakrum)\n"
            "   - 'LUKA_SAYAT_IRIS' (sayatan rapi lurus pisau/silet/kaca)\n"
            "   - 'LUKA_ROBEK' (robekan terbuka tepi tak beraturan akibat benturan keras)\n"
            "   - 'LUKA_LECET' (abrasi gesekan aspal/semen, keropeng merah-cokelat)\n"
            "2. ADNEKSA KUKU:\n"
            "   - 'CANTENGAN_PARONIKIA' (bengkak merah bernanah lipatan kuku menusuk daging)\n"
            "   - 'JAMUR_KUKU_ONIKOMIKOSIS' (kuku menebal, rapuh, kuning kecokelatan berkapur)\n"
            "   - 'HEMATOMA_KUKU_KEJEPIT' (bercak darah hitam/ungu di bawah kuku akibat terjepit)\n"
            "3. ADNEKSA RAMBUT & KEPALA:\n"
            "   - 'KETOMBE_SEBOROIK' (sisik ketombe tebal berminyak kekuningan berkerak di kulit kepala)\n"
            "   - 'ALOPECIA_KEBOTAKAN' (kebotakan koin pitak licin mendadak berbatas tegas)\n"
            "   - 'KUTU_RAMBUT_PEDIKULOSIS' (bintik oval telur kutu putih melekat di helai rambut)\n"
            "4. DERMATOLOGI & RUAM GATAL:\n"
            "   - 'CACAR_AIR_VARICELLA' (lenting gelembung air tetesan embun menyebar)\n"
            "   - 'HERPES_ZOSTER' (lenting bergerombol unilateral satu sisi dermatom saraf)\n"
            "   - 'BIDURAN_URTIKARIA' (bentol merah menonjol padat wheal)\n"
            "   - 'EKSIM_DERMATITIS' (kulit sangat kering bersisik menebal gatal kronis)\n"
            "   - 'KUDIS_SKABIES' (bintik merah sela jari gatal hebat malam hari)\n"
            "   - 'KURAP_KADAS' (ruam cincin tepi merah aktif central clearing)\n"
            "   - 'GIGITAN_SERANGGA', 'BIANG_KERINGAT', 'JERAWAT_ACNE', 'PANU', 'BISUL'\n"
            "5. NORMAL: 'KULIT_NORMAL' (kulit intak sehat tanpa lesi aktif patologis)\n\n"
            "Jawab HANYA dalam format JSON valid:\n"
            "{\n"
            '  "condition_key": "KUNCI_KONDISI",\n'
            '  "confidence": 0.95,\n'
            '  "clinical_observation": "Penjelasan ringkas tanda patologis yang terlihat",\n'
            '  "focal_point": {"x": 0.5, "y": 0.5, "radius": 0.2}\n'
            "}"
        )

        prompt_text = f"Analisis gambar kulit/luka ini. Konteks gejala tambahan pasien: {symptom_context}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": system_instruction + "\n\n" + prompt_text},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": b64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "response_mime_type": "application/json"
            }
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(raw_text)
                    if parsed.get("condition_key") in CONDITIONS_KNOWLEDGE_BASE:
                        return parsed
        except Exception:
            pass

        return None

    def analyze_tissue_composition(self, image_bgr: np.ndarray, skin_mask: np.ndarray) -> Dict[str, Any]:
        """
        Analisis Jaringan Luka Berdasarkan Standar Medis Internasional (TIME Framework)
        """
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        h, w = image_bgr.shape[:2]

        lower_r1 = np.array([0, 70, 50])
        upper_r1 = np.array([12, 255, 255])
        lower_r2 = np.array([168, 70, 50])
        upper_r2 = np.array([180, 255, 255])
        raw_mask_r = cv2.bitwise_or(cv2.inRange(hsv, lower_r1, upper_r1), cv2.inRange(hsv, lower_r2, upper_r2))

        # Luaskan daerah kulit efektif dengan mengisi kontur bagian dalam (luka/lesi di atas permukaan kulit)
        contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filled_skin = np.zeros_like(skin_mask)
        if contours:
            cv2.drawContours(filled_skin, contours, -1, 255, -1)
        effective_mask = cv2.bitwise_or(skin_mask, cv2.bitwise_or(raw_mask_r, filled_skin))

        mask_r = cv2.bitwise_and(raw_mask_r, effective_mask)

        lower_y = np.array([18, 50, 80])
        upper_y = np.array([35, 255, 255])
        mask_y = cv2.bitwise_and(cv2.inRange(hsv, lower_y, upper_y), effective_mask)

        lower_b = np.array([0, 0, 0])
        upper_b = np.array([180, 255, 55])
        mask_b = cv2.bitwise_and(cv2.inRange(hsv, lower_b, upper_b), effective_mask)

        count_r = np.sum(mask_r > 0)
        count_y = np.sum(mask_y > 0)
        count_b = np.sum(mask_b > 0)
        total_lesion_pixels = count_r + count_y + count_b

        if total_lesion_pixels > 0:
            pct_granulation = round((count_r / total_lesion_pixels) * 100, 1)
            pct_slough = round((count_y / total_lesion_pixels) * 100, 1)
            pct_necrotic = round((count_b / total_lesion_pixels) * 100, 1)
        else:
            pct_granulation = 80.0
            pct_slough = 18.0
            pct_necrotic = 2.0

        pixel_to_cm2_factor = 4225.0
        estimated_area = round(max(0.2, total_lesion_pixels / pixel_to_cm2_factor), 1)

        if estimated_area < 2.0:
            severity = "Kecil / Superfisial"
        elif estimated_area < 6.0:
            severity = "Sedang"
        else:
            severity = "Luas / Membutuhkan Perhatian Khusus"

        return {
            "granulation_percentage": pct_granulation,
            "slough_percentage": pct_slough,
            "necrotic_percentage": pct_necrotic,
            "estimated_area_cm2": estimated_area,
            "severity_classification": severity,
            "lesion_mask": mask_r if count_r >= count_y else mask_y
        }

    def predict_local(
        self,
        image_bgr: np.ndarray,
        complaint_category: str = "AUTO",
        body_location: str = "AUTO",
        # Gejala Kulit & Ruam
        symptom_itch: bool = False,
        symptom_night_itch: bool = False,
        symptom_wheal_bumps: bool = False,
        symptom_ring_circle: bool = False,
        symptom_dry_scaly: bool = False,
        symptom_vesicles_blister: bool = False,
        is_deep_cut: bool = False,
        # Gejala Kuku
        symptom_nail_ingrown: bool = False,
        symptom_nail_fungus: bool = False,
        symptom_nail_trauma: bool = False,
        # Gejala Rambut & Kulit Kepala
        symptom_scalp_dandruff: bool = False,
        symptom_hair_loss_patch: bool = False,
        symptom_head_lice: bool = False,
        # Gejala Ragam Luka Fisik
        symptom_puncture_nail: bool = False,
        symptom_animal_bite: bool = False,
        symptom_burn_blister: bool = False,
        symptom_burn_charred: bool = False,
        symptom_bruise_blunt: bool = False,
        symptom_bedsores: bool = False,
        symptom_clean_cut: bool = False
    ) -> Tuple[str, float, np.ndarray, Dict[str, Any], list, Dict[str, Any]]:
        """
        Klasifikasi Bertingkat 2-Tahap dengan Analisis Morfologi dan Konteks Anatomi:
        - Ekstraksi Fitur Morfologi (Vesikel Cacar/Herpes, Cincin Kurap, Keropeng Kasar, Lubang Tusuk)
        - Pembobotan Lokasi Tubuh (Anatomical Priors: Sela Jari, Lutut, Kuku, Kulit Kepala, Pinggang)
        - Generasi Top-3 Differential Diagnosis (DDx)
        """
        skin_mask = extract_skin_mask(image_bgr)
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        h, w = image_bgr.shape[:2]

        tissue_info = self.analyze_tissue_composition(image_bgr, skin_mask)
        skin_pixel_count = max(1, np.sum(skin_mask > 0))

        # Ekstraksi Fitur Morfologi Lanjutan
        morphology_dict = extract_morphology_features(image_bgr, skin_mask)

        # 1. Ekstraksi Fitur Warna & Tekstur
        lower_r1 = np.array([0, 70, 50])
        upper_r1 = np.array([12, 255, 255])
        lower_r2 = np.array([168, 70, 50])
        upper_r2 = np.array([180, 255, 255])
        red_mask = cv2.bitwise_or(cv2.inRange(hsv, lower_r1, upper_r1), cv2.inRange(hsv, lower_r2, upper_r2))
        red_mask_skin = cv2.bitwise_and(red_mask, skin_mask)
        red_ratio = float(np.sum(red_mask_skin > 0) / skin_pixel_count)

        # Deteksi Krusta/Keropeng Luka Jatuh (Scab)
        lower_scab = np.array([0, 60, 20])
        upper_scab = np.array([20, 255, 140])
        scab_mask = cv2.inRange(hsv, lower_scab, upper_scab)
        scab_mask_skin = cv2.bitwise_and(scab_mask, skin_mask)
        scab_ratio = float(np.sum(scab_mask_skin > 0) / skin_pixel_count)

        # Deteksi Sisik Putih / Ketombe
        lower_white = np.array([0, 0, 160])
        upper_white = np.array([180, 45, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        white_mask_skin = cv2.bitwise_and(white_mask, skin_mask)
        white_ratio = float(np.sum(white_mask_skin > 0) / skin_pixel_count)

        # Deteksi Diskontinuitas Tepi (Goresan/Sayatan)
        edges = cv2.Canny(gray, 40, 140)
        edges_skin = cv2.bitwise_and(edges, skin_mask)
        edge_density = float(np.sum(edges_skin > 0) / skin_pixel_count)

        # ----------------------------------------------------
        # TAHAP 1: DETERMINASI DOMAIN MAKRO (STAGE 1 MACRO)
        # ----------------------------------------------------
        has_wound_symptoms = (
            symptom_puncture_nail or symptom_animal_bite or symptom_burn_blister or 
            symptom_burn_charred or symptom_bruise_blunt or symptom_bedsores or 
            symptom_clean_cut or is_deep_cut
        )
        has_gatal_symptoms = (
            symptom_itch or symptom_wheal_bumps or symptom_night_itch or 
            symptom_ring_circle or symptom_dry_scaly or symptom_vesicles_blister
        )
        has_nail_symptoms = symptom_nail_ingrown or symptom_nail_fungus or symptom_nail_trauma
        has_hair_symptoms = symptom_scalp_dandruff or symptom_hair_loss_patch or symptom_head_lice

        if complaint_category == "KUKU" or body_location == "KUKU_JARI" or has_nail_symptoms:
            macro_domain = "KUKU"
        elif complaint_category == "RAMBUT" or (body_location == "KEPALA_WAJAH" and has_hair_symptoms):
            macro_domain = "RAMBUT"
        elif complaint_category == "LUKA":
            macro_domain = "LUKA"
        elif complaint_category == "GATAL":
            macro_domain = "GATAL"
        else:
            # Mode AUTO: Evaluasi prioritas klinis, gejala, dan morfologi CV
            if has_wound_symptoms:
                macro_domain = "LUKA"
            elif has_gatal_symptoms:
                macro_domain = "GATAL"
            elif body_location == "LUTUT_SIKU_KAKI" and (scab_ratio > 0.02 or edge_density > 0.03):
                macro_domain = "LUKA"
            elif morphology_dict["has_vesicles"] or morphology_dict["has_annular_ring"]:
                macro_domain = "GATAL"
            elif morphology_dict["is_punctate_wound"]:
                macro_domain = "LUKA"
            elif scab_ratio > 0.04 and edge_density > 0.04 and body_location != "DADA_PERUT":
                macro_domain = "LUKA"
            elif red_ratio > 0.04 or white_ratio > 0.08:
                macro_domain = "GATAL"
            elif red_ratio < 0.03 and white_ratio < 0.05 and edge_density < 0.03 and scab_ratio < 0.01:
                macro_domain = "NORMAL"
            else:
                macro_domain = "NORMAL"

        # ----------------------------------------------------
        # TAHAP 2: SPESIALISASI KONDISI MIKRO (STAGE 2 MICRO)
        # ----------------------------------------------------
        scores: Dict[str, float] = {k: 0.02 for k in CLASSES}

        # DOMAIN 1: KUKU
        if macro_domain == "KUKU":
            if symptom_nail_trauma:
                scores["HEMATOMA_KUKU_KEJEPIT"] = 0.96
            elif symptom_nail_fungus:
                scores["JAMUR_KUKU_ONIKOMIKOSIS"] = 0.96
            elif symptom_nail_ingrown:
                scores["CANTENGAN_PARONIKIA"] = 0.96
            else:
                if scab_ratio > 0.02 or tissue_info["necrotic_percentage"] > 8:
                    scores["HEMATOMA_KUKU_KEJEPIT"] = 0.90
                    scores["CANTENGAN_PARONIKIA"] = 0.40
                elif tissue_info["slough_percentage"] > 20 or white_ratio > 0.10:
                    scores["JAMUR_KUKU_ONIKOMIKOSIS"] = 0.90
                    scores["CANTENGAN_PARONIKIA"] = 0.35
                else:
                    scores["CANTENGAN_PARONIKIA"] = 0.88
                    scores["JAMUR_KUKU_ONIKOMIKOSIS"] = 0.30

        # DOMAIN 2: RAMBUT & KULIT KEPALA
        elif macro_domain == "RAMBUT":
            if symptom_hair_loss_patch:
                scores["ALOPECIA_KEBOTAKAN"] = 0.96
            elif symptom_head_lice:
                scores["KUTU_RAMBUT_PEDIKULOSIS"] = 0.96
            elif symptom_scalp_dandruff:
                scores["KETOMBE_SEBOROIK"] = 0.96
            else:
                if white_ratio > 0.08:
                    scores["KETOMBE_SEBOROIK"] = 0.88
                    scores["KUTU_RAMBUT_PEDIKULOSIS"] = 0.35
                elif edge_density < 0.02 and red_ratio < 0.03:
                    scores["ALOPECIA_KEBOTAKAN"] = 0.88
                else:
                    scores["KUTU_RAMBUT_PEDIKULOSIS"] = 0.85
                    scores["KETOMBE_SEBOROIK"] = 0.35

        # DOMAIN 3: LUKA FISIK & TRAUMATOLOGI
        elif macro_domain == "LUKA":
            if symptom_puncture_nail or morphology_dict["is_punctate_wound"]:
                scores["LUKA_TUSUK_PUNCTURE"] = 0.96
                scores["LUKA_ROBEK"] = 0.25
            elif symptom_animal_bite:
                scores["LUKA_GIGITAN_HEWAN"] = 0.96
                scores["LUKA_ROBEK"] = 0.30
            elif symptom_burn_charred:
                scores["LUKA_BAKAR_BERAT_DERAJAT_3"] = 0.96
            elif symptom_burn_blister:
                scores["LUKA_BAKAR"] = 0.95
            elif symptom_bruise_blunt or body_location == "LUTUT_SIKU_KAKI" and red_ratio < 0.03 and scab_ratio < 0.01:
                scores["LUKA_MEMAR_KONTUSIO"] = 0.95
            elif symptom_bedsores:
                scores["LUKA_TEKAN_DEKUBITUS"] = 0.95
            elif symptom_clean_cut:
                scores["LUKA_SAYAT_IRIS"] = 0.94
            elif is_deep_cut:
                scores["LUKA_ROBEK"] = 0.92
                scores["LUKA_SAYAT_IRIS"] = 0.30
            elif scab_ratio > 0.03 or morphology_dict["is_rough_scab"] or body_location == "LUTUT_SIKU_KAKI":
                scores["LUKA_LECET"] = 0.94
                scores["LUKA_ROBEK"] = 0.28
                scores["LUKA_MEMAR_KONTUSIO"] = 0.22
            else:
                scores["LUKA_LECET"] = 0.78
                scores["LUKA_BAKAR"] = 0.25

        # DOMAIN 4: DERMATOLOGI & RUAM GATAL
        elif macro_domain == "GATAL":
            # Morfologi vesikel (gelembung air berkilap)
            if morphology_dict["has_vesicles"] or symptom_vesicles_blister:
                if body_location == "PINGGANG_DERMATOM":
                    scores["HERPES_ZOSTER"] = 0.95
                    scores["CACAR_AIR_VARICELLA"] = 0.65
                else:
                    scores["CACAR_AIR_VARICELLA"] = 0.95
                    scores["HERPES_ZOSTER"] = 0.68
                scores["BIDURAN_URTIKARIA"] = 0.15
            # Morfologi cincin kurap
            elif morphology_dict["has_annular_ring"] or symptom_ring_circle:
                scores["KURAP_KADAS"] = 0.94
                scores["PANU"] = 0.35
                scores["EKSIM_DERMATITIS"] = 0.25
            # Anatomi sela jari (kudis)
            elif body_location == "SELA_JARI_TANGAN" or symptom_night_itch:
                scores["KUDIS_SKABIES"] = 0.95
                scores["EKSIM_DERMATITIS"] = 0.35
            elif symptom_wheal_bumps or morphology_dict["is_smooth_wheal"]:
                scores["BIDURAN_URTIKARIA"] = 0.92
                scores["GIGITAN_SERANGGA"] = 0.35
            elif symptom_dry_scaly:
                scores["EKSIM_DERMATITIS"] = 0.90
                scores["KURAP_KADAS"] = 0.30
            elif white_ratio > 0.12 or body_location == "PUNGGUNG" and white_ratio > 0.06:
                scores["PANU"] = 0.90
                scores["KURAP_KADAS"] = 0.25
            elif symptom_itch and red_ratio > 0.04:
                scores["BIDURAN_URTIKARIA"] = 0.60
                scores["BIANG_KERINGAT"] = 0.35
                scores["GIGITAN_SERANGGA"] = 0.30
            else:
                scores["BIDURAN_URTIKARIA"] = 0.50
                scores["GIGITAN_SERANGGA"] = 0.35
                scores["BIANG_KERINGAT"] = 0.25

        # DOMAIN 5: NORMAL
        else:
            scores["KULIT_NORMAL"] = 0.92

        # Pembobotan Prior Anatomi Tambahan (Body Map Bayesian contextual boost)
        if body_location == "KEPALA_WAJAH":
            if macro_domain == "GATAL":
                scores["JERAWAT_ACNE"] = max(scores.get("JERAWAT_ACNE", 0.0), 0.70)
        elif body_location == "PINGGANG_DERMATOM":
            scores["HERPES_ZOSTER"] = max(scores.get("HERPES_ZOSTER", 0.0), 0.82)
        elif body_location == "SELA_JARI_TANGAN":
            scores["KUDIS_SKABIES"] = max(scores.get("KUDIS_SKABIES", 0.0), 0.85)

        # Normalisasi probabilitas softmax
        exp_scores = {k: np.exp(v * 3.5) for k, v in scores.items()}
        sum_exp = sum(exp_scores.values())
        probs = {k: float(v / sum_exp) for k, v in exp_scores.items()}

        best_class = max(probs, key=probs.get)
        confidence = probs[best_class]

        # Bentuk Top-3 Differential Diagnosis (DDx)
        sorted_probs = sorted(probs.items(), key=lambda item: item[1], reverse=True)
        top3_differential = []
        for rank, (ckey, cprob) in enumerate(sorted_probs[:3]):
            cinfo = CONDITIONS_KNOWLEDGE_BASE.get(ckey, CONDITIONS_KNOWLEDGE_BASE["KULIT_NORMAL"])
            if rank == 0:
                rationale = "Temuan visual dan morfologi paling bersesuaian dengan karakteristik patologis utama."
            elif rank == 1:
                rationale = "Dipertimbangkan sebagai diagnosis banding sekunder karena kemiripan pola reaksi inflamasi/eritema."
            else:
                rationale = "Diferensial sekunder yang perlu dipantau jika keluhan tidak membaik dalam 3-5 hari."

            top3_differential.append({
                "condition_key": ckey,
                "common_name": cinfo["nama_umum"],
                "medical_name": cinfo["nama_medis"],
                "probability": round(cprob, 4),
                "percentage": f"{round(cprob * 100, 1)}%",
                "clinical_rationale": rationale
            })

        # Salient mask untuk Grad-CAM
        salient_mask = None
        if best_class == "KULIT_NORMAL":
            salient_mask = (skin_mask.astype(np.float32) / 255.0) * 0.2
        else:
            active_mask = red_mask_skin if np.max(red_mask_skin) > 0 else tissue_info["lesion_mask"]
            if np.max(active_mask) > 0:
                blurred = cv2.GaussianBlur(active_mask.astype(np.float32), (45, 45), 0)
                salient_mask = blurred / (np.max(blurred) + 1e-5)

        return best_class, confidence, salient_mask, tissue_info, top3_differential, morphology_dict

def analyze_abcde(image_bgr: np.ndarray, lesion_mask: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """
    Kalkulator Skrining ABCDE Kanker Kulit / Melanoma:
    - A (Asymmetry): Rasio asimetri kontur terhadap sumbu utama
    - B (Border): Border irregularity index
    - C (Color): Variasi standar deviasi warna polikromatik
    - D (Diameter): Estimasi diameter terpanjang lesi (mm)
    - E (Elevation / Evolving Risk)
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    if lesion_mask is None or np.sum(lesion_mask > 0) < 50:
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        lesion_mask = thresh

    contours, _ = cv2.findContours(lesion_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return {
            "has_pigmented_lesion": False,
            "risk_level": "RENDAH",
            "asymmetry_score": 0.1,
            "border_score": 1.1,
            "color_variation_score": 15.0,
            "diameter_mm": 2.0,
            "recommendation": "Tidak terdeteksi lesi berpigmen gelap yang mencurigakan.",
            "risk_points": 0
        }

    largest_cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_cnt)
    perimeter = cv2.arcLength(largest_cnt, True)

    asymmetry_score = 0.2
    if len(largest_cnt) >= 5 and area > 100:
        ellipse = cv2.fitEllipse(largest_cnt)
        (center, (major_axis, minor_axis), angle) = ellipse
        if major_axis > 0:
            asymmetry_score = round(1.0 - (minor_axis / major_axis), 2)

    if area > 0:
        compactness = (perimeter ** 2) / (4 * np.pi * area)
        border_score = round(min(5.0, compactness), 2)
    else:
        border_score = 1.0

    lesion_pixels = image_bgr[lesion_mask > 0]
    color_std = np.std(lesion_pixels, axis=0) if len(lesion_pixels) > 0 else np.array([0, 0, 0])
    color_var_score = round(float(np.mean(color_std)), 1)

    pixel_to_mm = 0.08
    rect = cv2.minAreaRect(largest_cnt)
    max_dim_pixels = max(rect[1]) if len(rect[1]) > 0 else 10
    diameter_mm = round(max_dim_pixels * pixel_to_mm, 1)

    risk_points = 0
    if asymmetry_score > 0.45: risk_points += 1
    if border_score > 1.6: risk_points += 1
    if color_var_score > 35: risk_points += 1
    if diameter_mm > 6.0: risk_points += 1

    if risk_points >= 3:
        risk_level = "TINGGI (Waspada Neoplasma / Melanoma)"
        recommendation = "Bercak tahi lalat memiliki karakteristik ABCDE yang mencurigakan. Segera periksakan ke Dokter Spesialis Kulit (Sp.D.V.E) untuk pemeriksaan dermoskopi!"
    elif risk_points == 2:
        risk_level = "SEDANG (Perlu Observasi Rutin)"
        recommendation = "Terdapat sedikit ketidakteraturan kontur/warna. Pantau apakah lesi membesar atau berubah bentuk dalam 3 bulan ke depan."
    else:
        risk_level = "RENDAH (Lesi Jinak / Nevus Normal)"
        recommendation = "Struktur lesi berbatas teratur dan simetris, kemungkinan besar tahi lalat jinak (nevus pigmentosus)."

    return {
        "has_pigmented_lesion": True,
        "risk_level": risk_level,
        "asymmetry_score": asymmetry_score,
        "border_score": border_score,
        "color_variation_score": color_var_score,
        "diameter_mm": diameter_mm,
        "recommendation": recommendation,
        "risk_points": risk_points
    }

def generate_adaptive_questions(condition_key: str) -> list:
    """
    Anamnesis Adaptif Medis Dinamis (CDSS):
    Menghasilkan 2-3 pertanyaan medis spesifik berbasis temuan visual.
    """
    questions_map = {
        "LUKA_TUSUK_PUNCTURE": [
            {
                "id": "q_rusted",
                "question": "Apakah benda yang menusuk (misal paku/kawat) dalam kondisi berkarat atau tercampur tanah?",
                "options": ["Ya, berkarat / kotor", "Tidak, benda baru/bersih", "Ragu-ragu / Tidak yakin"]
            },
            {
                "id": "q_tetanus_shot",
                "question": "Kapan terakhir kali Anda menerima suntikan vaksin tetanus (TT) atau serum anti-tetanus?",
                "options": ["Lebih dari 5 tahun lalu / Belum pernah", "Kurang dari 5 tahun lalu", "Lupa"]
            }
        ],
        "LUKA_GIGITAN_HEWAN": [
            {
                "id": "q_rabies_animal",
                "question": "Apakah hewan yang menggigit/mencakar adalah hewan liar (tidak bertuan) atau bertingkah agresif?",
                "options": ["Ya, hewan liar / mencurigakan", "Tidak, hewan peliharaan sehat tervaksin", "Tidak tahu"]
            },
            {
                "id": "q_wash_soap",
                "question": "Apakah luka gigitan sudah langsung dicuci dengan sabun dan air mengalir selama minimal 15 menit?",
                "options": ["Sudah, dicuci sabun 15 menit", "Hanya dicuci air sebentar", "Belum dicuci sama sekali"]
            }
        ],
        "LUKA_BAKAR_BERAT_DERAJAT_3": [
            {
                "id": "q_burn_numbness",
                "question": "Apakah area kulit yang hangus kehitaman atau putih lilin tersebut terasa kebas/mati rasa saat disentuh?",
                "options": ["Ya, mati rasa / tidak sakit", "Masih sangat perih/nyeri", "Nyeri berdenyut"]
            },
            {
                "id": "q_burn_inhalation",
                "question": "Apakah Anda sempat menghirup asap tebal, batuk jelaga hitam, atau mengalami sesak napas?",
                "options": ["Ya, ada sesak / terpapar asap tebal", "Tidak ada keluhan napas"]
            }
        ],
        "LUKA_MEMAR_KONTUSIO": [
            {
                "id": "q_bone_joint",
                "question": "Apakah bagian yang memar terasa ngilu hebat pada tulang atau sendi di dekatnya tidak bisa digerakkan?",
                "options": ["Ya, dicurigai retak / patah tulang", "Hanya nyeri otot biasa saat ditekan"]
            },
            {
                "id": "q_massage",
                "question": "Apakah memar sempat dipijat atau diurut keras sebelumnya?",
                "options": ["Tidak dipijat (sesuai anjuran)", "Sempat dipijat/diurut"]
            }
        ],
        "LUKA_TEKAN_DEKUBITUS": [
            {
                "id": "q_mobility",
                "question": "Apakah pasien mengalami keterbatasan gerak fisik (tirah baring lama / stroke / pengguna kursi roda)?",
                "options": ["Ya, tirah baring lama", "Tidak, masih bisa beraktivitas mandiri"]
            },
            {
                "id": "q_odor",
                "question": "Apakah luka borok mengeluarkan cairan nanah dengan aroma menyengat yang khas?",
                "options": ["Ya, berbau menyengat", "Tidak berbau busuk"]
            }
        ],
        "LUKA_SAYAT_IRIS": [
            {
                "id": "q_tendon_numb",
                "question": "Apakah ada bagian jari atau area setelah sayatan yang mati rasa atau tidak bisa ditekuk?",
                "options": ["Tidak, gerakan jari normal", "Ya, jari kaku/kebas"]
            }
        ],
        "CANTENGAN_PARONIKIA": [
            {
                "id": "q_pulsing_pain",
                "question": "Apakah tepi kuku terasa berdenyut hebat hingga mengganggu aktivitas tidur malam?",
                "options": ["Ya, berdenyut hebat", "Hanya nyeri saat tertekan sepatu"]
            }
        ],
        "CACAR_AIR_VARICELLA": [
            {
                "id": "q_rash_progression",
                "question": "Apakah lenting gelembung air muncul pertama kali di dada/perut/punggung lalu menyebar ke wajah dan lengan?",
                "options": ["Ya, menyebar dari badan ke luar", "Hanya di satu area tertentu"]
            },
            {
                "id": "q_history_pox",
                "question": "Apakah pasien sudah pernah menderita cacar air sebelumnya?",
                "options": ["Belum pernah (baru pertama kali)", "Sudah pernah sewaktu kecil"]
            }
        ],
        "BIDURAN_URTIKARIA": [
            {
                "id": "q_urticaria_shift",
                "question": "Apakah bentol-bentol merah timbul mendadak dan bisa hilang-timbul berpindah tempat dalam hitungan jam?",
                "options": ["Ya, bentol berpindah tempat cepat", "Bercak menetap di satu tempat"]
            }
        ],
        "KUDIS_SKABIES": [
            {
                "id": "q_household_itch",
                "question": "Apakah ada anggota keluarga, teman sekamar, atau rekan asrama yang mengalami keluhan gatal serupa?",
                "options": ["Ya, ada orang lain yang gatal juga", "Hanya saya sendiri"]
            }
        ]
    }

    default_questions = [
        {
            "id": "q_duration",
            "question": "Sudah berapa lama keluhan atau luka ini berlangsung?",
            "options": ["Baru terjadi hari ini (< 24 jam)", "1 - 3 hari yang lalu", "Lebih dari 1 minggu"]
        },
        {
            "id": "q_fever_general",
            "question": "Apakah keluhan ini disertai rasa demam, meriang, atau badan lemas?",
            "options": ["Tidak ada demam", "Ya, disertai demam atau meriang"]
        }
    ]

    return questions_map.get(condition_key, default_questions)

# Inisialisasi Singleton Instance
classifier_instance = WoundClassifier()

