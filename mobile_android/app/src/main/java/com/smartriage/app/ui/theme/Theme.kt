package com.smartriage.app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val TealPrimary = Color(0xFF0D9488)
val TealDark = Color(0xFF0F766E)
val TealLight = Color(0xFFF0FDFA)
val TealBorder = Color(0xFF99F6E4)
val EmeraldSafe = Color(0xFF10B981)
val EmeraldLight = Color(0xFFECFDF5)
val AmberWarning = Color(0xFFF59E0B)
val AmberLight = Color(0xFFFFFBEB)
val RoseEmergency = Color(0xFFE11D48)
val RoseLight = Color(0xFFFFF1F2)
val IndigoAi = Color(0xFF6366F1)
val IndigoLight = Color(0xFFEEF2FF)
val BackgroundLight = Color(0xFFF8FAFC)
val SurfaceCard = Color(0xFFFFFFFF)
val TextDark = Color(0xFF0F172A)
val TextMuted = Color(0xFF64748B)
val BorderLight = Color(0xFFE2E8F0)

private val LightColorScheme = lightColorScheme(
    primary = TealPrimary,
    onPrimary = Color.White,
    primaryContainer = TealLight,
    onPrimaryContainer = TealDark,
    secondary = EmeraldSafe,
    onSecondary = Color.White,
    secondaryContainer = EmeraldLight,
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
