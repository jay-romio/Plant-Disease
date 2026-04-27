# Google Cloud Deployment - Complete Step-by-Step Guide
## Plant Disease Recognition App

### Overview
This guide will walk you through deploying your Plant Disease Recognition Flask app to Google Cloud Platform using the browser interface for maximum reliability.

---

## 🚀 Step 1: Setup Google Cloud Project

### 1.1 Open Google Cloud Console
1. Go to: https://console.cloud.google.com
2. Sign in with your Google account (jayanandsidar27@gmail.com)
3. Click the project dropdown at the top

### 1.2 Create New Project
1. Click **"NEW PROJECT"**
2. **Project name**: `plant-disease-app`
3. **Organization**: Keep default
4. **Location**: Keep default
5. Click **"CREATE"**

### 1.3 Verify Project Selection
- Make sure your new project is selected in the dropdown
- Note your **Project ID** and **Project Number** for later

---

## 🔧 Step 2: Enable Required APIs

### 2.1 Navigate to API Library
1. Click navigation menu (☰) → **"APIs & Services"** → **"Library"**

### 2.2 Enable These APIs (One by One):

#### Cloud Build API
1. Search: "Cloud Build API"
2. Click on the result
3. Click **"ENABLE"**

#### Cloud Run API
1. Search: "Cloud Run API"
2. Click on the result
3. Click **"ENABLE"**

#### Cloud Storage API
1. Search: "Cloud Storage API"
2. Click on the result
3. Click **"ENABLE"**

#### Artifact Registry API
1. Search: "Artifact Registry API"
2. Click on the result
3. Click **"ENABLE"**

### 2.3 Verify APIs Enabled
1. Go to **"APIs & Services"** → **"Dashboard"**
2. All 4 APIs should appear as "Enabled"

---

## 📦 Step 3: Create Cloud Storage Bucket

### 3.1 Navigate to Cloud Storage
1. Navigation menu (☰) → **"Storage"** → **"Browser"**
2. Click **"CREATE BUCKET"**

### 3.2 Configure Bucket
1. **Name**: `plant-disease-models-unique-id` (must be globally unique)
   - Add timestamp for uniqueness: `plant-disease-models-1714160000`
2. **Location type**: Choose **"Region"**
3. **Location**: Select **"us-central1"**
4. **Storage class**: Choose **"Standard"**
5. **Control access**: Choose **"Uniform"**
6. Click **"CREATE"**

### 3.3 Upload Model Files
1. Click on your bucket name to open it
2. Click **"UPLOAD FILES"**
3. Upload these files from your project:
   - `models/plant_disease_recog_model_pwp.keras`
   - `plant_disease.json`
   - `plant_disease_hindi.json`

### 3.4 Create Folder Structure (Optional but Recommended)
1. Click **"CREATE FOLDER"** → Name it `models`
2. Open the models folder
3. Upload the `.keras` file into this folder
4. Upload JSON files to the root of the bucket

---

## 🔐 Step 4: Configure IAM Permissions

### 4.1 Navigate to IAM
1. Navigation menu (☰) → **"IAM & Admin"** → **"IAM"**
2. You'll see the current permissions list

### 4.2 Get Your Project Number
1. Navigation menu (☰) → **"IAM & Admin"** → **"Settings"**
2. Look for **"Project number"** (e.g., 130924525337)
3. Copy this number for the next steps

### 4.3 Add Cloud Build Service Account Permissions
1. Click **"GRANT ACCESS"** button at the top
2. **New principals**: Type: `PROJECT_NUMBER@cloudbuild.gserviceaccount.com`
   - Replace PROJECT_NUMBER with your actual number
   - Example: `130924525337@cloudbuild.gserviceaccount.com`
3. **Select a role**: Search and select **"Storage Object Viewer"**
4. Click **"SAVE"**

### 4.4 Add Artifact Registry Permissions
1. Click **"GRANT ACCESS"** again
2. **New principals**: Same service account (`PROJECT_NUMBER@cloudbuild.gserviceaccount.com`)
3. **Select a role**: Search and select **"Artifact Registry Writer"**
4. Click **"SAVE"**

### 4.5 Add Compute Service Account Permissions
1. Click **"GRANT ACCESS"** again
2. **New principals**: Type: `PROJECT_NUMBER-compute@developer.gserviceaccount.com`
3. **Select a role**: Search and select **"Storage Object Viewer"**
4. Click **"SAVE"**

---

## 🏗️ Step 5: Build Container with Cloud Build

### 5.1 Navigate to Cloud Build
1. Navigation menu (☰) → **"Cloud Build"**
2. Click **"Triggers"** tab

### 5.2 Create Build Trigger
1. Click **"CREATE TRIGGER"**
2. **Name**: `deploy-plant-disease-app`
3. **Region**: Select `us-central1`
4. **Repository**: Choose **"Cloud Storage"**
5. **Connection**: Click **"CREATE CONNECTION"** if needed
   - **Connection name**: `plant-disease-connection`
   - Click **"CREATE"**
6. **Bucket**: Select your storage bucket
7. **Build configuration**: Choose **"Dockerfile"**
8. **Dockerfile directory**: Type `/` (root directory)
9. Click **"CREATE"**

### 5.3 Run Build Manually
1. Go to **"Cloud Build"** → **"History"** tab
2. Click **"MANUAL RUN"**
3. Select your trigger: `deploy-plant-disease-app`
4. Click **"RUN"**

### 5.4 Monitor Build Progress
- Watch the build progress in real-time
- Build should take 5-10 minutes
- Look for green "SUCCESS" status

---

## 🚀 Step 6: Deploy to Cloud Run

### 6.1 Navigate to Cloud Run
1. Navigation menu (☰) → **"Cloud Run"**
2. Click **"CREATE SERVICE"**

### 6.2 Configure Cloud Run Service
1. **Service name**: `plant-disease-app`
2. **Region**: Select `us-central1`
3. **Platform**: Choose **"Managed"**
4. **Authentication**: Select **"Allow unauthenticated"**
5. **Container image**: 
   - Click **"SELECT"**
   - Choose your recently built image
   - Click **"SELECT"**

### 6.3 Configure Resources
1. **Memory allocation**: Choose **"2 GiB"**
2. **CPU allocation**: Choose **"1 CPU"**
3. **Maximum requests per instance**: Keep default
4. **Timeout**: Set to **"300 seconds"**

### 6.4 Configure Environment Variables
1. Click **"VARIABLES"** tab
2. Click **"ADD VARIABLE"**
3. **Name**: `MODEL_BUCKET`
4. **Value**: Your bucket name (e.g., `plant-disease-models-1714160000`)
5. Click **"DONE"**

### 6.5 Create Service
1. Click **"CREATE"** at the bottom
2. Wait for deployment to complete (2-3 minutes)

---

## ✅ Step 7: Test Your Deployment

### 7.1 Get Your Service URL
After deployment completes, you'll see:
- **Service URL**: `https://plant-disease-app-xxxxxxxxx-uc.a.run.app`
- **Copy this URL** - you'll need it for your Android app

### 7.2 Test Health Endpoint
1. Open your browser
2. Go to: `https://your-service-url.run.app/api/health`
3. Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "disease_data_loaded": true,
  "cloud_storage_connected": true
}
```

### 7.3 Test Web Interface
1. Go to: `https://your-service-url.run.app`
2. Verify the mobile interface loads
3. Try uploading a test image

### 7.4 Check Logs (if needed)
1. Go to **"Cloud Run"** → Click on your service
2. Click **"LOGS"** tab
3. Check for any errors

---

## 📱 Step 8: Update Android App

### 8.1 Open Android Studio
1. Open your Android project
2. Navigate to `android_app/app/src/main/java/com/digitalkhopdi/plantdisease/MainActivity.java`

### 8.2 Update Service URL
Find this line:
```java
webView.loadUrl("http://10.17.8.184:5000");
```

Replace with your Cloud Run URL:
```java
webView.loadUrl("https://plant-disease-app-xxxxxxxxx-uc.a.run.app");
```

### 8.3 Build New APK
1. In Android Studio: **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
2. Wait for build to complete
3. Install the new APK on your device

### 8.4 Test Android App
1. Open the app on your device
2. Test image upload and analysis
3. Verify Hindi text displays correctly
4. Test back button functionality

---

## 🎯 Success Checklist

### ✅ Deployment Success Indicators:
- [ ] Cloud Build completed successfully
- [ ] Cloud Run service is running
- [ ] Health endpoint returns positive status
- [ ] Web interface loads properly
- [ ] Android app connects and works
- [ ] No critical errors in logs

### ✅ Expected Results:
- **Service URL**: `https://plant-disease-app-xxxxxxxxx-uc.a.run.app`
- **Health Response**: All values `true`
- **Web Interface**: Mobile-friendly UI loads
- **Android App**: Full functionality working

---

## 🔧 Troubleshooting Guide

### Common Issues and Solutions:

#### Issue 1: Build Fails
**Symptoms**: Cloud Build shows red error status
**Solutions**:
1. Check Dockerfile syntax
2. Verify all files are uploaded to Cloud Storage
3. Check build logs for specific errors

#### Issue 2: Service Not Starting
**Symptoms**: Cloud Run service shows error or crashes
**Solutions**:
1. Check memory allocation (increase to 4GiB if needed)
2. Verify environment variables are correct
3. Check service logs for startup errors

#### Issue 3: Model Loading Fails
**Symptoms**: Health check shows `"model_loaded": false`
**Solutions**:
1. Verify model file is in Cloud Storage
2. Check bucket name in environment variables
3. Ensure model file path is correct

#### Issue 4: Permission Errors
**Symptoms**: 403 permission denied errors
**Solutions**:
1. Verify IAM permissions are set correctly
2. Check service account names
3. Ensure APIs are enabled

#### Issue 5: Android App Not Connecting
**Symptoms**: App shows connection errors
**Solutions**:
1. Verify URL is correct in MainActivity.java
2. Check if Cloud Run service is running
3. Test URL in browser first

---

## 💰 Cost Management

### Free Tier Limits (Monthly):
- **Cloud Run**: 2 million requests
- **Cloud Storage**: 5 GB standard storage
- **Cloud Build**: 120 build minutes
- **Artifact Registry**: 50 GB-month storage

### Cost Optimization Tips:
1. Use minimum required memory (2GiB should be sufficient)
2. Set appropriate request concurrency
3. Monitor usage in Google Cloud Console
4. Delete unused resources

---

## 🎉 Congratulations!

Your Plant Disease Recognition app is now running on Google Cloud Platform with:

- **24/7 Availability**: No local server needed
- **Global Access**: Available from anywhere
- **Automatic Scaling**: Handles multiple users
- **Professional Infrastructure**: 99.9% uptime SLA
- **Secure HTTPS**: SSL certificates included

### What You've Accomplished:
✅ Deployed Flask app to Google Cloud  
✅ Configured Cloud Storage for model files  
✅ Set up Cloud Run for serverless deployment  
✅ Updated Android app with cloud URL  
✅ Created production-ready application  

### Next Steps:
1. Monitor your app usage in Google Cloud Console
2. Set up alerts for high error rates
3. Consider adding custom domain
4. Share your app with users!

---

## 📞 Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Review Cloud Build and Cloud Run logs
3. Verify all configurations match this guide
4. Use the Google Cloud Console for visual debugging

Your Plant Disease Recognition app is now live on Google Cloud! 🚀
