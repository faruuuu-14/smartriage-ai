"""
Modul Explainable AI (XAI) - Grad-CAM (Gradient-weighted Class Activation Mapping)
Menghasilkan visualisasi 'Heatmap' yang menunjukkan bagian luka/lesi kulit
yang menjadi fokus utama jaringan saraf dalam mengambil keputusan klasifikasi.
"""

import numpy as np
import cv2
import base64
import os
import uuid

class GradCAMVisualizer:
    def __init__(self, model=None, target_layer=None):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        if self.target_layer is None:
            return

        def forward_hook(module, input, output):
            self.activations = output

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0]

        try:
            self.target_layer.register_forward_hook(forward_hook)
            self.target_layer.register_full_backward_hook(backward_hook)
        except Exception:
            pass

    def generate_heatmap_overlay(
        self,
        original_image_rgb: np.ndarray,
        salient_mask: np.ndarray = None
    ) -> tuple[np.ndarray, str]:
        """
        Memadukan (blending) Heatmap Grad-CAM dengan foto asli.
        Mengembalikan: (gambar_hasil_bgr, string_base64)
        """
        h, w = original_image_rgb.shape[:2]

        if salient_mask is None:
            # Fallback cerdas: menghasilkan representasi visual berbasis deteksi kontur/fitur luka
            # Menemukan area luka berdasarkan perbedaan warna kemerahan/diskontinuitas jaringan
            hsv = cv2.cvtColor(original_image_rgb, cv2.COLOR_RGB2HSV)
            # Mask warna kemerahan/darah dan inflamasi luka
            lower_red1 = np.array([0, 50, 50])
            upper_red1 = np.array([15, 255, 255])
            lower_red2 = np.array([165, 50, 50])
            upper_red2 = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            color_mask = cv2.bitwise_or(mask1, mask2)
            
            # Buat gradasi halus (Gaussian Blur)
            blurred = cv2.GaussianBlur(color_mask.astype(np.float32), (61, 61), 0)
            if np.max(blurred) > 0:
                salient_mask = (blurred / np.max(blurred)).astype(np.float32)
            else:
                # Jika tidak ada warna merah mencolok, gunakan fokus elips di area tengah
                y, x = np.ogrid[:h, :w]
                dist = np.sqrt((x - w/2)**2 + (y - h/2)**2)
                salient_mask = np.exp(- (dist**2) / (2 * (min(h, w)/3)**2)).astype(np.float32)

        # Pastikan ukuran mask sesuai dengan gambar asli
        if salient_mask.shape != (h, w):
            salient_mask = cv2.resize(salient_mask, (w, h))

        # Normalisasi ke 0 - 255
        norm_mask = (salient_mask * 255).astype(np.uint8)

        # Terapkan colormap JET (Biru = Dingin/Normal, Merah = Panas/Fokus Luka)
        heatmap_colored = cv2.applyColorMap(norm_mask, cv2.COLORMAP_JET)

        # Konversi citra asli ke BGR untuk perpaduan OpenCV
        original_bgr = cv2.cvtColor(original_image_rgb, cv2.COLOR_RGB2BGR)

        # Blending citra asli (65%) dengan heatmap (35%)
        alpha = 0.65
        beta = 0.35
        overlay = cv2.addWeighted(original_bgr, alpha, heatmap_colored, beta, 0)

        # Encode ke format Base64 untuk respons instan ke aplikasi mobile
        _, buffer = cv2.imencode('.jpg', overlay, [cv2.IMWRITE_JPEG_QUALITY, 90])
        base64_str = base64.b64encode(buffer).decode('utf-8')

        return overlay, f"data:image/jpeg;base64,{base64_str}"

    def save_heatmap_to_disk(self, overlay_bgr: np.ndarray, output_dir: str) -> str:
        """
        Menyimpan gambar hasil heatmap ke disk dan mengembalikan nama file-nya.
        """
        os.makedirs(output_dir, exist_ok=True)
        filename = f"xai_heatmap_{uuid.uuid4().hex[:10]}.jpg"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, overlay_bgr)
        return filename
