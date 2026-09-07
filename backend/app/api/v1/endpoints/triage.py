"""
Endpoint API Triase Medis dan Analisis Citra Dermatologi & Luka
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
import cv2
import numpy as np
from typing import List, Optional

from app.schemas.triage import (
    TriageAnalysisResponse,
    ConditionDetail,
    TissueAnalysis,
    QualityValidationResult,
    ABCDEAnalysis,
    AdaptiveQuestion,
    ProgressTrackingResponse,
    DifferentialDiagnosisItem,
    DrugSafetyWarning,
    ChatConsultRequest,
    ChatConsultResponse
)
from app.ml.preprocessor import load_image_from_bytes, extract_skin_mask, validate_image_quality
from app.ml.model import classifier_instance, analyze_abcde, generate_adaptive_questions
from app.ml.gradcam import GradCAMVisualizer
from app.ml.morphology import extract_morphology_features
from app.core.first_aid_guide import CONDITIONS_KNOWLEDGE_BASE
from app.core.triage_rules import evaluate_triage
from app.core.safety_checker import evaluate_drug_safety
from app.core.config import settings
import httpx
import json

router = APIRouter()
gradcam_visualizer = GradCAMVisualizer()

@router.post("/analyze", response_model=TriageAnalysisResponse)
async def analyze_wound_image(
    request: Request,
    file: UploadFile = File(..., description="Foto kulit, ruam gatal, atau luka (JPG/PNG/WEBP)"),
    gemini_api_key: Optional[str] = Form(None, description="Kunci API Google Gemini (Opsional untuk akurasi ultra-tinggi)"),
    complaint_category: str = Form("AUTO", description="Kategori keluhan: 'LUKA', 'GATAL', 'KUKU', 'RAMBUT', atau 'AUTO'"),
    body_location: str = Form("AUTO", description="Lokasi anatomi: 'AUTO', 'KEPALA_WAJAH', 'DADA_PERUT', 'PUNGGUNG', 'SELA_JARI_TANGAN', 'LUTUT_SIKU_KAKI', 'KUKU_JARI', 'PINGGANG_DERMATOM'"),
    patient_group: str = Form("DEWASA", description="Kelompok demografi pasien: 'DEWASA', 'ANAK', 'BAYI', 'HAMIL_MENYUSUI'"),
    
    # Gejala Klinis Gatal & Ruam
    symptom_itch: bool = Form(False, description="Apakah terasa gatal aktif?"),
    symptom_night_itch: bool = Form(False, description="Apakah rasa gatal jauh lebih parah di malam hari? (Ciri khas Kudis/Skabies)"),
    symptom_wheal_bumps: bool = Form(False, description="Apakah timbul bentol-bentol merah menonjol tiba-tiba? (Ciri khas Biduran)"),
    symptom_ring_circle: bool = Form(False, description="Apakah ruam berbentuk cincin melingkar dengan tepi merah? (Ciri khas Kurap)"),
    symptom_dry_scaly: bool = Form(False, description="Apakah kulit sangat kering, bersisik, atau pecah-pecah? (Ciri khas Eksim)"),
    symptom_vesicles_blister: bool = Form(False, description="Apakah tampak lenting/gelembung kecil berisi cairan bening? (Ciri khas Cacar Air / Herpes)"),
    
    # Gejala Kuku (Sistem Integumen Kuku)
    symptom_nail_ingrown: bool = Form(False, description="Tepi kuku bengkak merah menusuk daging (Cantengan / Paronikia)"),
    symptom_nail_fungus: bool = Form(False, description="Kuku menebal rapuh kekuningan berkapur (Jamur Kuku / Onikomikosis)"),
    symptom_nail_trauma: bool = Form(False, description="Kuku terjepit/terbentur timbul bercak darah hitam keunguan (Hematoma Subungual)"),

    # Gejala Rambut & Kulit Kepala (Sistem Integumen Rambut)
    symptom_scalp_dandruff: bool = Form(False, description="Ketombe tebal berkerak berminyak kekuningan (Dermatitis Seboroik)"),
    symptom_hair_loss_patch: bool = Form(False, description="Rambut rontok pitak koin licin mendadak (Alopecia Areata)"),
    symptom_head_lice: bool = Form(False, description="Gatal merayap di kulit kepala dan bintik telur kutu (Pedikulosis Capitis)"),

    # Gejala Ragam Luka Fisik & Trauma Mekanik
    symptom_puncture_nail: bool = Form(False, description="Tertusuk paku/jarum/kawat tajam (Risiko Tetanus)"),
    symptom_animal_bite: bool = Form(False, description="Gigitan atau cakaran hewan liar/peliharaan (Risiko Rabies)"),
    symptom_burn_blister: bool = Form(False, description="Luka bakar melepuh bergelembung cairan (Derajat 2)"),
    symptom_burn_charred: bool = Form(False, description="Luka bakar hangus hitam/putih lilin mati rasa (Derajat 3)"),
    symptom_bruise_blunt: bool = Form(False, description="Benturan tumpul timbul memar lebam kebiruan (Kontusio)"),
    symptom_bedsores: bool = Form(False, description="Luka tekan borok akibat tirah baring/stroke (Dekubitus)"),
    symptom_clean_cut: bool = Form(False, description="Sayatan pisau/kaca tepi lurus rapi (Vulnus Scissum)"),

    # Faktor Risiko Gawat Darurat
    has_tetanus_risk: bool = Form(False, description="Apakah terkena paku/benda berkarat/tanah kotor?"),
    is_bleeding_uncontrolled: bool = Form(False, description="Apakah darah tetap memancar setelah ditekan 10 menit?"),
    is_deep_cut: bool = Form(False, description="Apakah luka terlihat menganga dalam (>0.5 cm)?"),
    is_face_or_joint: bool = Form(False, description="Apakah lokasi kelainan di wajah atau sendi gerak utama?"),
    has_fever: bool = Form(False, description="Apakah disertai demam tinggi atau menggigil?"),
    pain_level: int = Form(3, description="Skala nyeri pasien dari 1 (ringan) sampai 10 (sangat berat)")
):
    """
    Menganalisis foto kulit, luka, kuku, atau rambut dengan dukungan:
    1. Quality Gatekeeper (Blur, Pencahayaan, OOD Non-Kulit)
    2. Hierarchical Two-Stage Computer Vision Model (Anti Salah Tebak Silang Domain)
    3. Gemini Multimodal Vision API (Opsional untuk akurasi ultra-tinggi)
    4. TIME Framework Tissue Decomposition & Triase Darurat
    5. Skrining ABCDE Melanoma & Dynamic Anamnesis CDSS
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File yang diunggah harus berupa citra (JPG, PNG, atau WEBP).")

    image_bytes = await file.read()
    try:
        image_bgr = load_image_from_bytes(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 1. Image Quality & Anatomical Gatekeeper
    quality_dict = validate_image_quality(image_bgr)
    quality_obj = QualityValidationResult(**quality_dict)

    predicted_class = None
    confidence = 0.85
    salient_mask = None
    skin_mask = extract_skin_mask(image_bgr)
    tissue_dict = classifier_instance.analyze_tissue_composition(image_bgr, skin_mask)

    # 2. Coba Analisis dengan Gemini Vision jika API Key diberikan
    if gemini_api_key and gemini_api_key.strip():
        symptoms_str = []
        if symptom_itch: symptoms_str.append("terasa gatal")
        if symptom_night_itch: symptoms_str.append("gatal hebat malam hari")
        if symptom_wheal_bumps: symptoms_str.append("bentol biduran")
        if symptom_ring_circle: symptoms_str.append("ruam cincin melingkar")
        if symptom_dry_scaly: symptoms_str.append("kulit kering bersisik")
        if symptom_vesicles_blister: symptoms_str.append("lenting gelembung kecil berisi cairan bening (cacar/herpes)")
        if symptom_nail_ingrown: symptoms_str.append("cantengan tepi kuku menusuk bengkak nanah")
        if symptom_nail_fungus: symptoms_str.append("jamur kuku menebal rapuh warna kuning kusam")
        if symptom_nail_trauma: symptoms_str.append("kuku terjepit hematoma bercak darah hitam ungu trauma")
        if symptom_scalp_dandruff: symptoms_str.append("ketombe dermatitis seboroik sisik kulit kepala berminyak")
        if symptom_hair_loss_patch: symptoms_str.append("kebotakan pitak bulat koin alopecia areata")
        if symptom_head_lice: symptoms_str.append("kutu rambut pedikulosis dan bintik telur kutu nits")
        if symptom_puncture_nail: symptoms_str.append("tertusuk paku jarum berkarat risiko tetanus")
        if symptom_animal_bite: symptoms_str.append("gigitan cakaran hewan liar anjing kucing rabies")
        if symptom_burn_blister: symptoms_str.append("luka bakar melepuh gelembung air derajat 2")
        if symptom_burn_charred: symptoms_str.append("luka bakar hangus hitam arang derajat 3")
        if symptom_bruise_blunt: symptoms_str.append("luka memar lebam trauma tumpul")
        if symptom_bedsores: symptoms_str.append("luka dekubitus borok tirah baring")
        if symptom_clean_cut: symptoms_str.append("luka sayat iris pisau tepi rapi")

        symptom_context = ", ".join(symptoms_str) if symptoms_str else f"kategori keluhan: {complaint_category}"

        gemini_result = await classifier_instance.analyze_with_gemini(
            image_bytes, gemini_api_key.strip(), symptom_context
        )
        if gemini_result:
            predicted_class = gemini_result["condition_key"]
            confidence = float(gemini_result.get("confidence", 0.92))

    # 3. Jika tidak menggunakan Gemini atau Gemini fallback, jalankan Two-Stage Model lokal
    top3_differential_data = []
    morphology_dict_data = {}

    if not predicted_class:
        predicted_class, confidence, salient_mask, tissue_dict, top3_differential_data, morphology_dict_data = classifier_instance.predict_local(
            image_bgr=image_bgr,
            complaint_category=complaint_category,
            body_location=body_location,
            symptom_itch=symptom_itch,
            symptom_night_itch=symptom_night_itch,
            symptom_wheal_bumps=symptom_wheal_bumps,
            symptom_ring_circle=symptom_ring_circle,
            symptom_dry_scaly=symptom_dry_scaly,
            symptom_vesicles_blister=symptom_vesicles_blister,
            is_deep_cut=is_deep_cut,
            symptom_nail_ingrown=symptom_nail_ingrown,
            symptom_nail_fungus=symptom_nail_fungus,
            symptom_nail_trauma=symptom_nail_trauma,
            symptom_scalp_dandruff=symptom_scalp_dandruff,
            symptom_hair_loss_patch=symptom_hair_loss_patch,
            symptom_head_lice=symptom_head_lice,
            symptom_puncture_nail=symptom_puncture_nail,
            symptom_animal_bite=symptom_animal_bite,
            symptom_burn_blister=symptom_burn_blister,
            symptom_burn_charred=symptom_burn_charred,
            symptom_bruise_blunt=symptom_bruise_blunt,
            symptom_bedsores=symptom_bedsores,
            symptom_clean_cut=symptom_clean_cut
        )
    else:
        morphology_dict_data = extract_morphology_features(image_bgr, skin_mask)
        cinfo = CONDITIONS_KNOWLEDGE_BASE.get(predicted_class, CONDITIONS_KNOWLEDGE_BASE["KULIT_NORMAL"])
        top3_differential_data = [
            {
                "condition_key": predicted_class,
                "common_name": cinfo["nama_umum"],
                "medical_name": cinfo["nama_medis"],
                "probability": round(confidence, 4),
                "percentage": f"{round(confidence * 100, 1)}%",
                "clinical_rationale": "Analisis AI Gemini Multimodal Vision mendeteksi kecocokan patofisiologis paling dominan."
            }
        ]

    # 4. Generate visualisasi Grad-CAM Heatmap
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    overlay_bgr, heatmap_base64 = gradcam_visualizer.generate_heatmap_overlay(
        image_rgb, salient_mask=salient_mask
    )
    
    saved_filename = gradcam_visualizer.save_heatmap_to_disk(overlay_bgr, settings.HEATMAP_DIR)
    base_url = str(request.base_url).rstrip("/")
    heatmap_url = f"{base_url}/static/heatmaps/{saved_filename}"

    # 5. Evaluasi Triase Medis
    triage_result = evaluate_triage(
        condition_key=predicted_class,
        confidence=confidence,
        has_tetanus_risk=has_tetanus_risk or symptom_puncture_nail,
        is_bleeding_uncontrolled=is_bleeding_uncontrolled,
        is_deep_cut=is_deep_cut or (predicted_class == "LUKA_BAKAR_BERAT_DERAJAT_3"),
        is_face_or_joint=is_face_or_joint,
        has_fever=has_fever,
        pain_level=pain_level
    )

    # 6. Ambil panduan P3K & perawatan
    condition_info = CONDITIONS_KNOWLEDGE_BASE.get(predicted_class, CONDITIONS_KNOWLEDGE_BASE["KULIT_NORMAL"])

    tissue_analysis_obj = TissueAnalysis(
        granulation_percentage=tissue_dict["granulation_percentage"],
        slough_percentage=tissue_dict["slough_percentage"],
        necrotic_percentage=tissue_dict["necrotic_percentage"],
        estimated_area_cm2=tissue_dict["estimated_area_cm2"],
        severity_classification=tissue_dict["severity_classification"]
    )

    # 7. Skrining ABCDE Melanoma
    abcde_dict = analyze_abcde(image_bgr, tissue_dict.get("lesion_mask"))
    abcde_obj = ABCDEAnalysis(**abcde_dict) if abcde_dict else None

    # 8. Dynamic Adaptive Anamnesis (CDSS)
    raw_questions = generate_adaptive_questions(predicted_class)
    adaptive_question_objs = [AdaptiveQuestion(**q) for q in raw_questions]

    # 9. Evaluasi Keselamatan Obat & Kontraindikasi Demografis
    raw_safety = evaluate_drug_safety(predicted_class, patient_group)
    safety_warning_objs = [DrugSafetyWarning(**s) for s in raw_safety]
    top3_diff_objs = [DifferentialDiagnosisItem(**d) for d in top3_differential_data]

    return TriageAnalysisResponse(
        success=True,
        condition_key=predicted_class,
        common_name=condition_info["nama_umum"],
        medical_name=condition_info["nama_medis"],
        confidence=round(confidence, 4),
        confidence_percentage=f"{round(confidence * 100, 1)}%",
        triage_level=triage_result["level"],
        triage_color=triage_result["badge_color"],
        triage_action=triage_result["action_instruction"],
        triage_reasons=triage_result["reasons"],
        tissue_analysis=tissue_analysis_obj,
        pain_level=pain_level,
        description=condition_info["deskripsi"],
        first_aid_steps=condition_info["langkah_p3k"],
        recommended_otc_meds=condition_info["obat_rekomendasi_bebas"],
        myths_and_warnings=condition_info["pantangan_dan_mitos"],
        estimated_healing_time=condition_info["estimasi_sembuh"],
        red_flags=condition_info["tanda_bahaya_ke_dokter"],
        heatmap_url=heatmap_url,
        heatmap_base64=heatmap_base64,
        quality_info=quality_obj,
        adaptive_questions=adaptive_question_objs,
        abcde_analysis=abcde_obj,
        top3_differential=top3_diff_objs,
        safety_warnings=safety_warning_objs,
        body_location=body_location,
        morphology_features=morphology_dict_data
    )

@router.post("/track-progress", response_model=ProgressTrackingResponse)
async def track_wound_progress(
    file_day1: UploadFile = File(..., description="Foto luka hari awal / sebelumnya"),
    file_day2: UploadFile = File(..., description="Foto luka hari ini / pemantauan")
):
    """
    Pemantau Trajektori Penyembuhan Luka Klinis (Wound Healing Trajectory Tracker):
    Membandingkan dua citra luka secara serial untuk menghitung:
    - Delta luas luka (Penyusutan / Pembesaran cm²)
    - Progres pergeseran TIME tissue composition (Granulasi vs Slough vs Nekrotik)
    - Klasifikasi status pemulihan klinis (Membaik Cepat, Normal, Stagnan, Memburuk)
    """
    bytes1 = await file_day1.read()
    bytes2 = await file_day2.read()

    try:
        img1 = load_image_from_bytes(bytes1)
        img2 = load_image_from_bytes(bytes2)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal memproses citra pembanding: {str(e)}")

    skin1 = extract_skin_mask(img1)
    skin2 = extract_skin_mask(img2)

    tissue1 = classifier_instance.analyze_tissue_composition(img1, skin1)
    tissue2 = classifier_instance.analyze_tissue_composition(img2, skin2)

    area1 = tissue1["estimated_area_cm2"]
    area2 = tissue2["estimated_area_cm2"]

    # Hitung persentase reduksi luas luka
    if area1 > 0:
        reduction_pct = round(((area1 - area2) / area1) * 100.0, 1)
    else:
        reduction_pct = 0.0

    # Evaluasi Klinis Trajektori
    granulation_gain = tissue2["granulation_percentage"] - tissue1["granulation_percentage"]
    necrotic_gain = tissue2["necrotic_percentage"] - tissue1["necrotic_percentage"]

    recommendations = []

    if reduction_pct >= 20.0 or (reduction_pct > 5.0 and granulation_gain >= 10.0):
        status = "MEMBAIK CEPAT (Excellent Healing)"
        badge_color = "#10B981"
        eval_text = (
            f"Luka mengalami penyusutan luas yang sangat baik sebesar {reduction_pct}%. "
            f"Jaringan granulasi merah meningkat {round(granulation_gain, 1)}%, "
            "menandakan proses re-epitelisasi dan vaskularisasi berjalan sangat aktif."
        )
        recommendations = [
            "Pertahankan balutan steril dan kelembapan luka yang optimal (moist wound healing).",
            "Hindari mengorek krusta atau lapisan merah baru yang terbentuk.",
            "Lanjutkan asupan protein tinggi untuk mempercepat regenerasi kolagen."
        ]
    elif reduction_pct >= 0.0:
        status = "MEMBAIK STABIL (On-Track)"
        badge_color = "#3B82F6"
        eval_text = (
            f"Luka menyusut perlahan sebesar {reduction_pct}% sesuai kurva penyembuhan normal. "
            "Tidak tampak perburukan jaringan yang signifikan."
        )
        recommendations = [
            "Ganti perban secara rutin setiap 1-2 hari atau saat kotor/basah.",
            "Jaga luka tetap kering dari air kotor saat mandi.",
            "Pantau terus tanda infeksi seperti bau, demam, atau nanah bertambah."
        ]
    elif reduction_pct >= -15.0 and necrotic_gain < 5.0:
        status = "STAGNAN (Perlu Evaluasi Perawatan)"
        badge_color = "#F59E0B"
        eval_text = (
            "Ukuran luka relatif menetap atau sedikit mengalami edema (bengkak). "
            "Proses penutupan tepi luka tampak terhambat."
        )
        recommendations = [
            "Evaluasi apakah ada gesekan berulang atau tekanan pada luka.",
            "Pertimbangkan penggunaan salep hidrogel atau debridemen ringan jika terdapat lapisan slough kuning.",
            "Bila luka tidak mengecil dalam 1 minggu, konsultasikan ke klinik perawatan luka."
        ]
    else:
        status = "MEMBURUK / WASPADA INFEKSI (Risk of Complication)"
        badge_color = "#EF4444"
        eval_text = (
            f"Luas luka bertambah sebesar {abs(reduction_pct)}% dengan peningkatan jaringan slough/nekrosis. "
            "Terdapat indikasi kolonisasi bakteri atau komplikasi infeksi jaringan."
        )
        recommendations = [
            "SEGERA periksakan ke dokter atau fasilitas kesehatan terdekat!",
            "Jangan memberikan salep sembarangan tanpa resep dokter.",
            "Waspadai demam menggigil, garis merah menjalar, atau nyeri hebat."
        ]

    tissue1_obj = TissueAnalysis(
        granulation_percentage=tissue1["granulation_percentage"],
        slough_percentage=tissue1["slough_percentage"],
        necrotic_percentage=tissue1["necrotic_percentage"],
        estimated_area_cm2=area1,
        severity_classification=tissue1["severity_classification"]
    )
    tissue2_obj = TissueAnalysis(
        granulation_percentage=tissue2["granulation_percentage"],
        slough_percentage=tissue2["slough_percentage"],
        necrotic_percentage=tissue2["necrotic_percentage"],
        estimated_area_cm2=area2,
        severity_classification=tissue2["severity_classification"]
    )

    return ProgressTrackingResponse(
        success=True,
        day1_area_cm2=area1,
        day2_area_cm2=area2,
        area_reduction_percentage=reduction_pct,
        healing_status=status,
        healing_badge_color=badge_color,
        clinical_evaluation=eval_text,
        day1_tissue=tissue1_obj,
        day2_tissue=tissue2_obj,
        recommendations=recommendations
    )

@router.get("/conditions", response_model=List[ConditionDetail])
def get_all_conditions():
    """
    Mengambil seluruh katalog 27 kondisi sistem integumen dan trauma luka fisik beserta panduan P3K klinis.
    """
    result = []
    for key, info in CONDITIONS_KNOWLEDGE_BASE.items():
        result.append(ConditionDetail(
            key=key,
            common_name=info["nama_umum"],
            medical_name=info["nama_medis"],
            description=info["deskripsi"],
            first_aid_steps=info["langkah_p3k"],
            recommended_otc_meds=info["obat_rekomendasi_bebas"],
            myths_and_warnings=info["pantangan_dan_mitos"],
            estimated_healing_time=info["estimasi_sembuh"],
            red_flags=info["tanda_bahaya_ke_dokter"]
        ))
    return result

@router.post("/consult-chat", response_model=ChatConsultResponse)
async def consult_chat(req: ChatConsultRequest):
    """
    Chatbot Konsultasi Dokter Virtual Terintegrasi SmartTriage AI:
    Menjawab pertanyaan pasien seputar kondisi kulit/luka yang terdeteksi,
    perawatan mandiri, pantangan makanan, mandi, pencegahan bekas/bopeng, dan edukasi obat.
    Mendukung integrasi Google Gemini API jika key diberikan, atau Rule-Based Clinical Expert System.
    """
    condition_info = CONDITIONS_KNOWLEDGE_BASE.get(req.condition_key, CONDITIONS_KNOWLEDGE_BASE["KULIT_NORMAL"])
    user_q = req.message.strip()
    q_lower = user_q.lower()

    # Coba gunakan Gemini Flash jika key disediakan
    if req.gemini_api_key and req.gemini_api_key.strip():
        gemini_prompt = (
            f"Anda adalah Asisten Dokter Spesialis Dermatologi & Perawatan Luka Virtual dari SmartTriage AI.\n"
            f"Pasien teridentifikasi menderita: {condition_info['nama_umum']} ({condition_info['nama_medis']}).\n"
            f"Deskripsi Klinis: {condition_info['deskripsi']}\n"
            f"Langkah P3K: {', '.join(condition_info['langkah_p3k'])}\n"
            f"Obat Aman Bebas: {', '.join(condition_info['obat_rekomendasi_bebas'])}\n"
            f"Pantangan & Mitos: {', '.join(condition_info['pantangan_dan_mitos'])}\n"
            f"Tanda Bahaya: {', '.join(condition_info['tanda_bahaya_ke_dokter'])}\n\n"
            f"Pertanyaan Pasien: \"{user_q}\"\n\n"
            f"Instruksi Khusus:\n"
            f"1. Berikan jawaban dalam Bahasa Indonesia yang ramah, jelas, empati, dan sesuai kaidah medis kedokteran.\n"
            f"2. Ingatkan kontraindikasi berbahaya jika relevan (misal: Jangan berikan aspirin pada cacar air anak karena risiko sindrom Reye, jangan beri salep steroid pada infeksi jamur).\n"
            f"3. Berikan 2-3 saran pertanyaan lanjutan yang relevan untuk ditanyakan pasien.\n"
            f"Format respons HARUS JSON valid:\n"
            f'{{"reply": "jawaban lengkap Anda", "suggested_questions": ["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3"]}}'
        )
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={req.gemini_api_key.strip()}"
        payload = {
            "contents": [{"parts": [{"text": gemini_prompt}]}],
            "generationConfig": {"temperature": 0.3, "response_mime_type": "application/json"}
        }
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    parsed = json.loads(data["candidates"][0]["content"]["parts"][0]["text"])
                    if "reply" in parsed:
                        return ChatConsultResponse(
                            success=True,
                            reply=parsed["reply"],
                            suggested_questions=parsed.get("suggested_questions", [
                                "Apakah boleh mandi dengan air hangat?",
                                "Bagaimana cara mencegah bekas bopeng atau flek hitam?",
                                "Kapan saya harus segera ke IGD rumah sakit?"
                            ])
                        )
        except Exception:
            pass

    # Sistem Pakar Klinis Berbasis Pengetahuan (Expert Medical Rule Engine)
    suggested_questions = [
        "Apakah boleh mandi saat kondisi seperti ini?",
        "Bagaimana cara mencegah timbulnya bekas luka atau bopeng?",
        "Apakah ada pantangan makanan tertentu?",
        "Kapan saya harus segera memeriksakan diri ke dokter?"
    ]

    if any(k in q_lower for k in ["mandi", "air", "sabun", "kebersihan"]):
        if req.condition_key in ["CACAR_AIR_VARICELLA", "HERPES_ZOSTER"]:
            reply = (
                f"**Mandi saat {condition_info['nama_umum']} SANGAT DIPERBOLEHKAN dan Dianjurkan**, bertolak belakang dengan mitos lama. "
                "Gunakan air suam-suam kuku (tidak terlalu panas dan tidak dingin) dengan sabun antiseptik lembut tanpa pewangi keras. "
                "**PENTING**: Jangan menggosok kulit dengan spons atau waslap kasar. Setelah mandi, keringkan dengan cara menepuk-nepuk lembut handuk bersih khusus (jangan digosok) agar lenting air tidak pecah."
            )
        elif "LUKA" in req.condition_key or req.condition_key in ["CANTENGAN_PARONIKIA", "VULNUS_PUNCTUM"]:
            reply = (
                f"Untuk luka pada **{condition_info['nama_umum']}**, jagalah agar area luka tidak terendam air kotor saat mandi. "
                "Anda dapat membersihkan tepi luka menggunakan larutan steril (NaCl 0.9%) atau air matang. Lindungi luka dengan plester kedap air (waterproof dressing) saat mandi, dan segera ganti balutan jika basah atau lembap."
            )
        else:
            reply = (
                f"Pada keluhan **{condition_info['nama_umum']}**, Anda tetap dapat mandi teratur 2 kali sehari untuk menjaga higienitas kulit dan mencegah superinfeksi bakteri. "
                "Gunakan sabun lembut ber-pH seimbang (pH 5.5) dan hindari mandi dengan air yang terlalu panas karena dapat memperparah rasa gatal dan iritasi."
            )

    elif any(k in q_lower for k in ["bekas", "bopeng", "flek", "hitam", "scar", "keloid"]):
        reply = (
            f"**Tips Mencegah Bekas Luka / Hiperpigmentasi Pasca-Inflamasi (PIH) pada {condition_info['nama_umum']}**:\n\n"
            "1. **JANGAN PERNAH MENCONGKEL/MENGGARUK**: Biarkan lenting atau keropeng (krusta) mengering dan terlepas sendiri secara alami.\n"
            "2. **Gunakan Pelembap Medis**: Setelah fase basah/lenting selesai dan luka menutup, oleskan krim pelembap yang mengandung Ceramide, Centella Asiatica, atau Gel Silikon medis secara teratur.\n"
            "3. **Lindungi dari Paparan Sinar Matahari**: Oleskan tabir surya (Sunscreen minimal SPF 30+) pada area bekas yang sembuh untuk mencegah pigmen melanin menggelap permanen.\n"
            "4. **Cukupi Hidrasi & Nutrisi**: Konsumsi vitamin C dan zink untuk menstimulasi sintesis kolagen kulit yang sehat."
        )

    elif any(k in q_lower for k in ["makan", "pantang", "alergi", "telur", "ikan", "udang"]):
        if req.condition_key in ["BIDURAN_URTIKARIA", "EKSIM_DERMATITIS"]:
            reply = (
                f"Untuk **{condition_info['nama_umum']}**, reaksi kulit sangat dipengaruhi oleh pemicu alergi (alergen). "
                "Disarankan membuat buku catatan harian makanan (food diary) dan sementara menghindari makanan pemicu umum seperti makanan laut (seafood), kacang, telur, penyedap rasa tinggi, atau makanan berpengawet jika Anda menyadari flare-up timbul setelah memakannya."
            )
        else:
            reply = (
                f"**Mitos Telur / Ikan Bikin Luka Bernanah adalah SALAH**: Pada kondisi **{condition_info['nama_umum']}**, tubuh justru membutuhkan asupan protein tinggi (seperti telur, ikan, daging tanpa lemak, dan tahu/tempe) untuk pembentukan jaringan baru dan regenerasi sel kulit. "
                "Kecuali jika pasien memiliki riwayat alergi khusus terhadap makanan tersebut, tidak ada pantangan makanan umum."
            )

    elif any(k in q_lower for k in ["menular", "tular", "sekolah", "kerja", "orang lain"]):
        if req.condition_key in ["CACAR_AIR_VARICELLA", "HERPES_ZOSTER", "KUDIS_SKABIES", "KURAP_KADAS", "KUTU_RAMBUT_PEDIKULOSIS"]:
            reply = (
                f"**PERHATIAN TINGGI**: Kondisi **{condition_info['nama_umum']} ({condition_info['nama_medis']}) BERSIFAT MENULAR!**\n\n"
                "- Hindari kontak kulit langsung atau berbagi pakaian, handuk, sisir, dan sprei dengan orang serumah.\n"
                "- Pada cacar air, pasien berpotensi menular hingga seluruh lenting mengering menjadi krusta hitam (biasanya 7-10 hari). Disarankan isolasi mandiri dan beristirahat dari sekolah/kantor.\n"
                "- Cuci seluruh pakaian dan seprai dengan air hangat serta setrika secara merata."
            )
        else:
            reply = (
                f"Kondisi **{condition_info['nama_umum']} TIDAK BERSIFAT MENULAR** ke orang lain. "
                "Kelainan ini merupakan proses inflamasi lokal, reaksi alergi, atau trauma mekanik fisik jaringan, sehingga Anda tidak perlu khawatir menulari anggota keluarga di sekitar Anda."
            )

    elif any(k in q_lower for k in ["obat", "salep", "minum", "parasetamol", "ibuprofen", "steroid", "resep"]):
        reply = (
            f"**Panduan Penggunaan Obat untuk {condition_info['nama_umum']}**:\n\n"
            f"- **Pilihan Obat Bebas (OTC)**: {', '.join(condition_info['obat_rekomendasi_bebas'])}\n"
            f"- **Peringatan Kontraindikasi**: {', '.join(condition_info['pantangan_dan_mitos'])}\n\n"
            "**Catatan Keamanan Obat**: Untuk meredakan demam/nyeri, Parasetamol adalah lini pertama yang paling aman. "
            "Hindari penggunaan antibiotik oral maupun salep steroid kuat tanpa resep dan pengawasan dokter, karena dapat memicu resistensi bakteri atau memperparah infeksi jamur."
        )

    elif any(k in q_lower for k in ["bahaya", "dokter", "darurat", "igd", "puskesmas", "kapan"]):
        reply = (
            f"**Tanda Bahaya (Red Flags) yang Mewajibkan Anda Segera ke Fasilitas Kesehatan**: \n\n"
            + "\n".join([f"⚠️ {rf}" for rf in condition_info['tanda_bahaya_ke_dokter']]) + "\n\n"
            "Jika Anda mengalami salah satu dari gejala di atas, jangan menunda untuk segera memeriksakan diri ke dokter atau instalasi gawat darurat terdekat."
        )

    else:
        reply = (
            f"Berdasarkan analisis klinis SmartTriage AI terhadap **{condition_info['nama_umum']} ({condition_info['nama_medis']})**:\n\n"
            f"**Ringkasan Kondisi**: {condition_info['deskripsi']}\n\n"
            f"**Langkah Perawatan Mandiri Utama**:\n" + "\n".join([f"• {step}" for step in condition_info['langkah_p3k'][:3]]) + "\n\n"
            f"**Estimasi Masa Pemulihan**: {condition_info['estimasi_sembuh']}.\n"
            f"Silakan tanyakan hal spesifik lainnya seperti cara mandi yang benar, pantangan makanan, atau cara mencegah bekas luka."
        )

    return ChatConsultResponse(
        success=True,
        reply=reply,
        suggested_questions=suggested_questions
    )
