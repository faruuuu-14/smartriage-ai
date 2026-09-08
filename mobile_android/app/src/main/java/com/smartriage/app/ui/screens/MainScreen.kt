package com.smartriage.app.ui.screens

import androidx.compose.animation.Crossfade
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.smartriage.app.ui.AppTab
import com.smartriage.app.ui.TriageViewModel
import com.smartriage.app.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(viewModel: TriageViewModel) {
    val currentTab by viewModel.currentTab.collectAsState()
    val geminiApiKey by viewModel.geminiApiKey.collectAsState()
    var showSettingsDialog by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = TealPrimary,
                            modifier = Modifier.size(34.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    Icons.Default.HealthAndSafety,
                                    contentDescription = "Logo",
                                    tint = Color.White,
                                    modifier = Modifier.size(22.dp)
                                )
                            }
                        }
                        Spacer(modifier = Modifier.width(10.dp))
                        Column {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(
                                    "SmarTriage AI",
                                    fontWeight = FontWeight.ExtraBold,
                                    fontSize = 17.sp,
                                    color = TextPrimary
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Surface(
                                    shape = RoundedCornerShape(6.dp),
                                    color = EmeraldSafe.copy(alpha = 0.15f)
                                ) {
                                    Row(
                                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Box(
                                            modifier = Modifier
                                                .size(5.dp)
                                                .clip(CircleShape)
                                                .background(EmeraldSafe)
                                        )
                                        Spacer(modifier = Modifier.width(4.dp))
                                        Text(
                                            "CDSS Siaga",
                                            fontSize = 9.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = EmeraldSafe
                                        )
                                    }
                                }
                            }
                            Text(
                                "Clinical Decision Support System",
                                fontSize = 11.sp,
                                color = TextSecondary
                            )
                        }
                    }
                },
                actions = {
                    IconButton(onClick = { showSettingsDialog = true }) {
                        Icon(
                            Icons.Outlined.Key,
                            contentDescription = "Pengaturan API Key",
                            tint = if (geminiApiKey.isNotBlank()) TealPrimary else TextSecondary
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = SurfaceCard
                )
            )
        },
        bottomBar = {
            NavigationBar(
                containerColor = SurfaceCard,
                tonalElevation = 6.dp
            ) {
                NavigationBarItem(
                    selected = currentTab == AppTab.TRIAGE,
                    onClick = { viewModel.currentTab.value = AppTab.TRIAGE },
                    icon = {
                        Icon(
                            if (currentTab == AppTab.TRIAGE) Icons.Default.MedicalServices else Icons.Outlined.MedicalServices,
                            contentDescription = "Triase"
                        )
                    },
                    label = {
                        Text(
                            "Triase CDSS",
                            fontWeight = if (currentTab == AppTab.TRIAGE) FontWeight.Bold else FontWeight.Normal,
                            fontSize = 11.sp
                        )
                    },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color.White,
                        indicatorColor = TealPrimary,
                        selectedTextColor = TealPrimary,
                        unselectedIconColor = TextSecondary,
                        unselectedTextColor = TextSecondary
                    )
                )

                NavigationBarItem(
                    selected = currentTab == AppTab.TRACKER,
                    onClick = { viewModel.currentTab.value = AppTab.TRACKER },
                    icon = {
                        Icon(
                            if (currentTab == AppTab.TRACKER) Icons.Default.TrendingDown else Icons.Outlined.TrendingDown,
                            contentDescription = "Trajektori"
                        )
                    },
                    label = {
                        Text(
                            "Trajektori",
                            fontWeight = if (currentTab == AppTab.TRACKER) FontWeight.Bold else FontWeight.Normal,
                            fontSize = 11.sp
                        )
                    },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color.White,
                        indicatorColor = TealPrimary,
                        selectedTextColor = TealPrimary,
                        unselectedIconColor = TextSecondary,
                        unselectedTextColor = TextSecondary
                    )
                )

                NavigationBarItem(
                    selected = currentTab == AppTab.CHAT,
                    onClick = { viewModel.currentTab.value = AppTab.CHAT },
                    icon = {
                        Icon(
                            if (currentTab == AppTab.CHAT) Icons.Default.ChatBubble else Icons.Outlined.ChatBubbleOutline,
                            contentDescription = "Konsultasi"
                        )
                    },
                    label = {
                        Text(
                            "Konsultasi",
                            fontWeight = if (currentTab == AppTab.CHAT) FontWeight.Bold else FontWeight.Normal,
                            fontSize = 11.sp
                        )
                    },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color.White,
                        indicatorColor = TealPrimary,
                        selectedTextColor = TealPrimary,
                        unselectedIconColor = TextSecondary,
                        unselectedTextColor = TextSecondary
                    )
                )
            }
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            Crossfade(targetState = currentTab, label = "TabTransition") { tab ->
                when (tab) {
                    AppTab.TRIAGE -> TriageScreen(viewModel = viewModel)
                    AppTab.TRACKER -> TrackerScreen(viewModel = viewModel)
                    AppTab.CHAT -> ConsultChatScreen(viewModel = viewModel)
                }
            }
        }
    }

    // Modal Dialog API Key Gemini Opsional
    if (showSettingsDialog) {
        var tempKey by remember { mutableStateOf(geminiApiKey) }

        AlertDialog(
            onDismissRequest = { showSettingsDialog = false },
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.VpnKey, contentDescription = null, tint = TealPrimary)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("API Key Gemini (Opsional)", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
            },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(
                        "Jika server lokal kehabisan kuota atau Anda ingin menggunakan kuota pribadi, Anda dapat memasukkan Gemini API Key Anda sendiri.",
                        fontSize = 12.sp,
                        color = TextSecondary,
                        lineHeight = 17.sp
                    )
                    OutlinedTextField(
                        value = tempKey,
                        onValueChange = { tempKey = it },
                        placeholder = { Text("AIzaSy...", fontSize = 12.sp) },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp)
                    )
                    Text(
                        "Catatan: Aplikasi terhubung default ke backend server di http://10.0.2.2:8000/ (Emulator) atau IP lokal Wi-Fi.",
                        fontSize = 11.sp,
                        color = Color(0xFF94A3B8)
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        viewModel.geminiApiKey.value = tempKey.trim()
                        showSettingsDialog = false
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Text("Simpan")
                }
            },
            dismissButton = {
                TextButton(onClick = { showSettingsDialog = false }) {
                    Text("Tutup", color = TextSecondary)
                }
            }
        )
    }
}
