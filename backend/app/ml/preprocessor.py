"""
Modul Pra-pemrosesan Citra (Image Preprocessing)
Termasuk segmentasi kulit (Skin Masking) untuk mereduksi distraksi latar belakang
seperti meja, keyboard, atau pakaian.
"""

import io
import numpy as np
import cv2
from PIL import Image

def load_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Membaca byte citra dan mengonversinya ke format numpy BGR (OpenCV)
    """
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Gagal membaca citra. Pastikan format file adalah JPG, PNG, atau WEBP yang valid.")
    return image

def extract_skin_mask(image_bgr: np.ndarray) -> np.ndarray:
    """
    Mengekstraksi mask kulit manusia menggunakan ruang warna YCrCb dan HSV
    untuk meredam objek non-kulit di latar belakang (keyboard, meja, baju, dll.)
    """
    # 1. Ruang Warna YCrCb
    ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    # Rentang warna kulit standar dermatologi
    lower_ycrcb = np.array([0, 133, 77], dtype=np.uint8)
    upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)
    mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

    # 2. Ruang Warna HSV
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([0, 30, 60], dtype=np.uint8)
    upper_hsv = np.array([25, 255, 255], dtype=np.uint8)
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Gabungkan kedua mask
    skin_mask = cv2.bitwise_and(mask_ycrcb, mask_hsv)

    # Morfologi untuk menghilangkan noise kecil (closing & opening)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # Jika area kulit terdeteksi sangat kecil (< 5%), fallback ke seluruh gambar
    if np.sum(skin_mask > 0) < (image_bgr.shape[0] * image_bgr.shape[1] * 0.05):
        skin_mask = np.full((image_bgr.shape[0], image_bgr.shape[1]), 255, dtype=np.uint8)

    return skin_mask

def validate_image_quality(image_bgr: np.ndarray) -> dict:
    """
    Quality & Anatomical Gatekeeper:
    1. Deteksi Blur/Fokus kamera menggunakan Laplacian Variance
    2. Deteksi Pencahayaan (terlalu gelap / over-exposed)
    3. Deteksi Jaringan Kulit / Tubuh Manusia (OOD Rejection)
    """
    h, w = image_bgr.shape[:2]
    total_pixels = h * w
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # 1. Laplacian Variance untuk Uji Ketajaman / Blur
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    blur_score = float(round(laplacian_var, 1))
    is_blurry = blur_score < 45.0

    # 2. Rata-rata Kecerahan
    mean_brightness = float(round(np.mean(gray), 1))
    is_too_dark = mean_brightness < 28.0
    is_over_exposed = mean_brightness > 245.0

    # 3. Validasi Kehadiran Jaringan Kulit / Tubuh
    ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    lower_ycrcb = np.array([0, 133, 77], dtype=np.uint8)
    upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)
    mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([0, 25, 50], dtype=np.uint8)
    upper_hsv = np.array([28, 255, 255], dtype=np.uint8)
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    skin_mask_combined = cv2.bitwise_and(mask_ycrcb, mask_hsv)
    skin_pixels = np.sum(skin_mask_combined > 0)
    skin_ratio = float(skin_pixels / total_pixels)

    # Deteksi warna kemerahan darah/luka (jika kulit tertutup darah penuh)
    lower_r1 = np.array([0, 70, 50])
    upper_r1 = np.array([12, 255, 255])
    lower_r2 = np.array([168, 70, 50])
    upper_r2 = np.array([180, 255, 255])
    red_mask = cv2.bitwise_or(cv2.inRange(hsv, lower_r1, upper_r1), cv2.inRange(hsv, lower_r2, upper_r2))
    red_ratio = float(np.sum(red_mask > 0) / total_pixels)

    # Deteksi warna rambut gelap/hitam/cokelat di kepala
    lower_hair = np.array([0, 0, 0])
    upper_hair = np.array([180, 255, 50])
    hair_mask = cv2.inRange(hsv, lower_hair, upper_hair)
    hair_ratio = float(np.sum(hair_mask > 0) / total_pixels)

    # Menentukan apakah citra mengandung jaringan tubuh/kulit/rambut manusia yang valid
    is_human_tissue = (skin_ratio >= 0.05) or (red_ratio >= 0.04) or (hair_ratio >= 0.15)

    is_valid = True
    warning_message = None
    quality_status = "OPTIMAL"

    if is_too_dark:
        is_valid = False
        quality_status = "TERLALU_GELAP"
        warning_message = "Foto terlalu gelap untuk dianalisis secara akurat. Harap nyalakan lampu atau gunakan lampu kilat (flash)."
    elif is_over_exposed:
        is_valid = False
        quality_status = "TERLALU_TERANG"
        warning_message = "Foto mengalami over-exposure (terlalu silau putih). Harap kurangi pantulan cahaya langsung."
    elif not is_human_tissue:
        is_valid = False
        quality_status = "BUKAN_KULIT"
        warning_message = "Citra tidak terdeteksi sebagai jaringan kulit, kuku, atau rambut manusia. Harap unggah foto medis yang relevan."
    elif is_blurry:
        # Foto blur masih diizinkan dianalisis namun disertai peringatan klinis
        quality_status = "BURAM"
        warning_message = "Foto tampak agak buram/goyang. Hasil analisis mungkin kurang maksimal. Disarankan mengambil foto ulang dengan fokus yang stabil."

    return {
        "is_valid": is_valid,
        "quality_status": quality_status,
        "blur_score": blur_score,
        "is_blurry": is_blurry,
        "mean_brightness": mean_brightness,
        "skin_percentage": round(skin_ratio * 100, 1),
        "is_human_tissue": is_human_tissue,
        "warning_message": warning_message
    }

def preprocess_for_model(image_bgr: np.ndarray, target_size: tuple = (224, 224)):
    """
    Mengubah ukuran dan menormalisasi citra sesuai standar torchvision (ImageNet statistics)
    """
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(image_rgb, target_size, interpolation=cv2.INTER_AREA)
    normalized = resized.astype(np.float32) / 255.0
    
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    standardized = (normalized - mean) / std
    
    transposed = np.transpose(standardized, (2, 0, 1))
    batch_tensor = np.expand_dims(transposed, axis=0)
    
    return batch_tensor, image_rgb

