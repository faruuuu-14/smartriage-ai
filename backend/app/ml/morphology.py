"""
Modul Analisis Morfologi dan Pola Tekstur Lesi (Computer Vision)
Mengekstraksi fitur mikro-patologis:
1. Specular Vesicle Blob Detector (Lenting berair berkilat khas Cacar Air & Herpes)
2. Annular Ring / Central Clearing Detector (Cincin bertepi aktif khas Kurap/Kadas)
3. Scab Texture Entropy Detector (Permukaan kasar keropeng luka lecet vs bentol halus biduran)
4. Punctate Depth Detector (Titik lubang tusukan paku berkarat)
"""

import cv2
import numpy as np
from typing import Dict, Any

def detect_specular_vesicles(image_bgr: np.ndarray, skin_mask: np.ndarray) -> float:
    """
    Mendeteksi keberadaan lenting gelembung air (vesikel) dengan kilap specular.
    Ciri khas Cacar Air (Varicella) dan Herpes Zoster:
    - Bintik kecil terang/berkilau (pantulan cahaya pada cairan) di tengah area eritema (merah).
    """
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    h, w = image_bgr.shape[:2]
    total_skin_pixels = max(1, np.sum(skin_mask > 0))

    # 1. Mask pantulan cahaya specular (terang berkilap, saturasi rendah)
    lower_specular = np.array([0, 0, 190])
    upper_specular = np.array([180, 75, 255])
    specular_mask = cv2.inRange(hsv, lower_specular, upper_specular)
    specular_mask = cv2.bitwise_and(specular_mask, skin_mask)

    # 2. Mask kemerahan (eritema di sekitar lenting)
    lower_r1 = np.array([0, 60, 60])
    upper_r1 = np.array([15, 255, 255])
    lower_r2 = np.array([165, 60, 60])
    upper_r2 = np.array([180, 255, 255])
    red_mask = cv2.bitwise_or(cv2.inRange(hsv, lower_r1, upper_r1), cv2.inRange(hsv, lower_r2, upper_r2))
    red_mask = cv2.bitwise_and(red_mask, skin_mask)

    # 3. Analisis kontur specular spots (harus kecil & tersebar bulat, bukan satu refleksi besar)
    contours, _ = cv2.findContours(specular_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    vesicle_count = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Lenting tetesan embun biasanya kecil berdiameter 3 - 35 px
        if 8 < area < 900:
            perimeter = cv2.arcLength(cnt, True)
            if perimeter > 0:
                circularity = 4 * np.pi * (area / (perimeter * perimeter))
                if circularity > 0.45:
                    # Periksa apakah di sekitar specular spot terdapat halo kemerahan
                    x, y, cw, ch = cv2.boundingRect(cnt)
                    pad = 12
                    x1 = max(0, x - pad)
                    y1 = max(0, y - pad)
                    x2 = min(w, x + cw + pad)
                    y2 = min(h, y + ch + pad)
                    local_red = red_mask[y1:y2, x1:x2]
                    if np.sum(local_red > 0) > 20:
                        vesicle_count += 1

    # Skor normalisasi (jika ditemukan multiple vesicles >= 3 bintik)
    if vesicle_count >= 5:
        vesicle_score = 0.95
    elif vesicle_count >= 3:
        vesicle_score = 0.78
    elif vesicle_count >= 1:
        vesicle_score = 0.45
    else:
        vesicle_score = 0.08

    return float(round(vesicle_score, 3))

def detect_annular_rings(image_bgr: np.ndarray, skin_mask: np.ndarray) -> float:
    """
    Mendeteksi pola cincin melingkar konsentris (Annular Lesion with Central Clearing).
    Ciri khas Kurap / Kadas (Tinea Corporis):
    - Tepi luar lesi aktif berwarna lebih merah/menonjol.
    - Bagian tengah lesi cenderung lebih pucat (central clearing).
    """
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Red lesion mask
    lower_r1 = np.array([0, 60, 60])
    upper_r1 = np.array([14, 255, 255])
    lower_r2 = np.array([166, 60, 60])
    upper_r2 = np.array([180, 255, 255])
    red_mask = cv2.bitwise_or(cv2.inRange(hsv, lower_r1, upper_r1), cv2.inRange(hsv, lower_r2, upper_r2))
    red_mask = cv2.bitwise_and(red_mask, skin_mask)

    # Deteksi cincin dengan deteksi kontur hirarkis (RETR_CCOMP)
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    ring_score = 0.05

    if hierarchy is not None and len(hierarchy[0]) > 0:
        for i, h_info in enumerate(hierarchy[0]):
            # h_info: [Next, Previous, First_Child, Parent]
            if h_info[2] != -1:
                outer_area = cv2.contourArea(contours[i])
                inner_area = cv2.contourArea(contours[h_info[2]])
                if outer_area > 450 and inner_area > 120:
                    ratio = inner_area / max(1.0, outer_area)
                    if 0.20 < ratio < 0.75:
                        ring_score = max(ring_score, 0.90)

    # Pendekatan Hough Circles terverifikasi dengan central clearing nyata
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=60, param1=70, param2=40, minRadius=30, maxRadius=160)
    if circles is not None and len(circles[0]) > 0:
        for c in circles[0]:
            cx, cy, r = int(c[0]), int(c[1]), int(c[2])
            if 0 <= cy < image_bgr.shape[0] and 0 <= cx < image_bgr.shape[1]:
                mask_outer = np.zeros_like(gray)
                cv2.circle(mask_outer, (cx, cy), r, 255, 6)
                mask_center = np.zeros_like(gray)
                cv2.circle(mask_center, (cx, cy), int(r * 0.4), 255, -1)
                
                red_edge_density = np.sum(red_mask[mask_outer > 0] > 0) / max(1, np.sum(mask_outer > 0))
                red_center_density = np.sum(red_mask[mask_center > 0] > 0) / max(1, np.sum(mask_center > 0))
                
                if red_edge_density > 0.35 and red_center_density < 0.12:
                    ring_score = max(ring_score, 0.85)

    return float(round(ring_score, 3))

def detect_scab_texture_entropy(image_bgr: np.ndarray, skin_mask: np.ndarray) -> float:
    """
    Mengukur kekasaran tekstur keropeng/krusta (Scab Texture Roughness/Entropy).
    Membedakan Luka Lecet/Jatuh (bertekstur kasar, darah mengering) dari Biduran (bentol edema halus licin).
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    # Deteksi warna keropeng (cokelat kemerahan gelap)
    lower_scab = np.array([0, 50, 20])
    upper_scab = np.array([22, 255, 140])
    scab_mask = cv2.bitwise_and(cv2.inRange(hsv, lower_scab, upper_scab), skin_mask)
    scab_pixels = np.sum(scab_mask > 0)

    # Local texture variance via Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    masked_lap = laplacian[scab_mask > 0] if scab_pixels > 50 else laplacian[skin_mask > 0]
    local_roughness = float(np.var(masked_lap)) if len(masked_lap) > 50 else 0.0

    # Normalisasi roughness score (0.0 halus / urtikaria -> 1.0 sangat kasar / keropeng)
    if scab_pixels > 400 and local_roughness > 65.0:
        entropy_score = 0.92
    elif scab_pixels > 150 or local_roughness > 45.0:
        entropy_score = 0.70
    elif local_roughness > 20.0:
        entropy_score = 0.40
    else:
        # Sangat halus (bentol biduran licin)
        entropy_score = 0.10

    return float(round(entropy_score, 3))

def detect_punctate_wound(image_bgr: np.ndarray, skin_mask: np.ndarray) -> float:
    """
    Mendeteksi lubang tusukan pungtata terisolasi (Punctate Pore).
    Ciri khas Luka Tusuk Paku/Kawat:
    - 1 atau 2 titik gelap terisolasi di tengah (lubang tusukan) dengan halo kemerahan di sekelilingnya.
    - TIDAK BANYAK BINTIK (bukan ruam diseminata atau lecet luas dengan ratusan bintik).
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    h, w = image_bgr.shape[:2]

    # Titik sangat gelap (lubang luka dalam)
    dark_mask = cv2.inRange(gray, 0, 45)
    dark_mask = cv2.bitwise_and(dark_mask, skin_mask)

    contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_dark_spots = len(contours)
    
    # Jika titik gelap sangat banyak (> 10), ini adalah tekstur krusta, rambut, atau ruam, BUKAN luka tusuk paku tunggal
    if total_dark_spots == 0 or total_dark_spots > 10:
        return 0.05

    punctate_score = 0.05
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 12 < area < 350:
            perimeter = cv2.arcLength(cnt, True)
            if perimeter > 0:
                circularity = 4 * np.pi * (area / (perimeter * perimeter))
                if circularity > 0.50:
                    x, y, cw, ch = cv2.boundingRect(cnt)
                    pad = 16
                    x1 = max(0, x - pad)
                    y1 = max(0, y - pad)
                    x2 = min(w, x + cw + pad)
                    y2 = min(h, y + ch + pad)
                    
                    sub_hsv = hsv[y1:y2, x1:x2]
                    lower_r = np.array([0, 70, 50])
                    upper_r = np.array([15, 255, 255])
                    red_surround = cv2.inRange(sub_hsv, lower_r, upper_r)
                    if np.sum(red_surround > 0) > 40:
                        punctate_score = max(punctate_score, 0.88)

    return float(round(punctate_score, 3))

def extract_morphology_features(image_bgr: np.ndarray, skin_mask: np.ndarray) -> Dict[str, Any]:
    """
    Mengekstraksi seluruh indikator morfologi patologis untuk disuplai ke Decision Engine.
    """
    vesicle_score = detect_specular_vesicles(image_bgr, skin_mask)
    ring_score = detect_annular_rings(image_bgr, skin_mask)
    entropy_score = detect_scab_texture_entropy(image_bgr, skin_mask)
    punctate_score = detect_punctate_wound(image_bgr, skin_mask)

    return {
        "vesicle_score": vesicle_score,
        "ring_score": ring_score,
        "entropy_score": entropy_score,
        "punctate_score": punctate_score,
        "has_vesicles": vesicle_score >= 0.50,
        "has_annular_ring": ring_score >= 0.50,
        "is_rough_scab": entropy_score >= 0.60,
        "is_smooth_wheal": entropy_score <= 0.25,
        "is_punctate_wound": punctate_score >= 0.50
    }
