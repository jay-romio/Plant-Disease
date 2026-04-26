# Android Studio Setup and APK Build Guide
## Plant Disease Recognition App

### Step 1: Open Android Studio Project

#### 1.1 Launch Android Studio
1. Open Android Studio from your desktop or Start Menu
2. If this is your first time, you'll see the welcome screen
3. Click **"Open"** (or **"File" → "Open"** if already in Android Studio)

#### 1.2 Navigate to Project
1. Browse to: `d:\pyproject\Crop_Project\android_app`
2. Select the `android_app` folder
3. Click **"OK"**

#### 1.3 Wait for Gradle Sync
- Android Studio will automatically sync the project
- This may take 2-5 minutes on first run
- Wait for the sync to complete (bottom progress bar)

---

### Step 2: Configure Android Studio Settings

#### 2.1 Check SDK Installation
1. Go to **"File" → "Settings"** (Windows) or **"Android Studio" → "Preferences"** (Mac)
2. Navigate to **"Appearance & Behavior" → "System Settings" → "Android SDK"**
3. Ensure you have:
   - **Android SDK Platform-Tools**: Latest version
   - **Android SDK Build-Tools**: 33.0.0 or higher
   - **Android 13 (API level 33)**: Installed

#### 2.2 Install Missing Components (if needed)
1. In SDK Manager, click **"SDK Tools"** tab
2. Check and install:
   - ✅ Android SDK Build-Tools
   - ✅ Android SDK Platform-Tools
   - ✅ Android SDK Command-line Tools
3. Click **"Apply"** and wait for installation

#### 2.3 Verify Project Structure
Your project should show this structure in the Project panel:
```
android_app/
├── app/
│   ├── java/
│   │   └── com.digitalkhopdi.plantdisease/
│   │       └── MainActivity.java
│   ├── res/
│   │   ├── layout/
│   │   │   └── activity_main.xml
│   │   └── values/
│   │       └── strings.xml
│   └── build.gradle
├── build.gradle
├── gradle.properties
└── settings.gradle
```

---

### Step 3: Fix Common Configuration Issues

#### 3.1 Update Gradle Version (if needed)
If you see Gradle sync errors:

1. Open **`android_app/build.gradle`** (project level)
2. Update the dependencies section:
```gradle
dependencies {
    classpath 'com.android.tools.build:gradle:7.4.2'
}
```

3. Open **`android_app/gradle/wrapper/gradle-wrapper.properties`**
4. Update distribution URL:
```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-7.5.1-all.zip
```

#### 3.2 Fix Build Configuration
Open **`android_app/app/build.gradle`** and ensure:

```gradle
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

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}
```

#### 3.3 Sync Project
1. Click **"Sync Now"** if you see a sync notification
2. Or go to **"File" → "Sync Project with Gradle Files"**
3. Wait for sync to complete

---

### Step 4: Build Debug APK

#### 4.1 Connect Android Device
1. Enable Developer Options on your Android device:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings > Developer Options
   - Enable "USB Debugging"

2. Connect device via USB
3. Allow USB debugging when prompted

#### 4.2 Build and Run Debug APK
1. Select your device from the dropdown menu (top toolbar)
2. Click the **"Run 'app'"** button (green play icon)
3. Wait for build and installation

#### 4.3 Build APK Without Running
1. Go to **"Build" → "Build Bundle(s) / APK(s)" → "Build APK(s)"**
2. Select **"debug"** variant
3. Wait for build to complete
4. APK will be located at: `android_app/app/build/outputs/apk/debug/app-debug.apk`

---

### Step 5: Build Release APK

#### 5.1 Generate Signed APK
1. Go to **"Build" → "Generate Signed Bundle / APKs"**
2. Select **"APK"** and click **"Next"**
3. Click **"Create new..."** to create a keystore

#### 5.2 Create Keystore
Fill in the keystore information:
- **Key store path**: Choose a location (e.g., `d:\my-release-key.keystore`)
- **Password**: Create a strong password (remember it!)
- **Alias**: `plant-disease-key`
- **Key password**: Same as store password
- **Validity (years)**: 25
- **Certificate**:
  - Name: Your Name
  - Organizational Unit: Development
  - Organization: Your Organization
  - City or Locality: Your City
  - State or Province: Your State
  - Country Code: IN (for India)

#### 5.3 Complete Build
1. Click **"OK"** to create keystore
2. Select **"release"** build variant
3. Click **"Finish"**
4. Wait for build to complete

#### 5.4 Find Release APK
Release APK will be at: `android_app/app/build/outputs/apk/release/app-release.apk`

---

### Step 6: Troubleshooting Common Issues

#### 6.1 Gradle Sync Failed
**Solution:**
1. Check internet connection
2. Update Gradle version (see Step 3.1)
3. Clear Gradle cache: **"File" → "Invalidate Caches / Restart"**

#### 6.2 SDK Not Found
**Solution:**
1. Go to **"Tools" → "SDK Manager"**
2. Install missing SDK components
3. Restart Android Studio

#### 6.3 Build Failed
**Solution:**
1. Check **"Build" → "Rebuild Project"**
2. Check error messages in **"Build" → "Build Output"**
3. Verify all dependencies in build.gradle files

#### 6.4 Device Not Detected
**Solution:**
1. Enable USB debugging on device
2. Install device drivers
3. Try different USB cable
4. Restart Android Studio and device

---

### Step 7: Test the App

#### 7.1 Run on Device
1. Make sure your Flask app is running: `python mobile_app.py`
2. Connect Android device via USB
3. Click **"Run 'app'"** button
4. Test all features:
   - App loads correctly
   - Can select images
   - Hindi text displays
   - Back button works

#### 7.2 Install APK Manually
1. Copy APK file to device
2. Enable "Install from unknown sources" in device settings
3. Open APK file and install
4. Test app functionality

---

### Step 8: Quick Reference Commands

#### Build Debug APK:
```bash
cd d:\pyproject\Crop_Project\android_app
.\gradlew assembleDebug
```

#### Build Release APK:
```bash
cd d:\pyproject\Crop_Project\android_app
.\gradlew assembleRelease
```

#### Clean Project:
```bash
.\gradlew clean
```

---

### Step 9: Final Checklist

Before building your final APK, ensure:

- [ ] Flask app is running on `http://10.17.8.184:5000`
- [ ] MainActivity.java has correct IP address
- [ ] All permissions are in AndroidManifest.xml
- [ ] Build completes without errors
- [ ] App works on device/emulator
- [ ] Hindi text displays correctly
- [ ] Image upload and analysis work

---

### Step 10: Production Deployment

#### For Google Play Store:
1. Generate signed APK (Step 5)
2. Create Google Play Console account
3. Upload APK and fill store listing
4. Submit for review

#### For Direct Distribution:
1. Share the release APK file
2. Users enable "Unknown Sources"
3. Install APK directly

---

## Important Notes

1. **IP Address**: Your MainActivity.java already has `http://10.17.8.184:5000` - ensure this matches your Flask server
2. **Flask Server**: Must be running when testing the app
3. **Network**: Device and computer must be on same WiFi network
4. **Permissions**: App requires internet and storage permissions
5. **Hindi Support**: Ensure device has Hindi font support

Your Android app is now ready for building and testing!
