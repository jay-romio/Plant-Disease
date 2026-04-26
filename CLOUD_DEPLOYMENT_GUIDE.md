# Cloud Deployment Guide
## Plant Disease Recognition App

### Overview
This guide will help you deploy your Flask Plant Disease Recognition app to a cloud server, making it accessible 24/7 without needing to run your local server.

---

## Option 1: Heroku Deployment (Recommended - Free & Easy)

### Step 1: Prepare Flask App for Heroku

#### 1.1 Create Procfile
Create a new file `Procfile` in your project root:

```text
web: gunicorn mobile_app:app
```

#### 1.2 Update Requirements
Create `requirements.txt` with all dependencies:

```text
flask==2.3.3
flask-cors==4.0.0
tensorflow==2.13.0
numpy==1.24.3
Pillow==10.0.0
gunicorn==21.2.0
```

#### 1.3 Create Runtime File
Create `runtime.txt`:

```text
python-3.9.16
```

#### 1.4 Update mobile_app.py for Production
Modify your `mobile_app.py`:

```python
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify
import numpy as np
import json
import uuid
import tensorflow as tf
import os
from flask_cors import CORS
import gunicorn

app = Flask(__name__)
CORS(app)

# Load model and data
try:
    model = tf.keras.models.load_model("models/plant_disease_recog_model_pwp.keras")
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load disease data
try:
    with open("plant_disease.json", 'r', encoding='utf-8') as file:
        plant_disease = json.load(file)
    with open("plant_disease_hindi.json", 'r', encoding='utf-8') as file:
        plant_disease_hindi = json.load(file)
    print("Disease data loaded successfully")
except Exception as e:
    print(f"Error loading disease data: {e}")
    plant_disease = {}
    plant_disease_hindi = {}

# Routes
@app.route('/')
def home():
    return render_template('mobile_home.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint for mobile app"""
    return jsonify({
        "status": "healthy", 
        "model_loaded": model is not None,
        "disease_data_loaded": len(plant_disease) > 0
    })

@app.route('/api/uploadimages/<path:filename>')
def uploaded_images(filename):
    return send_from_directory('./uploadimages', filename)

@app.route('/api/predict', methods=['POST'])
def predict_disease():
    """API endpoint for mobile app predictions"""
    try:
        if model is None:
            return jsonify({"error": "Model not available"}), 500
            
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
        if os.path.exists(temp_name):
            os.remove(temp_name)
        
        return jsonify({
            "success": True,
            "prediction": prediction
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_features(image):
    """Extract features from image"""
    try:
        image = tf.keras.utils.load_img(image, target_size=(160, 160))
        feature = tf.keras.utils.img_to_array(image)
        feature = np.array([feature])
        return feature
    except Exception as e:
        raise Exception(f"Error processing image: {e}")

def model_predict(image):
    """Make prediction using model"""
    try:
        img = extract_features(image)
        prediction = model.predict(img)
        
        # Get disease information
        disease_index = prediction.argmax()
        
        if disease_index < len(plant_disease) and disease_index < len(plant_disease_hindi):
            prediction_label = plant_disease[disease_index]
            prediction_label_hindi = plant_disease_hindi[disease_index]
        else:
            # Fallback if index out of range
            prediction_label = {"name": "Unknown Disease", "cause": "Unknown", "cure": "Unknown"}
            prediction_label_hindi = {"name_hindi": "अज्ञात रोग", "cause_hindi": "अज्ञात", "cure_hindi": "अज्ञात"}
        
        detailed_result = {
            'name': prediction_label.get('name', 'Unknown'),
            'name_hindi': prediction_label_hindi.get('name_hindi', 'अज्ञात रोग'),
            'cause': prediction_label.get('cause', 'Unknown cause'),
            'cause_hindi': prediction_label_hindi.get('cause_hindi', 'अज्ञात कारण'),
            'cure': prediction_label.get('cure', 'Unknown cure'),
            'cure_hindi': prediction_label_hindi.get('cure_hindi', 'अज्ञात इलाज'),
            'symptoms': prediction_label_hindi.get('symptoms', 'Unknown symptoms'),
            'symptoms_hindi': prediction_label_hindi.get('symptoms_hindi', 'अज्ञात लक्षण'),
            'prevention': prediction_label_hindi.get('prevention', 'Unknown prevention'),
            'prevention_hindi': prediction_label_hindi.get('prevention_hindi', 'अज्ञात रोकथाम'),
            'severity': prediction_label_hindi.get('severity', 'Unknown'),
            'severity_hindi': prediction_label_hindi.get('severity_hindi', 'अज्ञात'),
            'confidence': float(prediction.max() * 100)
        }
        
        return detailed_result
    except Exception as e:
        raise Exception(f"Error making prediction: {e}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Step 2: Install Heroku CLI

#### 2.1 Download and Install Heroku CLI
1. Go to https://devcenter.heroku.com/articles/heroku-cli
2. Download and install for Windows
3. Restart your computer

#### 2.2 Login to Heroku
Open Command Prompt and run:
```bash
heroku login
```
This will open your browser for authentication.

### Step 3: Create Heroku App

#### 3.1 Initialize Git
```bash
cd d:\pyproject\Crop_Project
git init
git add .
git commit -m "Initial commit"
```

#### 3.2 Create Heroku App
```bash
heroku create plant-disease-app
```
This will create a new app with a random name or use the name you provide.

#### 3.3 Add Buildpacks
```bash
heroku buildpacks:set heroku/python
```

### Step 4: Deploy to Heroku

#### 4.1 Push to Heroku
```bash
git push heroku main
```

#### 4.2 Scale the App
```bash
heroku ps:scale web=1
```

#### 4.3 Open the App
```bash
heroku open
```

### Step 5: Verify Deployment

#### 5.1 Check App Status
```bash
heroku logs --tail
```

#### 5.2 Test API Endpoints
- Open your app URL in browser
- Test: `https://your-app-name.herokuapp.com/api/health`
- Should return: `{"status": "healthy", "model_loaded": true}`

---

## Option 2: PythonAnywhere Deployment (Alternative)

### Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Create a free account
3. Verify your email

### Step 2: Upload Your Files

#### 2.1 Create Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask" framework
4. Choose Python 3.9
5. Click next

#### 2.2 Upload Files
1. Go to "Files" tab
2. Upload your project files:
   - `mobile_app.py`
   - `templates/mobile_home.html`
   - `plant_disease.json`
   - `plant_disease_hindi.json`
   - `models/plant_disease_recog_model_pwp.keras`
   - `requirements.txt`

#### 2.3 Configure Web App
1. In "Web" tab, edit your WSGI configuration
2. Replace the content with:
```python
import sys
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.append(path)

from mobile_app import app as application
```

### Step 3: Install Dependencies

#### 3.1 Install Packages
1. Go to "Consoles" tab
2. Start a Bash console
3. Run:
```bash
pip install flask flask-cors tensorflow numpy pillow gunicorn
```

### Step 4: Reload and Test

#### 4.1 Reload Web App
1. Go to "Web" tab
2. Click "Reload web app"

#### 4.2 Test Your App
Your app will be available at: `https://yourusername.pythonanywhere.com`

---

## Option 3: AWS EC2 (Advanced - More Control)

### Step 1: Create AWS Account

1. Go to https://aws.amazon.com
2. Create a free tier account
3. Complete registration

### Step 2: Launch EC2 Instance

#### 2.1 Create Instance
1. Go to EC2 Dashboard
2. Click "Launch Instances"
3. Choose "Ubuntu Server 20.04 LTS"
4. Select "t2.micro" (free tier)
5. Configure security group:
   - SSH (port 22)
   - HTTP (port 80)
   - HTTPS (port 443)

### Step 3: Setup Server

#### 3.1 Connect to Server
```bash
ssh -i your-key.pem ubuntu@your-server-ip
```

#### 3.2 Install Dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip nginx
pip3 install flask flask-cors tensorflow numpy pillow gunicorn
```

#### 3.3 Upload Your Files
Use SCP to upload your project files:
```bash
scp -i your-key.pem -r /path/to/your/project ubuntu@your-server-ip:/home/ubuntu/
```

### Step 4: Configure Web Server

#### 4.1 Create Systemd Service
```bash
sudo nano /etc/systemd/system/plantdisease.service
```

Add this content:
```ini
[Unit]
Description=Plant Disease Recognition App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/plantdisease
ExecStart=/usr/local/bin/gunicorn mobile_app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 4.2 Start Service
```bash
sudo systemctl enable plantdisease
sudo systemctl start plantdisease
```

---

## Step 5: Update Android App URL

### 5.1 Get Your Cloud URL
- **Heroku**: `https://your-app-name.herokuapp.com`
- **PythonAnywhere**: `https://yourusername.pythonanywhere.com`
- **AWS EC2**: `http://your-server-ip` or `https://your-domain.com`

### 5.2 Update Android MainActivity
Open `android_app/app/src/main/java/com/digitalkhopdi/plantdisease/MainActivity.java`:

```java
// Find this line in setupWebView() method:
webView.loadUrl("http://10.17.8.184:5000");

// Replace with your cloud URL:
webView.loadUrl("https://your-app-name.herokuapp.com");
```

### 5.3 Rebuild Android APK
1. Open Android Studio
2. Build → Build Bundle(s) / APK(s) → Build APK(s)
3. Install new APK on your device

---

## Step 6: Test Cloud Deployment

### 6.1 Test Web Interface
1. Open your cloud URL in browser
2. Test image upload and analysis
3. Verify Hindi text displays correctly

### 6.2 Test Android App
1. Install updated APK
2. Test all features:
   - App loads correctly
   - Image upload works
   - Analysis results display
   - Hindi text shows properly

### 6.3 Test API Endpoints
Test these URLs in browser or Postman:
- `https://your-cloud-url/api/health`
- `https://your-cloud-url/` (should show mobile interface)

---

## Step 7: Monitor and Maintain

### 7.1 Heroku Monitoring
```bash
heroku logs --tail
heroku ps
```

### 7.2 PythonAnywhere Monitoring
- Check "Web" tab for error logs
- Monitor CPU usage in account dashboard

### 7.3 AWS Monitoring
```bash
sudo systemctl status plantdisease
sudo journalctl -u plantdisease -f
```

---

## Troubleshooting

### Common Issues:

#### **Model Loading Errors**
- Ensure model file is uploaded correctly
- Check file paths in production
- Verify TensorFlow version compatibility

#### **CORS Issues**
- Ensure Flask-CORS is installed
- Check CORS configuration
- Verify API endpoints are accessible

#### **Memory Issues**
- Free tiers have memory limits
- Consider model optimization
- Monitor resource usage

#### **Connection Timeouts**
- Large model files may timeout
- Consider using CDN for static files
- Optimize model size

---

## Cost Comparison

| Platform | Free Tier | Paid Plans | Pros | Cons |
|----------|-----------|-------------|------|------|
| Heroku | 550 hours/month | $7+/month | Easy setup, Git deployment | Limited resources |
| PythonAnywhere | Limited | $5+/month | Web-based interface | Less flexible |
| AWS EC2 | 750 hours/month | $3.50+/month | Full control, scalable | More complex setup |

---

## Recommendation

**For beginners**: Use **Heroku** - easiest setup with Git deployment
**For simplicity**: Use **PythonAnywhere** - web-based interface
**For full control**: Use **AWS EC2** - most flexible option

Your Flask app will be accessible 24/7 without needing your local computer to be running!
