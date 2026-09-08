package com.smartriage.app.ui.screens

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.result.launch
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.smartriage.app.data.model.WoundProgressResponse
import com.smartriage.app.ui.TrackerUiState
import com.smartriage.app.ui.TriageViewModel
import com.smartriage.app.ui.theme.*

@Composable
fun TrackerScreen(viewModel: TriageViewModel) {
    val context = LocalContext.current
    val trackerState by viewModel.trackerState.collectAsState()
    val day1Bitmap by viewModel.trackerBitmapDay1.collectAsState()
    val day2Bitmap by viewModel.trackerBitmapDay2.collectAsState()
    val scrollState = rememberScrollState()

    // Launcher Hari 1 - Kamera
    val camera1Launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap ->
        if (bitmap != null) viewModel.trackerBitmapDay1.value = bitmap
    }

    // Launcher Hari 1 - Galeri
    val gallery1Launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            try {
                val stream = context.contentResolver.openInputStream(uri)
                val bitmap = BitmapFactory.decodeStream(stream)
                if (bitmap != null) viewModel.trackerBitmapDay1.value = bitmap
            } catch (_: Exception) {}
        }
    }

    // Launcher Hari 2 - Kamera
    val camera2Launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap ->
        if (bitmap != null) viewModel.trackerBitmapDay2.value = bitmap
    }

    // Launcher Hari 2 - Galeri
    val gallery2Launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            try {
                val stream = context.contentResolver.openInputStream(uri)
                val bitmap = BitmapFactory.decodeStream(stream)
                if (bitmap != null) viewModel.trackerBitmapDay2.value = bitmap
            } catch (_: Exception) {}
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Header Banner
        Card(
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = TealLight),
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier.padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = TealPrimary,
                    modifier = Modifier.size(44.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            Icons.Default.TrendingDown,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(24.dp)
                        )
                    }
                }
                Spacer(modifier = Modifier.width(12.dp))
                Column {
                    Text(
                        "Trajektori Penyembuhan Serial",
                        fontWeight = FontWeight.Bold,
                        fontSize = 17.sp,
                        color = TextPrimary
                    )
                    Text(
                        "Bandingkan reduksi luas luka & granulasi jaringan antar waktu",
                        fontSize = 12.sp,
                        color = TextSecondary
                    )
                }
            }
        }

        // Card Petunjuk Kalibrasi
        Card(
            shape = RoundedCornerShape(14.dp),
            colors = CardDefaults.cardColors(containerColor = IndigoAiLight),
            border = BorderStroke(1.dp, IndigoAi.copy(alpha = 0.3f)),
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier.padding(12.dp),
                verticalAlignment = Alignment.Top
            ) {
                Icon(
                    Icons.Outlined.Info,
                    contentDescription = null,
                    tint = IndigoAi,
                    modifier = Modifier
                        .size(20.dp)
                        .padding(top = 2.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    "Tips Presisi: Ambil kedua foto dari sudut 90° tegak lurus dengan pencahayaan konstan untuk estimasi luas area (cm²) yang akurat.",
                    fontSize = 12.sp,
                    color = TextPrimary,
                    lineHeight = 17.sp
                )
            }
        }

        // Dual Image Pickers Grid / Stack
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // Kolom Hari 1 (Baseline)
            Box(modifier = Modifier.weight(1f)) {
                WoundDayPicker(
                    title = "Hari 1 (Baseline)",
                    badgeColor = TealPrimary,
                    bitmap = day1Bitmap,
                    onCameraClick = { camera1Launcher.launch() },
                    onGalleryClick = { gallery1Launcher.launch("image/*") },
                    onRemove = { viewModel.trackerBitmapDay1.value = null }
                )
            }

            // Kolom Hari 2 (Evaluasi)
            Box(modifier = Modifier.weight(1f)) {
                WoundDayPicker(
                    title = "Hari 2 (Monitoring)",
                    badgeColor = IndigoAi,
                    bitmap = day2Bitmap,
                    onCameraClick = { camera2Launcher.launch() },
                    onGalleryClick = { gallery2Launcher.launch("image/*") },
                    onRemove = { viewModel.trackerBitmapDay2.value = null }
                )
            }
        }

        // Tombol Evaluasi
        val canEvaluate = day1Bitmap != null && day2Bitmap != null
        val isLoading = trackerState is TrackerUiState.Loading

        Button(
            onClick = { viewModel.evaluateWoundProgress() },
            enabled = canEvaluate && !isLoading,
            shape = RoundedCornerShape(16.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = TealPrimary,
                disabledContainerColor = Color(0xFFCBD5E1)
            ),
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp)
        ) {
            if (isLoading) {
                CircularProgressIndicator(
                    color = Color.White,
                    modifier = Modifier.size(22.dp),
                    strokeWidth = 2.5.dp
                )
                Spacer(modifier = Modifier.width(10.dp))
                Text("Menganalisis Perubahan...", fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
            } else {
                Icon(Icons.Default.Analytics, contentDescription = null, modifier = Modifier.size(20.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Bandingkan Progres Penyembuhan", fontSize = 15.sp, fontWeight = FontWeight.Bold)
            }
        }

        // Hasil Evaluasi
        AnimatedVisibility(
            visible = trackerState is TrackerUiState.Success,
            enter = fadeIn(),
            exit = fadeOut()
        ) {
            if (trackerState is TrackerUiState.Success) {
                val result = (trackerState as TrackerUiState.Success).result
                TrackerResultSection(result = result)
            }
        }

        // Error State
        AnimatedVisibility(
            visible = trackerState is TrackerUiState.Error,
            enter = fadeIn(),
            exit = fadeOut()
        ) {
            if (trackerState is TrackerUiState.Error) {
                val msg = (trackerState as TrackerUiState.Error).message
                Card(
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = RoseEmergencyLight),
                    border = BorderStroke(1.dp, RoseEmergency),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.ErrorOutline, contentDescription = null, tint = RoseEmergency)
                        Spacer(modifier = Modifier.width(10.dp))
                        Text(msg, color = RoseEmergency, fontSize = 13.sp, fontWeight = FontWeight.Medium)
                    }
                }
            }
        }
    }
}

@Composable
fun WoundDayPicker(
    title: String,
    badgeColor: Color,
    bitmap: Bitmap?,
    onCameraClick: () -> Unit,
    onGalleryClick: () -> Unit,
    onRemove: () -> Unit
) {
    Card(
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceCard),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Surface(
                shape = RoundedCornerShape(8.dp),
                color = badgeColor.copy(alpha = 0.12f),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = title,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = badgeColor,
                    modifier = Modifier.padding(vertical = 4.dp, horizontal = 8.dp)
                )
            }

            Spacer(modifier = Modifier.height(10.dp))

            if (bitmap != null) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(150.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .border(1.dp, Color(0xFFE2E8F0), RoundedCornerShape(12.dp))
                ) {
                    Image(
                        bitmap = bitmap.asImageBitmap(),
                        contentDescription = title,
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )
                    IconButton(
                        onClick = onRemove,
                        modifier = Modifier
                            .align(Alignment.TopEnd)
                            .padding(6.dp)
                            .size(28.dp)
                            .background(Color.Black.copy(alpha = 0.6f), CircleShape)
                    ) {
                        Icon(
                            Icons.Default.Close,
                            contentDescription = "Hapus",
                            tint = Color.White,
                            modifier = Modifier.size(16.dp)
                        )
                    }
                }
            } else {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(150.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color(0xFFF8FAFC))
                        .border(1.dp, Color(0xFFE2E8F0), RoundedCornerShape(12.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Icon(
                            Icons.Outlined.AddPhotoAlternate,
                            contentDescription = null,
                            tint = Color(0xFF94A3B8),
                            modifier = Modifier.size(36.dp)
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text("Pilih Foto", fontSize = 11.sp, color = TextSecondary)
                    }
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                OutlinedButton(
                    onClick = onCameraClick,
                    shape = RoundedCornerShape(10.dp),
                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 6.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.PhotoCamera, contentDescription = null, modifier = Modifier.size(16.dp))
                }
                OutlinedButton(
                    onClick = onGalleryClick,
                    shape = RoundedCornerShape(10.dp),
                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 6.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.PhotoLibrary, contentDescription = null, modifier = Modifier.size(16.dp))
                }
            }
        }
    }
}

@Composable
fun TrackerResultSection(result: WoundProgressResponse) {
    val isImproving = result.areaReductionPercentage > 0
    val badgeColor = try {
        Color(android.graphics.Color.parseColor(result.healingBadgeColor))
    } catch (_: Exception) {
        if (isImproving) EmeraldSafe else AmberWarning
    }

    Column(
        verticalArrangement = Arrangement.spacedBy(14.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        // Status Hero Card
        Card(
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceCard),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(18.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = badgeColor.copy(alpha = 0.15f),
                        border = BorderStroke(1.dp, badgeColor.copy(alpha = 0.4f))
                    ) {
                        Text(
                            text = result.healingStatus.ifBlank { "Evaluasi Selesai" },
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = badgeColor,
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp)
                        )
                    }

                    Text(
                        text = if (isImproving) "📈 Tren Positif" else "⚠️ Perlu Perhatian",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = if (isImproving) EmeraldSafe else AmberWarning
                    )
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Perubahan Luas Permukaan (Delta Area)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("Perubahan Ukuran", fontSize = 12.sp, color = TextSecondary)
                        Text(
                            text = "${if (result.areaReductionPercentage >= 0) "-" else "+"}${kotlin.math.abs(result.areaReductionPercentage)}%",
                            fontSize = 28.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = if (isImproving) EmeraldSafe else RoseEmergency
                        )
                    }

                    Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Card(
                            shape = RoundedCornerShape(12.dp),
                            colors = CardDefaults.cardColors(containerColor = Color(0xFFF8FAFC)),
                            modifier = Modifier.padding(2.dp)
                        ) {
                            Column(modifier = Modifier.padding(8.dp)) {
                                Text("Awal", fontSize = 10.sp, color = TextSecondary)
                                Text("${result.day1AreaCm2} cm²", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                            }
                        }
                        Card(
                            shape = RoundedCornerShape(12.dp),
                            colors = CardDefaults.cardColors(containerColor = Color(0xFFF8FAFC)),
                            modifier = Modifier.padding(2.dp)
                        ) {
                            Column(modifier = Modifier.padding(8.dp)) {
                                Text("Evaluasi", fontSize = 10.sp, color = TextSecondary)
                                Text("${result.day2AreaCm2} cm²", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                            }
                        }
                    }
                }
            }
        }

        // Evaluasi Klinis
        if (result.clinicalEvaluation.isNotBlank()) {
            Card(
                shape = RoundedCornerShape(18.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceCard),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.MedicalInformation, contentDescription = null, tint = TealPrimary)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Evaluasi Klinis Longitudinal", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        result.clinicalEvaluation,
                        fontSize = 13.sp,
                        color = TextPrimary,
                        lineHeight = 19.sp
                    )
                }
            }
        }

        // Rekomendasi Lanjutan
        if (result.recommendations.isNotEmpty()) {
            Card(
                shape = RoundedCornerShape(18.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceCard),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.CheckCircleOutline, contentDescription = null, tint = EmeraldSafe)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Rekomendasi Perawatan Lanjutan", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                    result.recommendations.forEach { rec ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp),
                            verticalAlignment = Alignment.Top
                        ) {
                            Icon(
                                Icons.Default.Check,
                                contentDescription = null,
                                tint = EmeraldSafe,
                                modifier = Modifier
                                    .size(16.dp)
                                    .padding(top = 2.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(rec, fontSize = 13.sp, color = TextPrimary, lineHeight = 18.sp)
                        }
                    }
                }
            }
        }
    }
}
