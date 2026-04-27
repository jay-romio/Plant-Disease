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
    """Make prediction using model"""
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
