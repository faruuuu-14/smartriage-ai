"""
Unit & Integration Tests untuk Backend SmarTriage-Wound AI
"""

import io
import numpy as np
import cv2
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_dummy_wound_image():
    """
    Membuat citra sintetis luka (lingkaran merah di tengah dengan latar warna kulit)
    """
    img = np.full((300, 300, 3), (160, 195, 235), dtype=np.uint8)
    cv2.circle(img, (150, 150), 40, (20, 20, 200), -1)
    cv2.line(img, (120, 130), (180, 170), (10, 10, 150), 5)
    _, encoded = cv2.imencode('.jpg', img)
    return io.BytesIO(encoded.tobytes())

def test_web_ui_and_health():
    """Menguji antarmuka web dan health check"""
    # Web UI root
    res_ui = client.get("/")
    assert res_ui.status_code == 200

    # API Health Check
    res_health = client.get("/health")
    assert res_health.status_code == 200
    data = res_health.json()
    assert data["status"] == "online"
    assert "SmarTriage" in data["system"]

def test_get_conditions():
    """Menguji endpoint katalog kondisi P3K dan kelainan kulit, kuku, rambut, dan ragam luka fisik"""
    response = client.get("/api/v1/triage/conditions")
    assert response.status_code == 200
    conditions = response.json()
    assert len(conditions) == 27
    
    keys = [c["key"] for c in conditions]
    assert "LUKA_ROBEK" in keys
    assert "LUKA_LECET" in keys
    assert "LUKA_BAKAR" in keys
    assert "LUKA_TUSUK_PUNCTURE" in keys
    assert "LUKA_GIGITAN_HEWAN" in keys
    assert "LUKA_BAKAR_BERAT_DERAJAT_3" in keys
    assert "LUKA_MEMAR_KONTUSIO" in keys
    assert "LUKA_TEKAN_DEKUBITUS" in keys
    assert "LUKA_SAYAT_IRIS" in keys
    assert "PANU" in keys
    assert "BISUL" in keys
    assert "CANTENGAN_PARONIKIA" in keys
    assert "JAMUR_KUKU_ONIKOMIKOSIS" in keys
    assert "HEMATOMA_KUKU_KEJEPIT" in keys
    assert "KETOMBE_SEBOROIK" in keys
    assert "ALOPECIA_KEBOTAKAN" in keys
    assert "KUTU_RAMBUT_PEDIKULOSIS" in keys

def test_analyze_wound_image_emergency_red():
    """Menguji analisis gambar dengan kondisi gawat darurat (risiko tetanus)"""
    dummy_img = create_dummy_wound_image()
    response = client.post(
        "/api/v1/triage/analyze",
        files={"file": ("wound.jpg", dummy_img, "image/jpeg")},
        data={
            "has_tetanus_risk": "true",
            "is_bleeding_uncontrolled": "false",
            "is_deep_cut": "true",
            "is_face_or_joint": "false",
            "has_fever": "false",
            "pain_level": "8"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["triage_level"] == "MERAH"
    assert data["heatmap_base64"].startswith("data:image/jpeg;base64,")
    assert len(data["first_aid_steps"]) > 0
    assert len(data["myths_and_warnings"]) > 0
    assert "quality_info" in data
    assert "adaptive_questions" in data
    assert len(data["adaptive_questions"]) > 0

def test_analyze_puncture_tetanus_wound():
    """Menguji klasifikasi dan triase luka tusuk paku berkarat (risiko tetanus)"""
    dummy_img = create_dummy_wound_image()
    response = client.post(
        "/api/v1/triage/analyze",
        files={"file": ("puncture.jpg", dummy_img, "image/jpeg")},
        data={
            "complaint_category": "LUKA",
            "symptom_puncture_nail": "true",
            "has_tetanus_risk": "true",
            "pain_level": "7"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["condition_key"] == "LUKA_TUSUK_PUNCTURE"
    assert data["triage_level"] == "MERAH"
    assert any("tetanus" in r.lower() or "paku" in r.lower() for r in data["triage_reasons"])

def test_analyze_animal_bite_rabies():
    """Menguji triase darurat luka gigitan hewan berisiko rabies"""
    dummy_img = create_dummy_wound_image()
    response = client.post(
        "/api/v1/triage/analyze",
        files={"file": ("bite.jpg", dummy_img, "image/jpeg")},
        data={
            "complaint_category": "LUKA",
            "symptom_animal_bite": "true",
            "pain_level": "6"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["condition_key"] == "LUKA_GIGITAN_HEWAN"
    assert data["triage_level"] == "MERAH"
    assert any("rabies" in r.lower() for r in data["triage_reasons"])

def test_analyze_wound_image_mild_green():
    """Menguji analisis gambar luka ringan tanpa risiko komplikasi"""
    dummy_img = create_dummy_wound_image()
    response = client.post(
        "/api/v1/triage/analyze",
        files={"file": ("wound.jpg", dummy_img, "image/jpeg")},
        data={
            "has_tetanus_risk": "false",
            "is_bleeding_uncontrolled": "false",
            "is_deep_cut": "false",
            "is_face_or_joint": "false",
            "has_fever": "false",
            "pain_level": "2"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["triage_level"] in ["HIJAU", "KUNING"]
    assert data["confidence"] > 0
    assert data["estimated_healing_time"] != ""

def test_analyze_nail_cantengan():
    """Menguji analisis kondisi kuku (cantengan / paronikia)"""
    dummy_img = create_dummy_wound_image()
    response = client.post(
        "/api/v1/triage/analyze",
        files={"file": ("nail.jpg", dummy_img, "image/jpeg")},
        data={
            "complaint_category": "KUKU",
            "symptom_nail_ingrown": "true",
            "pain_level": "5"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["condition_key"] == "CANTENGAN_PARONIKIA"
    assert data["triage_level"] == "KUNING"
    assert "Cantengan" in data["common_name"]

def test_analyze_hair_scalp_dandruff():
    """Menguji analisis kondisi rambut & kulit kepala (dermatitis seboroik)"""
    dummy_img = create_dummy_wound_image()
    response = client.post(
        "/api/v1/triage/analyze",
        files={"file": ("scalp.jpg", dummy_img, "image/jpeg")},
        data={
            "complaint_category": "RAMBUT",
            "symptom_scalp_dandruff": "true",
            "pain_level": "2"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["condition_key"] == "KETOMBE_SEBOROIK"
    assert data["triage_level"] == "HIJAU"
    assert "Ketombe" in data["common_name"]

def test_track_wound_progress():
    """Menguji endpoint serial trajectory tracker (pemantau penyusutan luka)"""
    # Citra luka awal (diameter 60 px)
    img1 = np.full((300, 300, 3), (160, 195, 235), dtype=np.uint8)
    cv2.circle(img1, (150, 150), 60, (20, 20, 200), -1)
    _, enc1 = cv2.imencode('.jpg', img1)

    # Citra luka hari ke-7 (diameter 30 px, menyusut)
    img2 = np.full((300, 300, 3), (160, 195, 235), dtype=np.uint8)
    cv2.circle(img2, (150, 150), 30, (20, 20, 200), -1)
    _, enc2 = cv2.imencode('.jpg', img2)

    response = client.post(
        "/api/v1/triage/track-progress",
        files={
            "file_day1": ("day1.jpg", io.BytesIO(enc1.tobytes()), "image/jpeg"),
            "file_day2": ("day2.jpg", io.BytesIO(enc2.tobytes()), "image/jpeg")
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["day1_area_cm2"] > data["day2_area_cm2"]
    assert data["area_reduction_percentage"] > 0
    assert "MEMBAIK" in data["healing_status"]
    assert len(data["recommendations"]) > 0

def test_quality_gatekeeper_non_skin():
    """Menguji penolakan citra non-kulit (misal meja, lantai, atau objek acak)"""
    green_table = np.full((300, 300, 3), (20, 180, 20), dtype=np.uint8)
    _, enc = cv2.imencode('.jpg', green_table)
    response = client.post(
        "/api/v1/triage/analyze",
        files={"file": ("desk.jpg", io.BytesIO(enc.tobytes()), "image/jpeg")},
        data={"complaint_category": "AUTO"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quality_info"]["is_valid"] is False
    assert data["quality_info"]["quality_status"] == "BUKAN_KULIT"
    assert "tidak terdeteksi sebagai jaringan kulit" in data["quality_info"]["warning_message"].lower()

def test_morphology_feature_extraction():
    """Menguji ekstraksi fitur morfologi Computer Vision (Vesikel, Annular Ring, Tekstur Scab, Punctate)"""
    from app.ml.morphology import extract_morphology_features
    # Gambar sintetis dengan specular highlights (vesikel)
    skin_img = np.full((200, 200, 3), (160, 195, 235), dtype=np.uint8)
    skin_mask = np.full((200, 200), 255, dtype=np.uint8)
    # Buat bintik pantulan cahaya terang (vesikel)
    for pt in [(50, 50), (60, 55), (70, 65), (80, 50), (90, 60)]:
        cv2.circle(skin_img, pt, 4, (255, 255, 255), -1)
    
    feats = extract_morphology_features(skin_img, skin_mask)
    assert "vesicle_score" in feats
    assert "ring_score" in feats
    assert "entropy_score" in feats
    assert "punctate_score" in feats
    assert feats["has_vesicles"] is True

def test_top3_differential_and_body_location():
    """Menguji Top-3 Differential Diagnosis dan contextual prior pembobotan anatomi tubuh"""
    dummy_img = create_dummy_wound_image()
    response = client.post(
        "/api/v1/triage/analyze",
        files={"file": ("rash.jpg", dummy_img, "image/jpeg")},
        data={
            "complaint_category": "GATAL",
            "body_location": "PINGGANG_DERMATOM",
            "patient_group": "DEWASA"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "top3_differential" in data
    assert len(data["top3_differential"]) == 3
    assert data["body_location"] == "PINGGANG_DERMATOM"
    
    # Differential diagnosis harus memiliki nama umum, persentase, dan rasional klinis
    for ddx in data["top3_differential"]:
        assert "condition_key" in ddx
        assert "common_name" in ddx
        assert "probability" in ddx
        assert "percentage" in ddx
        assert len(ddx["clinical_rationale"]) > 0

def test_drug_safety_rules():
    """Menguji modul safety checker untuk mendeteksi kontraindikasi fatal (Reye's syndrome & Tinea Incognito)"""
    from app.core.safety_checker import evaluate_drug_safety
    
    # 1. Cacar Air pada Anak-anak (Bahaya Aspirin -> Sindrom Reye)
    warnings_varicella_anak = evaluate_drug_safety("CACAR_AIR_VARICELLA", "ANAK")
    assert any("Reye" in w["warning_message"] or "Aspirin" in w["warning_message"] for w in warnings_varicella_anak)
    
    # 2. Infeksi Jamur (Kurap) -> Kontraindikasi Kortikosteroid
    warnings_kurap = evaluate_drug_safety("KURAP_KADAS", "DEWASA")
    assert any("Steroid" in w["title"] or "Tinea Incognito" in w["warning_message"] for w in warnings_kurap)

    # 3. Luka Terbuka -> Larangan Odol / Minyak Tanah / Es Batu
    warnings_luka = evaluate_drug_safety("LUKA_BAKAR", "DEWASA")
    assert any("LARANGAN_P3K" in w["category"] and ("odol" in w["warning_message"].lower() or "pasta gigi" in w["title"].lower()) for w in warnings_luka)

def test_telehealth_consult_chat_endpoint():
    """Menguji endpoint chatbot konsultasi dokter virtual"""
    # 1. Pertanyaan tentang mandi saat cacar air
    res_bath = client.post(
        "/api/v1/triage/consult-chat",
        json={
            "condition_key": "CACAR_AIR_VARICELLA",
            "message": "Apakah penderita cacar air boleh mandi?",
            "patient_group": "ANAK"
        }
    )
    assert res_bath.status_code == 200
    data_bath = res_bath.json()
    assert data_bath["success"] is True
    assert "mandi" in data_bath["reply"].lower()
    assert len(data_bath["suggested_questions"]) > 0

    # 2. Pertanyaan tentang pencegahan bekas luka / bopeng
    res_scar = client.post(
        "/api/v1/triage/consult-chat",
        json={
            "condition_key": "CACAR_AIR_VARICELLA",
            "message": "Bagaimana cara mencegah agar tidak bopeng atau berbekas?",
            "patient_group": "DEWASA"
        }
    )
    assert res_scar.status_code == 200
    data_scar = res_scar.json()
    assert "bekas" in data_scar["reply"].lower() or "garuk" in data_scar["reply"].lower()

