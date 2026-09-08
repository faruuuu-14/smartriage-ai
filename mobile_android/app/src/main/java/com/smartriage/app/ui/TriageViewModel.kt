package com.smartriage.app.ui

import android.graphics.Bitmap
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.smartriage.app.data.api.TriageApiService
import com.smartriage.app.data.model.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.ByteArrayOutputStream

enum class AppTab {
    TRIAGE, TRACKER, CHAT
}

sealed class TriageUiState {
    object Idle : TriageUiState()
    object Loading : TriageUiState()
    data class Success(val result: TriageResponse, val originalBitmap: Bitmap?) : TriageUiState()
    data class Error(val message: String) : TriageUiState()
}

sealed class TrackerUiState {
    object Idle : TrackerUiState()
    object Loading : TrackerUiState()
    data class Success(val result: WoundProgressResponse) : TrackerUiState()
    data class Error(val message: String) : TrackerUiState()
}

class TriageViewModel(
    private val apiService: TriageApiService = TriageApiService.create()
) : ViewModel() {

    // Tab Navigasi Aktif
    val currentTab = MutableStateFlow(AppTab.TRIAGE)

    // UI States
    private val _uiState = MutableStateFlow<TriageUiState>(TriageUiState.Idle)
    val uiState: StateFlow<TriageUiState> = _uiState

    private val _trackerState = MutableStateFlow<TrackerUiState>(TrackerUiState.Idle)
    val trackerState: StateFlow<TrackerUiState> = _trackerState

    // 1. Profil Pasien & Peta Tubuh
    val patientGroup = MutableStateFlow("DEWASA") // DEWASA, ANAK, BAYI, HAMIL_MENYUSUI
    val bodyLocation = MutableStateFlow("AUTO")   // AUTO, KEPALA_WAJAH, DADA_PERUT, PUNGGUNG, etc.

    // 2. Fokus Makro & Foto
    val complaintCategory = MutableStateFlow("AUTO") // AUTO, LUKA, GATAL, KUKU, RAMBUT
    val selectedBitmap = MutableStateFlow<Bitmap?>(null)

    // 3. Gejala & Skala Nyeri
    val activeSymptomTab = MutableStateFlow("skin") // wound, skin, nail, hair
    val painLevel = MutableStateFlow(1)

    // Gejala Ragam Luka Fisik
    val symPuncture = MutableStateFlow(false)
    val symAnimalBite = MutableStateFlow(false)
    val symBurnCharred = MutableStateFlow(false)
    val symBurnBlister = MutableStateFlow(false)
    val symBedsores = MutableStateFlow(false)
    val symBruiseBlunt = MutableStateFlow(false)
    val symCleanCut = MutableStateFlow(false)

    // Gejala Kulit & Gatal
    val symItch = MutableStateFlow(false)
    val symBumps = MutableStateFlow(false)
    val symNight = MutableStateFlow(false)
    val symRing = MutableStateFlow(false)
    val symBlister = MutableStateFlow(false)
    val symDry = MutableStateFlow(false)

    // Gejala Kuku
    val symNailIngrown = MutableStateFlow(false)
    val symNailFungus = MutableStateFlow(false)
    val symNailTrauma = MutableStateFlow(false)

    // Gejala Rambut
    val symScalpDandruff = MutableStateFlow(false)
    val symHairLossPatch = MutableStateFlow(false)
    val symHeadLice = MutableStateFlow(false)

    // Tanda Bahaya (Red Flags)
    val riskTetanus = MutableStateFlow(false)
    val riskBleeding = MutableStateFlow(false)
    val riskDeep = MutableStateFlow(false)
    val riskFace = MutableStateFlow(false)
    val riskFever = MutableStateFlow(false)

    // API Key Opsional
    val geminiApiKey = MutableStateFlow("")

    // Hasil Analisis Terakhir
    var lastResult: TriageResponse? = null
        private set

    // Chat State
    val chatMessages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val chatInput = MutableStateFlow("")
    val isChatLoading = MutableStateFlow(false)
    val quickChips = MutableStateFlow<List<String>>(
        listOf(
            "Apakah boleh mandi?",
            "Bagaimana cara mencegah bopeng/bekas luka?",
            "Apakah ada pantangan makanan?",
            "Kapan harus ke dokter?"
        )
    )

    // Tracker State
    val trackerBitmapDay1 = MutableStateFlow<Bitmap?>(null)
    val trackerBitmapDay2 = MutableStateFlow<Bitmap?>(null)

    fun selectComplaintCategory(cat: String) {
        complaintCategory.value = cat
        when (cat) {
            "LUKA" -> activeSymptomTab.value = "wound"
            "KUKU" -> activeSymptomTab.value = "nail"
            "RAMBUT" -> activeSymptomTab.value = "hair"
            else -> activeSymptomTab.value = "skin"
        }
    }

    fun analyzeImage() {
        val bitmap = selectedBitmap.value ?: return
        viewModelScope.launch {
            _uiState.value = TriageUiState.Loading
            try {
                val stream = ByteArrayOutputStream()
                bitmap.compress(Bitmap.CompressFormat.JPEG, 90, stream)
                val byteArray = stream.toByteArray()

                val requestFile = byteArray.toRequestBody("image/jpeg".toMediaTypeOrNull())
                val filePart = MultipartBody.Part.createFormData("file", "wound_scan.jpg", requestFile)

                fun strBody(str: String) = str.toRequestBody("text/plain".toMediaTypeOrNull())
                fun boolBody(b: Boolean) = b.toString().toRequestBody("text/plain".toMediaTypeOrNull())

                val apiKeyBody = if (geminiApiKey.value.isNotBlank()) strBody(geminiApiKey.value) else null

                val response = apiService.analyzeWound(
                    file = filePart,
                    complaintCategory = strBody(complaintCategory.value),
                    bodyLocation = strBody(bodyLocation.value),
                    patientGroup = strBody(patientGroup.value),
                    painLevel = strBody(painLevel.value.toString()),
                    hasTetanusRisk = boolBody(riskTetanus.value),
                    isBleedingUncontrolled = boolBody(riskBleeding.value),
                    isDeepCut = boolBody(riskDeep.value),
                    isFaceOrJoint = boolBody(riskFace.value),
                    hasFever = boolBody(riskFever.value),
                    symPuncture = boolBody(symPuncture.value),
                    symAnimalBite = boolBody(symAnimalBite.value),
                    symBurnBlister = boolBody(symBurnBlister.value),
                    symBurnCharred = boolBody(symBurnCharred.value),
                    symBruiseBlunt = boolBody(symBruiseBlunt.value),
                    symBedsores = boolBody(symBedsores.value),
                    symCleanCut = boolBody(symCleanCut.value),
                    symItch = boolBody(symItch.value),
                    symBumps = boolBody(symBumps.value),
                    symNight = boolBody(symNight.value),
                    symRing = boolBody(symRing.value),
                    symDry = boolBody(symDry.value),
                    symBlister = boolBody(symBlister.value),
                    symNailIngrown = boolBody(symNailIngrown.value),
                    symNailFungus = boolBody(symNailFungus.value),
                    symNailTrauma = boolBody(symNailTrauma.value),
                    symScalpDandruff = boolBody(symScalpDandruff.value),
                    symHairLossPatch = boolBody(symHairLossPatch.value),
                    symHeadLice = boolBody(symHeadLice.value),
                    geminiApiKey = apiKeyBody
                )

                lastResult = response
                _uiState.value = TriageUiState.Success(response, bitmap)

                // Inisialisasi Chat Welcome Message
                chatMessages.value = listOf(
                    ChatMessage(
                        text = "Halo! Saya Asisten Dokter Virtual SmarTriage AI. Saya siap menjawab pertanyaan seputar perawatan ${response.commonName} (${response.medicalName}), panduan mandi, makanan, atau pencegahan bekas luka.",
                        isUser = false
                    )
                )
            } catch (e: Exception) {
                _uiState.value = TriageUiState.Error("Koneksi gagal: Pastikan server aktif (${e.localizedMessage})")
            }
        }
    }

    fun sendChatMessage(customText: String? = null) {
        val text = customText ?: chatInput.value.trim()
        if (text.isBlank()) return

        val conditionKey = lastResult?.conditionKey ?: "LUKA_LECET"
        val userMsg = ChatMessage(text = text, isUser = true)
        chatMessages.value = chatMessages.value + userMsg
        chatInput.value = ""
        isChatLoading.value = true

        viewModelScope.launch {
            try {
                val req = ConsultChatRequest(
                    conditionKey = conditionKey,
                    message = text,
                    patientGroup = patientGroup.value,
                    geminiApiKey = if (geminiApiKey.value.isNotBlank()) geminiApiKey.value else null
                )
                val resp = apiService.sendConsultChat(req)
                val aiMsg = ChatMessage(text = resp.reply, isUser = false)
                chatMessages.value = chatMessages.value + aiMsg
                if (!resp.suggestedQuestions.isNullOrEmpty()) {
                    quickChips.value = resp.suggestedQuestions
                }
            } catch (e: Exception) {
                val errorMsg = ChatMessage(
                    text = "Maaf, terjadi kendala saat menghubungkan ke asisten virtual: ${e.localizedMessage}",
                    isUser = false
                )
                chatMessages.value = chatMessages.value + errorMsg
            } finally {
                isChatLoading.value = false
            }
        }
    }

    fun evaluateWoundProgress() {
        val b1 = trackerBitmapDay1.value ?: return
        val b2 = trackerBitmapDay2.value ?: return

        viewModelScope.launch {
            _trackerState.value = TrackerUiState.Loading
            try {
                fun toPart(b: Bitmap, name: String): MultipartBody.Part {
                    val s = ByteArrayOutputStream()
                    b.compress(Bitmap.CompressFormat.JPEG, 90, s)
                    val r = s.toByteArray().toRequestBody("image/jpeg".toMediaTypeOrNull())
                    return MultipartBody.Part.createFormData(name, "$name.jpg", r)
                }

                val p1 = toPart(b1, "file_day1")
                val p2 = toPart(b2, "file_day2")
                val res = apiService.trackWoundProgress(p1, p2)
                _trackerState.value = TrackerUiState.Success(res)
            } catch (e: Exception) {
                _trackerState.value = TrackerUiState.Error("Gagal evaluasi progres: ${e.localizedMessage}")
            }
        }
    }

    fun resetTriage() {
        _uiState.value = TriageUiState.Idle
        selectedBitmap.value = null
    }
}
