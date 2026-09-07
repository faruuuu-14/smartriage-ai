package com.smartriage.app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val TealPrimary = Color(0xFF0D9488)
val TealDark = Color(0xFF0F766E)
val EmeraldSafe = Color(0xFF10B981)
val AmberWarning = Color(0xFFF59E0B)
val RoseEmergency = Color(0xFFEF4444)
val BackgroundLight = Color(0xFFF8FAFC)
val SurfaceCard = Color(0xFFFFFFFF)
val TextDark = Color(0xFF0F172A)
val TextMuted = Color(0xFF64748B)

private val LightColorScheme = lightColorScheme(
    primary = TealPrimary,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFCCFBF1),
    secondary = EmeraldSafe,
    background = BackgroundLight,
    surface = SurfaceCard,
    onBackground = TextDark,
    onSurface = TextDark
)

@Composable
fun SmarTriageTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColorScheme,
        content = content
    )
}
