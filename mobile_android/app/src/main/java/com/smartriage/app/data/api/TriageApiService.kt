package com.smartriage.app.data.api

import com.smartriage.app.data.model.TriageResponse
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.RequestBody
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part
import java.util.concurrent.TimeUnit

interface TriageApiService {
    @Multipart
    @POST("api/v1/triage/analyze")
    suspend fun analyzeWound(
        @Part file: MultipartBody.Part,
        @Part("has_tetanus_risk") hasTetanusRisk: RequestBody,
        @Part("is_bleeding_uncontrolled") isBleedingUncontrolled: RequestBody,
        @Part("is_deep_cut") isDeepCut: RequestBody,
        @Part("is_face_or_joint") isFaceOrJoint: RequestBody
    ): TriageResponse

    companion object {
        // Alamat IP 10.0.2.2 adalah IP host komputer jika dijalankan dari Android Emulator
        // Jika menggunakan HP fisik via Wi-Fi yang sama, ganti dengan IP lokal laptop (misal 192.168.1.X)
        private const val BASE_URL = "http://10.0.2.2:8000/"

        fun create(): TriageApiService {
            val logging = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }

            val client = OkHttpClient.Builder()
                .addInterceptor(logging)
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .build()

            return Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(client)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(TriageApiService::class.java)
        }
    }
}
