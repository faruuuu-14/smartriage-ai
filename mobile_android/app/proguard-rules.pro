# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in C:\Users\fatur\AppData\Local\Android\Sdk/tools/proguard/proguard-android.txt
# You can edit the include path and order by changing the proguardFiles
# directive in build.gradle.

# Keep Retrofit and Gson models
-keepattributes Signature
-keepattributes *Annotation*
-keep class com.smartriage.app.data.model.** { *; }
