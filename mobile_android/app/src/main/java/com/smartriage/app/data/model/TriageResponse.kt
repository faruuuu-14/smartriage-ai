package com.smartriage.app.data.model

import com.google.gson.annotations.SerializedName

data class TissueAnalysis(
    @SerializedName("granulation_percentage") val granulationPercentage: Float,
    @SerializedName("slough_percentage") val sloughPercentage: Float,
    @SerializedName("necrotic_percentage") val necroticPercentage: Float,
    @SerializedName("estimated_area_cm2") val estimatedAreaCm2: Float,
    @SerializedName("severity_classification") val severityClassification: String
)

data class TriageResponse(
    @SerializedName("success") val success: Boolean,
    @SerializedName("condition_key") val conditionKey: String,
    @SerializedName("common_name") val commonName: String,
    @SerializedName("medical_name") val medicalName: String,
    @SerializedName("confidence") val confidence: Float,
    @SerializedName("confidence_percentage") val confidencePercentage: String,
    @SerializedName("triage_level") val triageLevel: String,
    @SerializedName("triage_color") val triageColor: String,
    @SerializedName("triage_action") val triageAction: String,
    @SerializedName("triage_reasons") val triageReasons: List<String>,
    @SerializedName("tissue_analysis") val tissueAnalysis: TissueAnalysis,
    @SerializedName("pain_level") val painLevel: Int,
    @SerializedName("description") val description: String,
    @SerializedName("first_aid_steps") val firstAidSteps: List<String>,
    @SerializedName("recommended_otc_meds") val recommendedOtcMeds: List<String>,
    @SerializedName("myths_and_warnings") val mythsAndWarnings: List<String>,
    @SerializedName("estimated_healing_time") val estimatedHealingTime: String,
    @SerializedName("red_flags") val redFlags: List<String>,
    @SerializedName("heatmap_url") val heatmapUrl: String?,
    @SerializedName("heatmap_base64") val heatmapBase64: String?
)
