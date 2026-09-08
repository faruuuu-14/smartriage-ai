package com.smartriage.app.ui.screens

import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.util.Base64
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.result.launch
import androidx.compose.animation.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
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
import com.smartriage.app.data.model.TriageResponse
import com.smartriage.app.ui.AppTab
import com.smartriage.app.ui.TriageUiState
import com.smartriage.app.ui.TriageViewModel
import com.smartriage.app.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TriageScreen(viewModel: TriageViewModel) {
    val context = LocalContext.current
    val uiState by viewModel.uiState.collectAsState()
    val selectedBitmap by viewModel.selectedBitmap.collectAsState()
    val scrollState = rememberScrollState()

    // Kamera Launcher
    val cameraLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap ->
        if (bitmap != null) {
            viewModel.selectedBitmap.value = bitmap
        }
    }

    // Galeri Launcher
    val galleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            try {
                val inputStream = context.contentResolver.openInputStream(uri)
                val bitmap = BitmapFactory.decodeStream(inputStream)
                if (bitmap != null) {
                    viewModel.selectedBitmap.value = bitmap
                }
            } catch (e: Exception) {
                // Handle decode error
            }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {

        // =========================================================================
        // LANGKAH 1: PROFIL PASIEN & BODY MAP (DEMOGRAFI & LOKASI ANATOMIS)
        // =========================================================================
        Card(
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceCard),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = TealPrimary,
                            modifier = Modifier.size(26.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Text("1", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Column {
                            Text("Profil Pasien & Peta Tubuh", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = TextDark)
                            Text("Cegah kontraindikasi & tentukan lokasi", fontSize = 11.sp, color = TextMuted)
                        }
                    }
                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = TealLight,
                        border = BorderStroke(1.dp, TealBorder)
                    ) {
                        Text("Safety Guard", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = TealDark, modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp))
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Kelompok Pasien Selector
                Text("Kelompok Pasien (Pencegahan Bahaya Obat):", fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = TextDark)
                Spacer(modifier = Modifier.height(6.dp))

                val currentGroup by viewModel.patientGroup.collectAsState()
                val groups = listOf(
                    "DEWASA" to "Dewasa (18-64 thn)",
                    "ANAK" to "Anak (2-17 thn) • Waspada Reye",
                    "BAYI" to "Bayi (<2 thn) • Waspada Salep Keras",
                    "HAMIL_MENYUSUI" to "Ibu Hamil / Menyusui"
                )

                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    groups.forEach { (key, label) ->
                        val isSelected = currentGroup == key
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = if (isSelected) TealLight else Color(0xFFF8FAFC),
                            border = BorderStroke(1.dp, if (isSelected) TealPrimary else BorderLight),
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { viewModel.patientGroup.value = key }
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp)
                            ) {
                                RadioButton(
                                    selected = isSelected,
                                    onClick = { viewModel.patientGroup.value = key },
                                    colors = RadioButtonDefaults.colors(selectedColor = TealPrimary),
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(label, fontSize = 11.sp, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal, color = if (isSelected) TealDark else TextDark)
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Peta Anatomi Tubuh (Body Map Chips)
                val currentBodyLoc by viewModel.bodyLocation.collectAsState()
                Text("Lokasi Anatomis Tubuh (Body Map):", fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = TextDark)
                Spacer(modifier = Modifier.height(6.dp))

                val locations = listOf(
                    "AUTO" to "🤖 Auto",
                    "KEPALA_WAJAH" to "👤 Wajah",
                    "DADA_PERUT" to "👕 Dada",
                    "PUNGGUNG" to "🛡️ Punggung",
                    "SELA_JARI_TANGAN" to "🖐️ Sela Jari",
                    "LUTUT_SIKU_KAKI" to "🦵 Kaki/Siku",
                    "KUKU_JARI" to "💅 Kuku",
                    "PINGGANG_DERMATOM" to "⚡ Dermatom"
                )

                // Grid 4 x 2 Chips
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                    locations.take(4).forEach { (loc, label) ->
                        val isSel = currentBodyLoc == loc
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = if (isSel) TealPrimary else Color(0xFFF1F5F9),
                            modifier = Modifier
                                .weight(1f)
                                .clickable { viewModel.bodyLocation.value = loc }
                        ) {
                            Text(
                                text = label,
                                fontSize = 10.sp,
                                fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium,
                                color = if (isSel) Color.White else TextDark,
                                modifier = Modifier.padding(vertical = 8.dp),
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(6.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                    locations.drop(4).forEach { (loc, label) ->
                        val isSel = currentBodyLoc == loc
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = if (isSel) TealPrimary else Color(0xFFF1F5F9),
                            modifier = Modifier
                                .weight(1f)
                                .clickable { viewModel.bodyLocation.value = loc }
                        ) {
                            Text(
                                text = label,
                                fontSize = 10.sp,
                                fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium,
                                color = if (isSel) Color.White else TextDark,
                                modifier = Modifier.padding(vertical = 8.dp),
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                            )
                        }
                    }
                }
            }
        }

        // =========================================================================
        // LANGKAH 2: FOKUS MAKRO & FOTO LESI (KAMERA / GALERI)
        // =========================================================================
        Card(
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceCard),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = Color(0xFF0284C7),
                            modifier = Modifier.size(26.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Text("2", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Column {
                            Text("Fokus Makro & Foto Lesi", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = TextDark)
                            Text("Pilih kategori domain & unggah foto", fontSize = 11.sp, color = TextMuted)
                        }
                    }
                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = Color(0xFFE0F2FE),
                        border = BorderStroke(1.dp, Color(0xFFBAE6FD))
                    ) {
                        Text("Gatekeeper On", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0369A1), modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp))
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Fokus Makro Segmented Chips
                val currentCategory by viewModel.complaintCategory.collectAsState()
                Text("Fokus Makro Pemeriksaan:", fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = TextDark)
                Spacer(modifier = Modifier.height(6.dp))

                val categories = listOf(
                    "AUTO" to "🤖 Auto",
                    "LUKA" to "🩹 Luka",
                    "GATAL" to "🌿 Kulit",
                    "KUKU" to "💅 Kuku",
                    "RAMBUT" to "💇 Rambut"
                )

                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                    categories.forEach { (cat, label) ->
                        val isSel = currentCategory == cat
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = if (isSel) Color(0xFF0284C7) else Color(0xFFF1F5F9),
                            modifier = Modifier
                                .weight(1f)
                                .clickable { viewModel.selectComplaintCategory(cat) }
                        ) {
                            Text(
                                text = label,
                                fontSize = 10.sp,
                                fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium,
                                color = if (isSel) Color.White else TextDark,
                                modifier = Modifier.padding(vertical = 7.dp),
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Area Foto Preview / Upload Dropzone
                if (selectedBitmap != null) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(230.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(Color(0xFFF1F5F9))
                    ) {
                        Image(
                            bitmap = selectedBitmap!!.asImageBitmap(),
                            contentDescription = "Foto Lesi",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.Crop
                        )
                        IconButton(
                            onClick = { viewModel.selectedBitmap.value = null },
                            modifier = Modifier
                                .align(Alignment.TopEnd)
                                .padding(10.dp)
                                .background(Color.Black.copy(alpha = 0.65f), CircleShape)
                                .size(34.dp)
                        ) {
                            Icon(Icons.Default.Close, contentDescription = "Hapus", tint = Color.White, modifier = Modifier.size(18.dp))
                        }
                    }
                } else {
                    Surface(
                        shape = RoundedCornerShape(16.dp),
                        color = Color(0xFFF8FAFC),
                        border = BorderStroke(1.5.dp, BorderLight),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(160.dp)
                    ) {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center,
                            modifier = Modifier.padding(16.dp)
                        ) {
                            Surface(
                                shape = CircleShape,
                                color = TealLight,
                                modifier = Modifier.size(46.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Icon(Icons.Default.CameraAlt, contentDescription = null, tint = TealPrimary, modifier = Modifier.size(24.dp))
                                }
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            Text("Ambil Foto atau Pilih dari Galeri", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = TextDark)
                            Text("Luka tusuk, gigitan hewan, luka bakar, ruam, kuku, atau rambut", fontSize = 11.sp, color = TextMuted)
                        }
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                // Tombol Ambil Foto: Kamera & Galeri
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                    OutlinedButton(
                        onClick = { cameraLauncher.launch() },
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.weight(1f)
                    ) {
                        Icon(Icons.Default.PhotoCamera, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Kamera", fontSize = 12.sp)
                    }

                    OutlinedButton(
                        onClick = { galleryLauncher.launch("image/*") },
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.weight(1f)
                    ) {
                        Icon(Icons.Default.PhotoLibrary, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Galeri", fontSize = 12.sp)
                    }
                }
            }
        }

        // =========================================================================
        // LANGKAH 3: CIRI GEJALA SPESIFIK & SKALA NYERI
        // =========================================================================
        Card(
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceCard),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = IndigoAi,
                            modifier = Modifier.size(26.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Text("3", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Column {
                            Text("Ciri Gejala & Skala Nyeri", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = TextDark)
                            Text("Karakteristik klinis & sensasi subjektif", fontSize = 11.sp, color = TextMuted)
                        }
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Mini Tabs Kategori Gejala
                val activeTab by viewModel.activeSymptomTab.collectAsState()
                val symTabs = listOf(
                    "wound" to "🩹 Luka",
                    "skin" to "🌿 Kulit",
                    "nail" to "💅 Kuku",
                    "hair" to "💇 Rambut"
                )

                Row(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFFF1F5F9), RoundedCornerShape(10.dp))
                        .padding(4.dp)
                ) {
                    symTabs.forEach { (tabKey, tabLabel) ->
                        val isSel = activeTab == tabKey
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = if (isSel) SurfaceCard else Color.Transparent,
                            modifier = Modifier
                                .weight(1f)
                                .clickable { viewModel.activeSymptomTab.value = tabKey }
                        ) {
                            Text(
                                text = tabLabel,
                                fontSize = 10.sp,
                                fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium,
                                color = if (isSel) TealDark else TextMuted,
                                modifier = Modifier.padding(vertical = 6.dp),
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                // Checklist Gejala Sesuai Tab Aktif
                when (activeTab) {
                    "wound" -> {
                        SymptomCheckbox(
                            title = "Tertusuk paku / kawat / duri tajam",
                            subtitle = "⚠️ Risiko Tinggi Spora Tetanus",
                            checked = viewModel.symPuncture.collectAsState().value,
                            onCheckedChange = { viewModel.symPuncture.value = it },
                            isEmergency = true
                        )
                        SymptomCheckbox(
                            title = "Gigitan / cakaran anjing, kucing liar",
                            subtitle = "⚠️ Risiko Infeksi Virus Rabies",
                            checked = viewModel.symAnimalBite.collectAsState().value,
                            onCheckedChange = { viewModel.symAnimalBite.value = it },
                            isEmergency = true
                        )
                        SymptomCheckbox(
                            title = "Luka bakar hangus arang / putih mati rasa",
                            subtitle = "Derajat 3 (Full-thickness) butuh bedah",
                            checked = viewModel.symBurnCharred.collectAsState().value,
                            onCheckedChange = { viewModel.symBurnCharred.value = it },
                            isEmergency = true
                        )
                        SymptomCheckbox(
                            title = "Luka bakar melepuh gelembung air (Bula)",
                            subtitle = "Derajat 2 (Partial-thickness) jangan pecah",
                            checked = viewModel.symBurnBlister.collectAsState().value,
                            onCheckedChange = { viewModel.symBurnBlister.value = it }
                        )
                        SymptomCheckbox(
                            title = "Luka borok tekan tirah baring (Dekubitus)",
                            subtitle = "Iskemia jaringan akibat penekanan lama",
                            checked = viewModel.symBedsores.collectAsState().value,
                            onCheckedChange = { viewModel.symBedsores.value = it }
                        )
                        SymptomCheckbox(
                            title = "Benturan tumpul timbul memar lebam biru",
                            subtitle = "Kontusio jaringan lunak",
                            checked = viewModel.symBruiseBlunt.collectAsState().value,
                            onCheckedChange = { viewModel.symBruiseBlunt.value = it }
                        )
                        SymptomCheckbox(
                            title = "Sayatan pisau / kaca tepi lurus rapi",
                            subtitle = "Luka sayat (vulnus scissum)",
                            checked = viewModel.symCleanCut.collectAsState().value,
                            onCheckedChange = { viewModel.symCleanCut.value = it }
                        )
                    }
                    "skin" -> {
                        SymptomCheckbox(
                            title = "Terasa sangat gatal / dorongan menggaruk",
                            subtitle = "Pruritus aktif pada kulit",
                            checked = viewModel.symItch.collectAsState().value,
                            onCheckedChange = { viewModel.symItch.value = it }
                        )
                        SymptomCheckbox(
                            title = "Bentol merah menonjol cepat berpindah",
                            subtitle = "Biduran / Urtikaria",
                            checked = viewModel.symBumps.collectAsState().value,
                            onCheckedChange = { viewModel.symBumps.value = it }
                        )
                        SymptomCheckbox(
                            title = "Gatal memuncak malam hari di sela jari",
                            subtitle = "Skabies / Kudis (Sarcoptes scabiei)",
                            checked = viewModel.symNight.collectAsState().value,
                            onCheckedChange = { viewModel.symNight.value = it }
                        )
                        SymptomCheckbox(
                            title = "Ruam melingkar mirip cincin tepi merah",
                            subtitle = "Kurap / Kadas (Tinea Corporis)",
                            checked = viewModel.symRing.collectAsState().value,
                            onCheckedChange = { viewModel.symRing.value = it }
                        )
                        SymptomCheckbox(
                            title = "Lenting gelembung kecil berair",
                            subtitle = "Cacar Air (Varicella) / Cacar Api (Herpes)",
                            checked = viewModel.symBlister.collectAsState().value,
                            onCheckedChange = { viewModel.symBlister.value = it },
                            isEmergency = true
                        )
                        SymptomCheckbox(
                            title = "Kulit sangat kering, menebal dan bersisik",
                            subtitle = "Eksim / Dermatitis Atopik",
                            checked = viewModel.symDry.collectAsState().value,
                            onCheckedChange = { viewModel.symDry.value = it }
                        )
                    }
                    "nail" -> {
                        SymptomCheckbox(
                            title = "Tepi kuku menusuk daging bengkak bernanah",
                            subtitle = "Cantengan (Paronikia / Ingrown Toenail)",
                            checked = viewModel.symNailIngrown.collectAsState().value,
                            onCheckedChange = { viewModel.symNailIngrown.value = it },
                            isEmergency = true
                        )
                        SymptomCheckbox(
                            title = "Kuku menebal rapuh warna kuning/cokelat",
                            subtitle = "Jamur Kuku (Onikomikosis)",
                            checked = viewModel.symNailFungus.collectAsState().value,
                            onCheckedChange = { viewModel.symNailFungus.value = it }
                        )
                        SymptomCheckbox(
                            title = "Kuku terjepit timbul bercak darah hitam/ungu",
                            subtitle = "Hematoma Subungual",
                            checked = viewModel.symNailTrauma.collectAsState().value,
                            onCheckedChange = { viewModel.symNailTrauma.value = it }
                        )
                    }
                    "hair" -> {
                        SymptomCheckbox(
                            title = "Ketombe tebal berkerak kuning berminyak",
                            subtitle = "Dermatitis Seboroik / Cradle Cap",
                            checked = viewModel.symScalpDandruff.collectAsState().value,
                            onCheckedChange = { viewModel.symScalpDandruff.value = it }
                        )
                        SymptomCheckbox(
                            title = "Rambut rontok pitak koin bulat licin",
                            subtitle = "Alopecia Areata (Kebotakan setempat)",
                            checked = viewModel.symHairLossPatch.collectAsState().value,
                            onCheckedChange = { viewModel.symHairLossPatch.value = it }
                        )
                        SymptomCheckbox(
                            title = "Gatal merayap & bintik telur di batang rambut",
                            subtitle = "Kutu Kepala (Pedikulosis Kapitis)",
                            checked = viewModel.symHeadLice.collectAsState().value,
                            onCheckedChange = { viewModel.symHeadLice.value = it }
                        )
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))
                Divider(color = BorderLight)
                Spacer(modifier = Modifier.height(14.dp))

                // Skala Nyeri 1-10 Slider
                val currentPain by viewModel.painLevel.collectAsState()
                val (painEmoji, painDesc) = when {
                    currentPain <= 3 -> "😊" to "Bebas Nyeri / Ringan"
                    currentPain <= 6 -> "😐" to "Nyeri Sedang"
                    currentPain <= 8 -> "😣" to "Nyeri Berat"
                    else -> "🚨" to "Sangat Tak Tertahankan"
                }

                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Skala Nyeri / Perih:", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = TextDark)
                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = Color(0xFFF1F5F9),
                        border = BorderStroke(1.dp, BorderLight)
                    ) {
                        Text("$currentPain/10 ($painEmoji $painDesc)", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = TextDark, modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp))
                    }
                }

                Slider(
                    value = currentPain.toFloat(),
                    onValueChange = { viewModel.painLevel.value = it.toInt() },
                    valueRange = 1f..10f,
                    steps = 8,
                    colors = SliderDefaults.colors(
                        thumbColor = TealPrimary,
                        activeTrackColor = TealPrimary,
                        inactiveTrackColor = Color(0xFFE2E8F0)
                    )
                )

                Spacer(modifier = Modifier.height(10.dp))

                // Red Flags Collapsible
                var isRedFlagsExpanded by remember { mutableStateOf(false) }
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = RoseLight,
                    border = BorderStroke(1.dp, Color(0xFFFECDD3)),
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { isRedFlagsExpanded = !isRedFlagsExpanded }
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Warning, contentDescription = null, tint = RoseEmergency, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("Tanda Bahaya Darurat / Red Flags (Opsional)", fontWeight = FontWeight.Bold, fontSize = 11.sp, color = Color(0xFF9F1239))
                            }
                            Icon(
                                if (isRedFlagsExpanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                                contentDescription = null,
                                tint = RoseEmergency,
                                modifier = Modifier.size(18.dp)
                            )
                        }

                        if (isRedFlagsExpanded) {
                            Spacer(modifier = Modifier.height(8.dp))
                            RedFlagCheckbox("Tercampur paku berkarat / tanah (Tetanus)", viewModel.riskTetanus.collectAsState().value) { viewModel.riskTetanus.value = it }
                            RedFlagCheckbox("Pendarahan deras tidak henti > 10 menit", viewModel.riskBleeding.collectAsState().value) { viewModel.riskBleeding.value = it }
                            RedFlagCheckbox("Luka robek menganga dalam (>0.5 cm)", viewModel.riskDeep.collectAsState().value) { viewModel.riskDeep.value = it }
                            RedFlagCheckbox("Di area wajah dekat mata atau sendi", viewModel.riskFace.collectAsState().value) { viewModel.riskFace.value = it }
                            RedFlagCheckbox("Disertai demam tinggi atau menggigil", viewModel.riskFever.collectAsState().value) { viewModel.riskFever.value = it }
                        }
                    }
                }
            }
        }

        // =========================================================================
        // TOMBOL CTA UTAMA ANALISIS
        // =========================================================================
        Button(
            onClick = { viewModel.analyzeImage() },
            enabled = selectedBitmap != null && uiState !is TriageUiState.Loading,
            shape = RoundedCornerShape(16.dp),
            colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp)
        ) {
            if (uiState is TriageUiState.Loading) {
                CircularProgressIndicator(color = Color.White, modifier = Modifier.size(20.dp), strokeWidth = 2.5.dp)
                Spacer(modifier = Modifier.width(10.dp))
                Text("Menganalisis Jaringan & Gejala...", fontWeight = FontWeight.Bold, fontSize = 13.sp)
            } else {
                Icon(Icons.Default.AutoAwesome, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Analisis Integumen, Luka & Triase Medis", fontWeight = FontWeight.Bold, fontSize = 13.sp)
            }
        }

        // =========================================================================
        // DASHBOARD HASIL TRIASE CDSS
        // =========================================================================
        when (val state = uiState) {
            is TriageUiState.Success -> {
                FullResultDashboard(data = state.result, originalBitmap = state.originalBitmap, onOpenChat = {
                    viewModel.currentTab.value = AppTab.CHAT
                })
            }
            is TriageUiState.Error -> {
                Card(
                    shape = RoundedCornerShape(14.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFFEE2E2)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.ErrorOutline, contentDescription = null, tint = RoseEmergency)
                        Spacer(modifier = Modifier.width(10.dp))
                        Text(state.message, color = Color(0xFF991B1B), fontSize = 12.sp)
                    }
                }
            }
            else -> {}
        }
    }
}

// Sub-komponen Checkbox Gejala Berbentuk Kartu
@Composable
fun SymptomCheckbox(
    title: String,
    subtitle: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    isEmergency: Boolean = false
) {
    val bg = if (checked) {
        if (isEmergency) RoseLight else TealLight
    } else Color(0xFFF8FAFC)

    val border = if (checked) {
        if (isEmergency) Color(0xFFFDA4AF) else TealPrimary
    } else BorderLight

    Surface(
        shape = RoundedCornerShape(12.dp),
        color = bg,
        border = BorderStroke(1.dp, border),
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 3.dp)
            .clickable { onCheckedChange(!checked) }
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp)
        ) {
            Checkbox(
                checked = checked,
                onCheckedChange = onCheckedChange,
                colors = CheckboxDefaults.colors(checkedColor = if (isEmergency) RoseEmergency else TealPrimary)
            )
            Spacer(modifier = Modifier.width(4.dp))
            Column {
                Text(title, fontSize = 11.sp, fontWeight = if (checked) FontWeight.Bold else FontWeight.Medium, color = TextDark)
                Text(subtitle, fontSize = 10.sp, color = if (isEmergency) Color(0xFF9F1239) else TextMuted)
            }
        }
    }
}

@Composable
fun RedFlagCheckbox(title: String, checked: Boolean, onCheckedChange: (Boolean) -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onCheckedChange(!checked) }
            .padding(vertical = 2.dp)
    ) {
        Checkbox(
            checked = checked,
            onCheckedChange = onCheckedChange,
            colors = CheckboxDefaults.colors(checkedColor = RoseEmergency),
            modifier = Modifier.size(18.dp)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(title, fontSize = 11.sp, color = TextDark)
    }
}

// Dashboard Hasil Lengkap
@Composable
fun FullResultDashboard(
    data: TriageResponse,
    originalBitmap: Bitmap?,
    onOpenChat: () -> Unit
) {
    val context = LocalContext.current
    val isRed = data.triageLevel == "MERAH"
    val isYellow = data.triageLevel == "KUNING"

    val (cardBg, badgeBg, badgeText) = when {
        isRed -> Triple(RoseLight, RoseEmergency, "LEVEL TRIASE: MERAH (GAWAT DARURAT)")
        isYellow -> Triple(AmberLight, AmberWarning, "LEVEL TRIASE: KUNING (PERIKSA DOKTER)")
        else -> Triple(EmeraldLight, EmeraldSafe, "LEVEL TRIASE: HIJAU (RAWAT MANDIRI)")
    }

    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {

        // 1. Triage Hero Banner
        Card(
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = cardBg),
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
                        shape = RoundedCornerShape(6.dp),
                        color = badgeBg
                    ) {
                        Text(
                            badgeText,
                            color = Color.White,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.ExtraBold,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                        )
                    }
                    Text("Keyakinan: ${data.confidencePercentage}", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = TextMuted)
                }

                Spacer(modifier = Modifier.height(10.dp))

                Text(
                    "${data.commonName} (${data.medicalName})",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Black,
                    color = TextDark
                )

                Spacer(modifier = Modifier.height(4.dp))

                Text(
                    data.triageAction,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = TextDark
                )

                if (data.triageReasons.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    data.triageReasons.forEach { reason ->
                        Text("• $reason", fontSize = 11.sp, color = TextDark)
                    }
                }
            }
        }

        // 2. Emergency Action Bar (Khusus Level MERAH)
        if (isRed) {
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = RoseEmergency),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.LocalHospital, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Kondisi Kegawatdaruratan Medis!", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                    Text("Segera kunjungi IGD Rumah Sakit atau Faskes terdekat", color = Color.White.copy(alpha = 0.9f), fontSize = 11.sp, modifier = Modifier.padding(vertical = 4.dp))

                    Spacer(modifier = Modifier.height(8.dp))

                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        // Buka Google Maps IGD Terdekat
                        Button(
                            onClick = {
                                val mapIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=IGD+rumah+sakit+terdekat"))
                                context.startActivity(mapIntent)
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                            shape = RoundedCornerShape(10.dp),
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.Navigation, contentDescription = null, tint = RoseEmergency, modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("Rute IGD Terdekat", color = RoseEmergency, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        }

                        // Telepon Darurat 119
                        Button(
                            onClick = {
                                val dialIntent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:119"))
                                context.startActivity(dialIntent)
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF9F1239)),
                            shape = RoundedCornerShape(10.dp)
                        ) {
                            Icon(Icons.Default.Phone, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("119", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }

        // 3. Top-3 Differential Diagnosis (DDx)
        if (!data.top3Differential.isNullOrEmpty()) {
            Card(
                shape = RoundedCornerShape(18.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceCard),
                elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Top-3 Diagnosis Banding (DDx)", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = TextDark)
                    Text("Probabilitas komparatif & rasional patologis:", fontSize = 11.sp, color = TextMuted)
                    Spacer(modifier = Modifier.height(10.dp))

                    data.top3Differential.forEachIndexed { index, ddx ->
                        val isTop1 = index == 0
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = if (isTop1) TealLight else Color(0xFFF8FAFC),
                            border = BorderStroke(1.dp, if (isTop1) TealBorder else BorderLight),
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp)
                        ) {
                            Column(modifier = Modifier.padding(10.dp)) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    modifier = Modifier.fillMaxWidth()
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Surface(
                                            shape = CircleShape,
                                            color = if (isTop1) TealPrimary else Color(0xFFCBD5E1),
                                            modifier = Modifier.size(18.dp)
                                        ) {
                                            Box(contentAlignment = Alignment.Center) {
                                                Text("${index + 1}", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                            }
                                        }
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Text("${ddx.commonName} (${ddx.medicalName})", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = TextDark)
                                    }
                                    Text(ddx.percentage, fontSize = 12.sp, fontWeight = FontWeight.Black, color = if (isTop1) TealDark else TextMuted)
                                }

                                Spacer(modifier = Modifier.height(4.dp))
                                Text(ddx.clinicalRationale, fontSize = 10.sp, color = TextDark, lineHeight = 14.sp)
                            }
                        }
                    }
                }
            }
        }

        // 4. Peringatan Keselamatan Obat Demografis
        if (!data.safetyWarnings.isNullOrEmpty()) {
            Card(
                shape = RoundedCornerShape(18.dp),
                colors = CardDefaults.cardColors(containerColor = AmberLight),
                border = BorderStroke(1.dp, Color(0xFFFDE68A)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Shield, contentDescription = null, tint = AmberWarning, modifier = Modifier.size(18.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Pencegahan Bahaya Obat & Kontraindikasi", fontWeight = FontWeight.Bold, fontSize = 12.sp, color = Color(0xFF78350F))
                    }
                    Spacer(modifier = Modifier.height(8.dp))

                    data.safetyWarnings.forEach { warn ->
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = Color.White,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 3.dp)
                        ) {
                            Column(modifier = Modifier.padding(10.dp)) {
                                Text(warn.title, fontWeight = FontWeight.Bold, fontSize = 11.sp, color = RoseEmergency)
                                Text(warn.warningMessage, fontSize = 10.sp, color = TextDark, lineHeight = 14.sp)
                            }
                        }
                    }
                }
            }
        }

        // 5. Explainable AI (Grad-CAM Heatmap)
        Card(
            shape = RoundedCornerShape(18.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceCard),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Explainable AI (Grad-CAM Heatmap)", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = TextDark)
                Text("Peta panas fokus atensi model jaringan", fontSize = 11.sp, color = TextMuted)
                Spacer(modifier = Modifier.height(10.dp))

                Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                    // Original Photo
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.weight(1f)) {
                        Box(
                            modifier = Modifier
                                .height(130.dp)
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFE2E8F0))
                        ) {
                            if (originalBitmap != null) {
                                Image(bitmap = originalBitmap.asImageBitmap(), contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                            }
                        }
                        Text("Foto Asli", fontSize = 11.sp, color = TextMuted, modifier = Modifier.padding(top = 4.dp))
                    }

                    // Heatmap
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.weight(1f)) {
                        val heatmapBitmap = remember(data.heatmapBase64) {
                            try {
                                val clean = data.heatmapBase64?.substringAfter("base64,") ?: ""
                                val bytes = Base64.decode(clean, Base64.DEFAULT)
                                BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
                            } catch (e: Exception) {
                                null
                            }
                        }
                        Box(
                            modifier = Modifier
                                .height(130.dp)
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFE2E8F0))
                        ) {
                            if (heatmapBitmap != null) {
                                Image(bitmap = heatmapBitmap.asImageBitmap(), contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                            }
                        }
                        Text("Peta Panas Grad-CAM", fontSize = 11.sp, color = TealDark, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 4.dp))
                    }
                }
            }
        }

        // 6. Analisis Jaringan Klinis (TIME Framework)
        val tissue = data.tissueAnalysis
        Card(
            shape = RoundedCornerShape(18.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceCard),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Komposisi Jaringan (TIME)", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = TextDark)
                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = TealLight
                    ) {
                        Text("Luas: ${tissue.estimatedAreaCm2} cm²", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = TealDark, modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp))
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))

                // Bar Segmented TIME
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(12.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFE2E8F0))
                ) {
                    if (tissue.granulationPercentage > 0) {
                        Box(modifier = Modifier.weight(tissue.granulationPercentage.coerceAtLeast(1f)).fillMaxHeight().background(RoseEmergency))
                    }
                    if (tissue.sloughPercentage > 0) {
                        Box(modifier = Modifier.weight(tissue.sloughPercentage.coerceAtLeast(1f)).fillMaxHeight().background(AmberWarning))
                    }
                    if (tissue.necroticPercentage > 0) {
                        Box(modifier = Modifier.weight(tissue.necroticPercentage.coerceAtLeast(1f)).fillMaxHeight().background(Color(0xFF1E293B)))
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))

                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                    MetricChip(title = "Granulasi", value = "${tissue.granulationPercentage}%", color = RoseEmergency, modifier = Modifier.weight(1f))
                    MetricChip(title = "Slough", value = "${tissue.sloughPercentage}%", color = AmberWarning, modifier = Modifier.weight(1f))
                    MetricChip(title = "Nekrotik", value = "${tissue.necroticPercentage}%", color = Color(0xFF1E293B), modifier = Modifier.weight(1f))
                }
            }
        }

        // 7. Tab Informasi Medis (P3K, Obat, Mitos)
        var activeTabEdu by remember { mutableStateOf("p3k") }
        Card(
            shape = RoundedCornerShape(18.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceCard),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(4.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFFF1F5F9), RoundedCornerShape(10.dp))
                        .padding(4.dp)
                ) {
                    listOf("p3k" to "P3K", "obat" to "Obat", "mitos" to "Mitos").forEach { (tab, label) ->
                        val isSel = activeTabEdu == tab
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = if (isSel) SurfaceCard else Color.Transparent,
                            modifier = Modifier
                                .weight(1f)
                                .clickable { activeTabEdu = tab }
                        ) {
                            Text(label, fontSize = 11.sp, fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium, color = if (isSel) TealDark else TextMuted, modifier = Modifier.padding(vertical = 6.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                        }
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                when (activeTabEdu) {
                    "p3k" -> {
                        data.firstAidSteps.forEachIndexed { i, s ->
                            Text("${i + 1}. $s", fontSize = 11.sp, color = TextDark, modifier = Modifier.padding(vertical = 2.dp), lineHeight = 15.sp)
                        }
                    }
                    "obat" -> {
                        data.recommendedOtcMeds.forEach { m ->
                            Text("• $m", fontSize = 11.sp, color = TextDark, modifier = Modifier.padding(vertical = 2.dp))
                        }
                    }
                    "mitos" -> {
                        data.mythsAndWarnings.forEach { mw ->
                            Text("✕ $mw", fontSize = 11.sp, color = RoseEmergency, modifier = Modifier.padding(vertical = 2.dp), lineHeight = 15.sp)
                        }
                    }
                }
            }
        }

        // 8. Tombol Alihkan ke Konsultasi Virtual Dokter AI
        Button(
            onClick = onOpenChat,
            colors = ButtonDefaults.buttonColors(containerColor = TealLight),
            border = BorderStroke(1.dp, TealBorder),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier.fillMaxWidth().height(48.dp)
        ) {
            Icon(Icons.Default.ChatBubbleOutline, contentDescription = null, tint = TealDark, modifier = Modifier.size(16.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text("Tanya Dokter AI Seputar Kondisi Ini", color = TealDark, fontWeight = FontWeight.Bold, fontSize = 12.sp)
        }
    }
}

@Composable
fun MetricChip(title: String, value: String, color: Color, modifier: Modifier = Modifier) {
    Surface(
        shape = RoundedCornerShape(10.dp),
        color = Color(0xFFF8FAFC),
        border = BorderStroke(1.dp, BorderLight),
        modifier = modifier
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.padding(vertical = 6.dp)
        ) {
            Text(title, fontSize = 10.sp, color = TextMuted)
            Text(value, fontSize = 12.sp, fontWeight = FontWeight.Bold, color = color)
        }
    }
}
