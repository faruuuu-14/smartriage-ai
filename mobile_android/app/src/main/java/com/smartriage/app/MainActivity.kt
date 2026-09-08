package com.smartriage.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import com.smartriage.app.ui.TriageViewModel
import com.smartriage.app.ui.screens.MainScreen
import com.smartriage.app.ui.theme.SmarTriageTheme

class MainActivity : ComponentActivity() {
    private val viewModel: TriageViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SmarTriageTheme {
                MainScreen(viewModel = viewModel)
            }
        }
    }
}
