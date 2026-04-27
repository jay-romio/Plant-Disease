# WebView Android App Deployment - Step by Step Guide
## Plant Disease Recognition System

### Overview
This guide will walk you through creating an Android app that wraps your Flask Plant Disease Recognition web application using WebView. This is the fastest way to deploy your app to Android devices.

---

## Step 1: Prepare Mobile-Optimized Flask App

### 1.1 Create Mobile Flask Application

Create a new file `mobile_app.py` in your project root:

```python
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify
import numpy as np
import json
import uuid
import tensorflow as tf
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Load model and data
model = tf.keras.models.load_model("models/plant_disease_recog_model_pwp.keras")
label = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
         'Background_without_leaves', 'Blueberry___healthy', 'Cherry___Powdery_mildew', 'Cherry___healthy',
         'Corn___Cercospora_leaf_spot Gray_leaf_spot', 'Corn___Common_rust', 'Corn___Northern_Leaf_Blight',
         'Corn___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
         'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
         'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
         'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
         'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
         'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
         'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
         'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

# Load disease data
with open("plant_disease.json", 'r', encoding='utf-8') as file:
    plant_disease = json.load(file)

with open("plant_disease_hindi.json", 'r', encoding='utf-8') as file:
    plant_disease_hindi = json.load(file)

# Mobile-optimized routes
@app.route('/')
def home():
    return render_template('mobile_home.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint for mobile app"""
    return jsonify({"status": "healthy", "model_loaded": True})

@app.route('/api/uploadimages/<path:filename>')
def uploaded_images(filename):
    return send_from_directory('./uploadimages', filename)

@app.route('/api/predict', methods=['POST'])
def predict_disease():
    """API endpoint for mobile app predictions"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image = request.files['image']
        if image.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Save temporary file
        temp_name = f"uploadimages/temp_{uuid.uuid4().hex}_{image.filename}"
        image.save(temp_name)
        
        # Make prediction
        prediction = model_predict(temp_name)
        
        # Clean up
        os.remove(temp_name)
        
        return jsonify({
            "success": True,
            "prediction": prediction
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_features(image):
    """Extract features from image"""
    image = tf.keras.utils.load_img(image, target_size=(160, 160))
    feature = tf.keras.utils.img_to_array(image)
    feature = np.array([feature])
    return feature

def model_predict(image):
    """Make prediction using the model"""
    img = extract_features(image)
    prediction = model.predict(img)
    prediction_label = plant_disease[prediction.argmax()]
    prediction_label_hindi = plant_disease_hindi[prediction.argmax()]
    
    detailed_result = {
        'name': prediction_label['name'],
        'name_hindi': prediction_label_hindi['name_hindi'],
        'cause': prediction_label['cause'],
        'cause_hindi': prediction_label_hindi['cause_hindi'],
        'cure': prediction_label['cure'],
        'cure_hindi': prediction_label_hindi['cure_hindi'],
        'symptoms': prediction_label_hindi['symptoms'],
        'symptoms_hindi': prediction_label_hindi['symptoms_hindi'],
        'prevention': prediction_label_hindi['prevention'],
        'prevention_hindi': prediction_label_hindi['prevention_hindi'],
        'severity': prediction_label_hindi['severity'],
        'severity_hindi': prediction_label_hindi['severity_hindi'],
        'confidence': float(prediction.max() * 100)
    }
    
    return detailed_result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 1.2 Create Mobile-Optimized HTML Template

Create `templates/mobile_home.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plant Disease Recognition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
    <style>
        .mobile-container {
            max-width: 100%;
            padding: 0;
            margin: 0;
        }
        .upload-area {
            border: 3px dashed #007bff;
            border-radius: 15px;
            padding: 40px 20px;
            text-align: center;
            background: #f8f9fa;
            margin: 20px;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            background: #e9ecef;
            border-color: #0056b3;
        }
        .upload-icon {
            font-size: 3rem;
            color: #007bff;
            margin-bottom: 15px;
        }
        .result-card {
            margin: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .disease-name {
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            padding: 15px;
            border-radius: 15px 15px 0 0;
            text-align: center;
        }
        .hindi-text {
            font-family: 'Mangal', 'Devanagari Sans', sans-serif;
            color: #495057;
            font-weight: 500;
            margin-top: 8px;
            font-size: 1.05rem;
            line-height: 1.7;
        }
        .confidence-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            margin: 5px;
        }
        .info-section {
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #007bff;
        }
        .loading-spinner {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .preview-image {
            max-width: 100%;
            max-height: 300px;
            border-radius: 10px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="mobile-container">
        <!-- Header -->
        <div class="bg-primary text-white p-3">
            <h1 class="text-center mb-0">Plant Disease Recognition</h1>
            <p class="text-center mb-0">Identify plant diseases instantly with AI</p>
        </div>

        <!-- Upload Section -->
        <div class="container-fluid p-3">
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">+ Upload Image</div>
                <h4>Tap to select plant image</h4>
                <p class="text-muted">Choose from gallery or take a photo</p>
                <input type="file" id="fileInput" accept="image/*" style="display: none;">
            </div>

            <!-- Image Preview -->
            <div id="imagePreview" style="display: none;">
                <img id="previewImg" class="preview-image mx-auto d-block" alt="Preview">
                <button onclick="analyzeImage()" class="btn btn-success btn-lg w-100 mt-3">
                    Analyze Disease
                </button>
            </div>

            <!-- Loading Spinner -->
            <div class="loading-spinner" id="loadingSpinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Analyzing...</span>
                </div>
                <p class="mt-2">Analyzing plant disease...</p>
            </div>

            <!-- Results Section -->
            <div id="results" style="display: none;">
                <div class="result-card">
                    <div class="disease-name">
                        <h3 id="diseaseName"></h3>
                        <h4 class="hindi-text" id="diseaseNameHindi"></h4>
                    </div>
                    
                    <div class="card-body">
                        <div class="text-center mb-3">
                            <span class="confidence-badge bg-info" id="confidenceBadge"></span>
                            <span class="confidence-badge" id="severityBadge"></span>
                        </div>

                        <div class="info-section">
                            <h5>Cause / kaaran:</h5>
                            <p id="cause"></p>
                            <p class="hindi-text" id="causeHindi"></p>
                        </div>

                        <div class="info-section">
                            <h5>Symptoms / lakshan:</h5>
                            <p id="symptoms"></p>
                            <p class="hindi-text" id="symptomsHindi"></p>
                        </div>

                        <div class="info-section">
                            <h5>Treatment / ilaaj:</h5>
                            <p id="cure"></p>
                            <p class="hindi-text" id="cureHindi"></p>
                        </div>

                        <div class="info-section">
                            <h5>Prevention / rokaav:</h5>
                            <p id="prevention"></p>
                            <p class="hindi-text" id="preventionHindi"></p>
                        </div>
                    </div>
                </div>

                <button onclick="resetApp()" class="btn btn-secondary btn-lg w-100 mt-3">
                    Analyze Another Image
                </button>
            </div>
        </div>
    </div>

    <script>
        let selectedFile = null;

        // File input handler
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                selectedFile = file;
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    document.getElementById('previewImg').src = e.target.result;
                    document.getElementById('imagePreview').style.display = 'block';
                };
                
                reader.readAsDataURL(file);
            }
        });

        // Analyze image
        function analyzeImage() {
            if (!selectedFile) {
                alert('Please select an image first');
                return;
            }

            // Show loading
            document.getElementById('loadingSpinner').style.display = 'block';
            document.getElementById('imagePreview').style.display = 'none';
            document.getElementById('results').style.display = 'none';

            // Create form data
            const formData = new FormData();
            formData.append('image', selectedFile);

            // Send to server
            fetch('/api/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displayResults(data.prediction);
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error analyzing image. Please try again.');
            })
            .finally(() => {
                document.getElementById('loadingSpinner').style.display = 'none';
            });
        }

        // Display results
        function displayResults(prediction) {
            document.getElementById('diseaseName').textContent = prediction.name;
            document.getElementById('diseaseNameHindi').textContent = prediction.name_hindi;
            document.getElementById('confidenceBadge').textContent = `Confidence: ${prediction.confidence.toFixed(1)}%`;
            
            // Set severity badge
            const severityBadge = document.getElementById('severityBadge');
            severityBadge.textContent = `Severity: ${prediction.severity} / ${prediction.severity_hindi}`;
            severityBadge.className = 'confidence-badge';
            
            if (prediction.severity === 'Severe') {
                severityBadge.classList.add('bg-danger');
            } else if (prediction.severity === 'Moderate') {
                severityBadge.classList.add('bg-warning');
            } else {
                severityBadge.classList.add('bg-success');
            }

            document.getElementById('cause').textContent = prediction.cause;
            document.getElementById('causeHindi').textContent = prediction.cause_hindi;
            document.getElementById('symptoms').textContent = prediction.symptoms;
            document.getElementById('symptomsHindi').textContent = prediction.symptoms_hindi;
            document.getElementById('cure').textContent = prediction.cure;
            document.getElementById('cureHindi').textContent = prediction.cure_hindi;
            document.getElementById('prevention').textContent = prediction.prevention;
            document.getElementById('preventionHindi').textContent = prediction.prevention_hindi;

            document.getElementById('results').style.display = 'block';
        }

        // Reset app
        function resetApp() {
            document.getElementById('fileInput').value = '';
            document.getElementById('imagePreview').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            selectedFile = null;
        }
    </script>
</body>
</html>
```

### 1.3 Update Dependencies

Add Flask-CORS to your requirements.txt:
```bash
pip install flask-cors
```

---

## Step 2: Test Mobile Flask App

### 2.1 Run the Mobile App

```bash
cd d:\pyproject\Crop_Project
python mobile_app.py
```

### 2.2 Find Your IP Address

Open Command Prompt and run:
```bash
ipconfig
```

Look for "IPv4 Address" (usually starts with 192.168.x.x or 10.x.x.x)

### 2.3 Test in Browser

Open browser and navigate to: `http://YOUR_IP:5000`

---

## Step 3: Create Android Studio Project

### 3.1 Install Android Studio

Download and install Android Studio from: https://developer.android.com/studio

### 3.2 Create New Project

1. Open Android Studio
2. Click "New Project"
3. Select "Empty Views Activity"
4. Configure project:
   - Name: `PlantDiseaseRecognition`
   - Package name: `com.digitalkhopdi.plantdisease`
   - Language: `Java`
   - Minimum SDK: `API 21: Android 5.0 (Lollipop)`
   - Build configuration language: `Groovy`

5. Click "Finish"

---

## Step 4: Configure Android WebView

### 4.1 Update build.gradle (app level)

Open `app/build.gradle` and replace contents:

```gradle
apply plugin: 'com.android.application'

android {
    compileSdkVersion 33
    buildToolsVersion "33.0.0"

    defaultConfig {
        applicationId "com.digitalkhopdi.plantdisease"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'com.google.android.material:material:1.9.0'
}
```

### 4.2 Update AndroidManifest.xml

Open `app/src/main/AndroidManifest.xml` and replace contents:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.digitalkhopdi.plantdisease">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.CAMERA" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
```

### 4.3 Update MainActivity.java

Open `app/src/main/java/com/digitalkhopdi/plantdisease/MainActivity.java` and replace contents:

```java
package com.digitalkhopdi.plantdisease;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_CODE_GALLERY = 1;
    private static final int REQUEST_CODE_CAMERA = 2;
    private static final int PERMISSION_REQUEST_CODE = 3;
    private WebView webView;
    private ProgressBar progressBar;
    private ValueCallback<Uri[]> uploadMessage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webview);
        progressBar = findViewById(R.id.progressBar);

        setupWebView();
        checkPermissions();
    }

    private void setupWebView() {
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        
        // Enable file upload from web
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowFileAccessFromFileURLs(true);
        webSettings.setAllowUniversalAccessFromFileURLs(true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                progressBar.setVisibility(View.GONE);
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return false;
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
                uploadMessage = filePathCallback;
                openFileChooser();
                return true;
            }
        });

        // IMPORTANT: Replace with your actual IP address
        webView.loadUrl("http://YOUR_IP_ADDRESS:5000");
    }

    private void openFileChooser() {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("image/*");
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(Intent.createChooser(intent, "Select Image"), REQUEST_CODE_GALLERY);
    }

    private void checkPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) 
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, 
                        new String[]{Manifest.permission.READ_EXTERNAL_STORAGE},
                        PERMISSION_REQUEST_CODE);
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permission granted", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        
        if (requestCode == REQUEST_CODE_GALLERY && resultCode == RESULT_OK) {
            if (uploadMessage != null) {
                Uri[] results = new Uri[]{data.getData()};
                uploadMessage.onReceiveValue(results);
                uploadMessage = null;
            }
        }
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
```

### 4.4 Update activity_main.xml

Open `app/src/main/res/layout/activity_main.xml` and replace contents:

```xml
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ProgressBar
        android:id="@+id/progressBar"
        style="?android:attr/progressBarStyle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_centerInParent="true" />

    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:visibility="visible" />

</RelativeLayout>
```

---

## Step 5: Update Your IP Address

### 5.1 Find Your IP Address

Run in Command Prompt:
```bash
ipconfig
```

Look for "IPv4 Address" (e.g., 192.168.1.100)

### 5.2 Update MainActivity.java

In MainActivity.java, find this line:
```java
webView.loadUrl("http://YOUR_IP_ADDRESS:5000");
```

Replace `YOUR_IP_ADDRESS` with your actual IP address:
```java
webView.loadUrl("http://192.168.1.100:5000");
```

---

## Step 6: Test the Android App

### 6.1 Set Up Android Device

1. Enable Developer Options on your Android device:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings > Developer Options
   - Enable "USB Debugging"

2. Connect your device to computer via USB

### 6.2 Run the App

1. Make sure your Flask app is running: `python mobile_app.py`
2. In Android Studio, click the green "Run" button
3. Select your connected device
4. Wait for app to install and launch

### 6.3 Test Features

- [ ] App loads correctly
- [ ] Can tap to select image
- [ ] Image preview works
- [ ] Analysis button works
- [ ] Results display correctly
- [ ] Hindi text shows properly
- [ ] Back button works

---

## Step 7: Build Release APK

### 7.1 Generate Signed APK

1. In Android Studio: Build > Generate Signed Bundle/APK
2. Select "APK"
3. Click "Create new..." for keystore
4. Fill in keystore information:
   - Key store path: Choose location
   - Password: Create password
   - Alias: Your app alias
   - Key password: Same as store password
   - Validity: 25 years
   - Certificate: Fill in your details

5. Click "Next"
6. Select "release" build variant
7. Click "Finish"

### 7.2 Find Your APK

The APK will be located at:
`app/release/app-release.apk`

---

## Step 8: Deploy to Google Play Store (Optional)

### 8.1 Prepare Store Listing

1. Create app icon (512x512 pixels)
2. Take screenshots of your app
3. Write app description
4. Create privacy policy (simple text file)

### 8.2 Upload to Google Play

1. Go to Google Play Console
2. Create new application
3. Fill in store listing
4. Upload your APK
5. Complete content rating questionnaire
6. Submit for review

---

## Troubleshooting

### Common Issues:

**App shows blank screen:**
- Check that Flask app is running
- Verify IP address is correct
- Ensure both devices are on same WiFi network

**Image upload not working:**
- Check permissions are granted
- Verify file chooser implementation
- Check CORS settings in Flask

**Hindi text not displaying:**
- Ensure Mangal font is available
- Check CSS font-family settings
- Verify UTF-8 encoding

**Connection refused:**
- Make sure Flask app runs on `0.0.0.0:5000`
- Check firewall settings
- Verify network connectivity

---

## Production Deployment

### Option 1: Cloud Server
- Deploy Flask to Heroku, PythonAnywhere, or AWS
- Update Android URL to cloud server
- No need for local server

### Option 2: VPS Hosting
- Rent a VPS (DigitalOcean, Vultr)
- Install Flask and configure
- Point Android app to VPS IP

### Option 3: Firebase Hosting
- Use Firebase Functions for backend
- Deploy Flask as serverless function
- Use Firebase domain in Android app

---

## Summary

You now have a complete Android app that:
- Wraps your Flask web application
- Supports image upload and analysis
- Displays bilingual results (English + Hindi)
- Works on Android 5.0 and above
- Can be published to Google Play Store

The WebView approach gives you the fastest deployment time while preserving all your existing functionality!
