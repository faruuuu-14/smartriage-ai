package com.smartriage.app.ui.screens

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Base64
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.result.launch
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.smartriage.app.data.model.TriageResponse
import com.smartriage.app.ui.TriageUiState
import com.smartriage.app.ui.TriageViewModel
import com.smartriage.app.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TriageScreen(viewModel: TriageViewModel) {
    val uiState by viewModel.uiState.collectAsState()
    val selectedBitmap by viewModel.selectedBitmap.collectAsState()
    val scrollState = rememberScrollState()

    // Activity Result Launcher untuk mengambil foto dari Kamera
    val cameraLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap ->
        if (bitmap != null) {
            viewModel.selectedBitmap.value = bitmap
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = TealPrimary,
                            modifier = Modifier.size(36.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(Icons.Default.MedicalServices, contentDescription = null, tint = Color.White)
                            }
                        }
                        Spacer(modifier = Modifier.width(10.dp))
                        Column {
                            Text("SmarTriage.AI", fontSize = 18.sp, fontWeight = FontWeight.Bold)
                            Text("Asisten Sistem Integumen (Kulit, Kuku, Rambut)", fontSize = 11.sp, color = TextMuted)
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        containerColor = BackgroundLight
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(scrollState)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Card 1: Pengambilan Foto & Preview
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "Foto Area Luka / Kelainan Kulit",
                        fontWeight = FontWeight.Bold,
                        fontSize = 15.sp,
                        color = TextDark
                    )
                    Spacer(modifier = Modifier.height(12.dp))

                    if (selectedBitmap != null) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(220.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFF1F5F9))
                        ) {
                            Image(
                                bitmap = selectedBitmap!!.asImageBitmap(),
                                contentDescription = "Foto Luka",
                                modifier = Modifier.fillMaxSize(),
                                contentScale = ContentScale.Crop
                            )
                            IconButton(
                                onClick = { viewModel.selectedBitmap.value = null },
                                modifier = Modifier
                                    .align(Alignment.TopEnd)
                                    .padding(8.dp)
                                    .background(Color.Black.copy(alpha = 0.6f), CircleShape)
                                    .size(32.dp)
                            ) {
                                Icon(Icons.Default.Close, contentDescription = "Hapus", tint = Color.White, modifier = Modifier.size(16.dp))
                            }
                        }
                    } else {
                        Surface(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(160.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .border(1.5.dp, Color(0xFFCBD5E1), RoundedCornerShape(12.dp))
                                .clickable { cameraLauncher.launch() },
                            color = Color(0xFFF8FAFC)
                        ) {
                            Column(
                                horizontalAlignment = Alignment.CenterHorizontally,
                                verticalArrangement = Arrangement.Center,
                                modifier = Modifier.padding(16.dp)
                            ) {
                                Surface(
                                    shape = CircleShape,
                                    color = Color(0xFFCCFBF1),
                                    modifier = Modifier.size(48.dp)
                                ) {
                                    Box(contentAlignment = Alignment.Center) {
                                        Icon(Icons.Default.CameraAlt, contentDescription = null, tint = TealPrimary)
                                    }
                                }
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Ketuk untuk Memotret Luka", fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                                Text("Pastikan pencahayaan terang dan fokus", fontSize = 11.sp, color = TextMuted)
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    // Tombol Aksi Kamera
                    OutlinedButton(
                        onClick = { cameraLauncher.launch() },
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Icon(Icons.Default.PhotoCamera, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(if (selectedBitmap == null) "Buka Kamera" else "Ambil Ulang Foto")
                    }
                }
            }

            // Card 2: Kuesioner Risiko Singkat
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Pertanyaan Klinis Awal", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Spacer(modifier = Modifier.height(8.dp))

                    val tetanus by viewModel.hasTetanusRisk.collectAsState()
                    val bleeding by viewModel.isBleedingUncontrolled.collectAsState()
                    val deepCut by viewModel.isDeepCut.collectAsState()

                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = tetanus, onCheckedChange = { viewModel.hasTetanusRisk.value = it })
                        Text("Terkena paku, besi berkarat, atau tanah?", fontSize = 12.sp)
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = bleeding, onCheckedChange = { viewModel.isBleedingUncontrolled.value = it })
                        Text("Darah memancar tak henti > 10 menit?", fontSize = 12.sp)
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = deepCut, onCheckedChange = { viewModel.isDeepCut.value = it })
                        Text("Luka robek dalam (>0.5 cm atau tampak lemak)?", fontSize = 12.sp)
                    }
                }
            }

            // Tombol Analisis Utama
            Button(
                onClick = { selectedBitmap?.let { viewModel.analyzeImage(it) } },
                enabled = selectedBitmap != null && uiState !is TriageUiState.Loading,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                shape = RoundedCornerShape(12.dp),
                colors = ButtonDefaults.buttonColors(containerColor = TealPrimary)
            ) {
                if (uiState is TriageUiState.Loading) {
                    CircularProgressIndicator(color = Color.White, modifier = Modifier.size(20.dp))
                    Spacer(modifier = Modifier.width(10.dp))
                    Text("Menganalisis Citra & Grad-CAM...")
                } else {
                    Icon(Icons.Default.AutoAwesome, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Mulai Analisis Triase Medis", fontWeight = FontWeight.Bold)
                }
            }

            // Card 3: Hasil Triase (Jika Sukses)
            when (val state = uiState) {
                is TriageUiState.Success -> {
                    ResultSection(state.result, state.originalBitmap)
                }
                is TriageUiState.Error -> {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color(0xFFFEE2E2)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Error, contentDescription = null, tint = RoseEmergency)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(state.message, color = Color(0xFF991B1B), fontSize = 12.sp)
                        }
                    }
                }
                else -> {}
            }
        }
    }
}

@Composable
fun ResultSection(data: TriageResponse, originalBitmap: Bitmap?) {
    val (bannerColor, badgeColor, badgeText) = when (data.triageLevel) {
        "MERAH" -> Triple(Color(0xFFFFF1F2), RoseEmergency, "GAWAT DARURAT (KE IGD)")
        "KUNING" -> Triple(Color(0xFFFEFCE8), AmberWarning, "KONSULTASI DOKTER")
        else -> Triple(Color(0xFFF0FDF4), EmeraldSafe, "RAWAT MANDIRI")
    }

    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
        // Banner Triase
        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = bannerColor),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Surface(
                    color = badgeColor,
                    shape = RoundedCornerShape(6.dp),
                    modifier = Modifier.padding(bottom = 6.dp)
                ) {
                    Text(
                        text = badgeText,
                        color = Color.White,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.ExtraBold,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                    )
                }
                Text(
                    text = "${data.commonName} (${data.medicalName})",
                    fontWeight = FontWeight.Bold,
                    fontSize = 17.sp,
                    color = TextDark
                )
                Text(
                    text = "Akurasi Keyakinan: ${data.confidencePercentage}",
                    fontSize = 11.sp,
                    color = TextMuted
                )
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    text = data.triageAction,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 13.sp,
                    color = TextDark
                )
            }
        }

        // Card Grad-CAM Visualisasi
        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Explainable AI (Grad-CAM Heatmap)", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                Text("Menyoroti fokus patologis keputusan model", fontSize = 11.sp, color = TextMuted)
                Spacer(modifier = Modifier.height(10.dp))

                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    // Original
                    Column(modifier = Modifier.weight(1f), horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(modifier = Modifier.height(120.dp).fillMaxWidth().clip(RoundedCornerShape(10.dp)).background(Color.LightGray)) {
                            if (originalBitmap != null) {
                                Image(bitmap = originalBitmap.asImageBitmap(), contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                            }
                        }
                        Text("Foto Asli", fontSize = 11.sp, color = TextMuted, modifier = Modifier.padding(top = 4.dp))
                    }

                    // Heatmap Base64
                    Column(modifier = Modifier.weight(1f), horizontalAlignment = Alignment.CenterHorizontally) {
                        val heatmapBitmap = remember(data.heatmapBase64) {
                            try {
                                val cleanBase64 = data.heatmapBase64?.substringAfter("base64,") ?: ""
                                val decodedBytes = Base64.decode(cleanBase64, Base64.DEFAULT)
                                BitmapFactory.decodeByteArray(decodedBytes, 0, decodedBytes.size)
                            } catch (e: Exception) {
                                null
                            }
                        }
                        Box(modifier = Modifier.height(120.dp).fillMaxWidth().clip(RoundedCornerShape(10.dp)).background(Color.LightGray)) {
                            if (heatmapBitmap != null) {
                                Image(bitmap = heatmapBitmap.asImageBitmap(), contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                            }
                        }
                        Text("Heatmap XAI", fontSize = 11.sp, color = TealDark, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 4.dp))
                    }
                }
            }
        }

        // Card Edukasi P3K & Mitos
        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Langkah Pertolongan Pertama (P3K):", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                Spacer(modifier = Modifier.height(6.dp))
                data.firstAidSteps.forEachIndexed { index, step ->
                    Text("${index + 1}. $step", fontSize = 12.sp, modifier = Modifier.padding(vertical = 2.dp), color = TextDark)
                }

                Spacer(modifier = Modifier.height(12.dp))
                Divider()
                Spacer(modifier = Modifier.height(12.dp))

                Text("Peringatan & Anti-Mitos:", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = RoseEmergency)
                Spacer(modifier = Modifier.height(6.dp))
                data.mythsAndWarnings.forEach { myth ->
                    Text("• $myth", fontSize = 12.sp, color = Color(0xFF991B1B), modifier = Modifier.padding(vertical = 2.dp))
                }
            }
        }
    }
}
