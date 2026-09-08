package com.smartriage.app.data.model

import com.google.gson.annotations.SerializedName

data class TissueAnalysis(
    @SerializedName("granulation_percentage") val granulationPercentage: Float = 0f,
    @SerializedName("slough_percentage") val sloughPercentage: Float = 0f,
    @SerializedName("necrotic_percentage") val necroticPercentage: Float = 0f,
    @SerializedName("estimated_area_cm2") val estimatedAreaCm2: Float = 0f,
    @SerializedName("severity_classification") val severityClassification: String = ""
)

data class QualityInfo(
    @SerializedName("is_valid") val isValid: Boolean = true,
    @SerializedName("is_blurry") val isBlurry: Boolean = false,
    @SerializedName("blur_score") val blurScore: Float = 0f,
    @SerializedName("quality_status") val qualityStatus: String = "OPTIMAL",
    @SerializedName("warning_message") val warningMessage: String? = null
)

data class AbcdeAnalysis(
    @SerializedName("has_pigmented_lesion") val hasPigmentedLesion: Boolean = false,
    @SerializedName("asymmetry_score") val asymmetryScore: Float = 0f,
    @SerializedName("border_score") val borderScore: Float = 0f,
    @SerializedName("color_variation_score") val colorVariationScore: Float = 0f,
    @SerializedName("diameter_mm") val diameterMm: Float = 0f,
    @SerializedName("risk_level") val riskLevel: String = "RENDAH",
    @SerializedName("recommendation") val recommendation: String = ""
)

data class Top3DifferentialItem(
    @SerializedName("condition_key") val conditionKey: String = "",
    @SerializedName("common_name") val commonName: String = "",
    @SerializedName("medical_name") val medicalName: String = "",
    @SerializedName("probability") val probability: Float = 0f,
    @SerializedName("percentage") val percentage: String = "0%",
    @SerializedName("clinical_rationale") val clinicalRationale: String = ""
)

data class SafetyWarningItem(
    @SerializedName("title") val title: String = "",
    @SerializedName("warning_message") val warningMessage: String = "",
    @SerializedName("category") val category: String = "KONTRAINDIKASI",
    @SerializedName("severity") val severity: String = "PERINGATAN_SEDANG"
)

data class AdaptiveQuestion(
    @SerializedName("question") val question: String = "",
    @SerializedName("options") val options: List<String> = emptyList()
)

data class TriageResponse(
    @SerializedName("success") val success: Boolean = true,
    @SerializedName("condition_key") val conditionKey: String = "",
    @SerializedName("common_name") val commonName: String = "",
    @SerializedName("medical_name") val medicalName: String = "",
    @SerializedName("confidence") val confidence: Float = 0f,
    @SerializedName("confidence_percentage") val confidencePercentage: String = "0%",
    @SerializedName("triage_level") val triageLevel: String = "HIJAU",
    @SerializedName("triage_color") val triageColor: String = "#10b981",
    @SerializedName("triage_action") val triageAction: String = "",
    @SerializedName("triage_reasons") val triageReasons: List<String> = emptyList(),
    @SerializedName("tissue_analysis") val tissueAnalysis: TissueAnalysis = TissueAnalysis(),
    @SerializedName("quality_info") val qualityInfo: QualityInfo? = null,
    @SerializedName("abcde_analysis") val abcdeAnalysis: AbcdeAnalysis? = null,
    @SerializedName("top3_differential") val top3Differential: List<Top3DifferentialItem>? = null,
    @SerializedName("safety_warnings") val safetyWarnings: List<SafetyWarningItem>? = null,
    @SerializedName("adaptive_questions") val adaptiveQuestions: List<AdaptiveQuestion>? = null,
    @SerializedName("pain_level") val painLevel: Int = 1,
    @SerializedName("description") val description: String = "",
    @SerializedName("first_aid_steps") val firstAidSteps: List<String> = emptyList(),
    @SerializedName("recommended_otc_meds") val recommendedOtcMeds: List<String> = emptyList(),
    @SerializedName("myths_and_warnings") val mythsAndWarnings: List<String> = emptyList(),
    @SerializedName("estimated_healing_time") val estimatedHealingTime: String = "",
    @SerializedName("red_flags") val redFlags: List<String> = emptyList(),
    @SerializedName("heatmap_url") val heatmapUrl: String? = null,
    @SerializedName("heatmap_base64") val heatmapBase64: String? = null
)

data class ConsultChatRequest(
    @SerializedName("condition_key") val conditionKey: String,
    @SerializedName("message") val message: String,
    @SerializedName("patient_group") val patientGroup: String = "DEWASA",
    @SerializedName("gemini_api_key") val geminiApiKey: String? = null
)

data class ConsultChatResponse(
    @SerializedName("success") val success: Boolean = true,
    @SerializedName("reply") val reply: String = "",
    @SerializedName("suggested_questions") val suggestedQuestions: List<String>? = null
)

data class ChatMessage(
    val id: String = java.util.UUID.randomUUID().toString(),
    val text: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis()
)

data class WoundProgressResponse(
    @SerializedName("success") val success: Boolean = true,
    @SerializedName("healing_status") val healingStatus: String = "",
    @SerializedName("healing_badge_color") val healingBadgeColor: String = "#10b981",
    @SerializedName("area_reduction_percentage") val areaReductionPercentage: Float = 0f,
    @SerializedName("day1_area_cm2") val day1AreaCm2: Float = 0f,
    @SerializedName("day2_area_cm2") val day2AreaCm2: Float = 0f,
    @SerializedName("clinical_evaluation") val clinicalEvaluation: String = "",
    @SerializedName("recommendations") val recommendations: List<String> = emptyList()
)
