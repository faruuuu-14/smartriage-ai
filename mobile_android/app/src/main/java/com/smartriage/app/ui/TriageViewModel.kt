package com.smartriage.app.ui

import android.content.Context
import android.graphics.Bitmap
import android.net.Uri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.smartriage.app.data.api.TriageApiService
import com.smartriage.app.data.model.TriageResponse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.ByteArrayOutputStream

sealed class TriageUiState {
    object Idle : TriageUiState()
    object Loading : TriageUiState()
    data class Success(val result: TriageResponse, val originalBitmap: Bitmap?) : TriageUiState()
    data class Error(val message: String) : TriageUiState()
}

class TriageViewModel(
    private val apiService: TriageApiService = TriageApiService.create()
) : ViewModel() {

    private val _uiState = MutableStateFlow<TriageUiState>(TriageUiState.Idle)
    val uiState: StateFlow<TriageUiState> = _uiState

    var selectedBitmap = MutableStateFlow<Bitmap?>(null)
    var hasTetanusRisk = MutableStateFlow(false)
    var isBleedingUncontrolled = MutableStateFlow(false)
    var isDeepCut = MutableStateFlow(false)
    var isFaceOrJoint = MutableStateFlow(false)

    fun analyzeImage(bitmap: Bitmap) {
        viewModelScope.launch {
            _uiState.value = TriageUiState.Loading
            try {
                // Konversi Bitmap ke ByteArray
                val stream = ByteArrayOutputStream()
                bitmap.compress(Bitmap.CompressFormat.JPEG, 90, stream)
                val byteArray = stream.toByteArray()

                val requestFile = byteArray.toRequestBody("image/jpeg".toMediaTypeOrNull())
                val body = MultipartBody.Part.createFormData("file", "wound_image.jpg", requestFile)

                val tetanusPart = hasTetanusRisk.value.toString().toRequestBody("text/plain".toMediaTypeOrNull())
                val bleedingPart = isBleedingUncontrolled.value.toString().toRequestBody("text/plain".toMediaTypeOrNull())
                val deepPart = isDeepCut.value.toString().toRequestBody("text/plain".toMediaTypeOrNull())
                val facePart = isFaceOrJoint.value.toString().toRequestBody("text/plain".toMediaTypeOrNull())

                val response = apiService.analyzeWound(body, tetanusPart, bleedingPart, deepPart, facePart)
                _uiState.value = TriageUiState.Success(response, bitmap)
            } catch (e: Exception) {
                _uiState.value = TriageUiState.Error("Koneksi gagal: Pastikan server backend sudah aktif (${e.localizedMessage})")
            }
        }
    }

    fun resetState() {
        _uiState.value = TriageUiState.Idle
        selectedBitmap.value = null
    }
}
