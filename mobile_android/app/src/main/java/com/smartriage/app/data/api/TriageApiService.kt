package com.smartriage.app.data.api

import com.smartriage.app.data.model.ConsultChatRequest
import com.smartriage.app.data.model.ConsultChatResponse
import com.smartriage.app.data.model.TriageResponse
import com.smartriage.app.data.model.WoundProgressResponse
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.RequestBody
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part
import java.util.concurrent.TimeUnit

interface TriageApiService {
    @Multipart
    @POST("api/v1/triage/analyze")
    suspend fun analyzeWound(
        @Part file: MultipartBody.Part,
        @Part("complaint_category") complaintCategory: RequestBody,
        @Part("body_location") bodyLocation: RequestBody,
        @Part("patient_group") patientGroup: RequestBody,
        @Part("pain_level") painLevel: RequestBody,
        @Part("has_tetanus_risk") hasTetanusRisk: RequestBody,
        @Part("is_bleeding_uncontrolled") isBleedingUncontrolled: RequestBody,
        @Part("is_deep_cut") isDeepCut: RequestBody,
        @Part("is_face_or_joint") isFaceOrJoint: RequestBody,
        @Part("has_fever") hasFever: RequestBody,
        @Part("symptom_puncture_nail") symPuncture: RequestBody,
        @Part("symptom_animal_bite") symAnimalBite: RequestBody,
        @Part("symptom_burn_blister") symBurnBlister: RequestBody,
        @Part("symptom_burn_charred") symBurnCharred: RequestBody,
        @Part("symptom_bruise_blunt") symBruiseBlunt: RequestBody,
        @Part("symptom_bedsores") symBedsores: RequestBody,
        @Part("symptom_clean_cut") symCleanCut: RequestBody,
        @Part("symptom_itch") symItch: RequestBody,
        @Part("symptom_wheal_bumps") symBumps: RequestBody,
        @Part("symptom_night_itch") symNight: RequestBody,
        @Part("symptom_ring_circle") symRing: RequestBody,
        @Part("symptom_dry_scaly") symDry: RequestBody,
        @Part("symptom_vesicles_blister") symBlister: RequestBody,
        @Part("symptom_nail_ingrown") symNailIngrown: RequestBody,
        @Part("symptom_nail_fungus") symNailFungus: RequestBody,
        @Part("symptom_nail_trauma") symNailTrauma: RequestBody,
        @Part("symptom_scalp_dandruff") symScalpDandruff: RequestBody,
        @Part("symptom_hair_loss_patch") symHairLossPatch: RequestBody,
        @Part("symptom_head_lice") symHeadLice: RequestBody,
        @Part("gemini_api_key") geminiApiKey: RequestBody? = null
    ): TriageResponse

    @POST("api/v1/triage/consult-chat")
    suspend fun sendConsultChat(
        @Body request: ConsultChatRequest
    ): ConsultChatResponse

    @Multipart
    @POST("api/v1/triage/track-progress")
    suspend fun trackWoundProgress(
        @Part fileDay1: MultipartBody.Part,
        @Part fileDay2: MultipartBody.Part
    ): WoundProgressResponse

    companion object {
        // IP 10.0.2.2 adalah host computer dari Android Emulator.
        // Jika menggunakan perangkat HP fisik via WiFi lokal, ubah ke IP komputer (misal http://192.168.1.X:8000/)
        var BASE_URL = "http://10.0.2.2:8000/"

        fun create(baseUrl: String = BASE_URL): TriageApiService {
            val logging = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }

            val client = OkHttpClient.Builder()
                .addInterceptor(logging)
                .connectTimeout(45, TimeUnit.SECONDS)
                .readTimeout(45, TimeUnit.SECONDS)
                .build()

            return Retrofit.Builder()
                .baseUrl(baseUrl)
                .client(client)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(TriageApiService::class.java)
        }
    }
}
