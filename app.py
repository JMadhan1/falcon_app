import os
import cv2
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io
import json
from datetime import datetime
import traceback

app = Flask(__name__)

# Flask Configuration - Ensure JSON responses for all errors
app.config['PROPAGATE_EXCEPTIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_SORT_KEYS'] = False

# Configuration
MODEL_PATH = 'best.pt'

# Use /tmp directory on Vercel (writable), local directories otherwise
if os.environ.get('VERCEL'):
    UPLOAD_FOLDER = '/tmp/uploads'
    FEEDBACK_FOLDER = '/tmp/feedback_data'
else:
    UPLOAD_FOLDER = 'static/uploads'
    FEEDBACK_FOLDER = 'feedback_data'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FEEDBACK_FOLDER, exist_ok=True)

# Global model variable
model = None
model_load_error = None

def get_model():
    """Load the YOLO model with comprehensive error handling"""
    global model, model_load_error
    
    if model is not None:
        return model
        
    if model_load_error is not None:
        # Don't retry if we already failed
        return None
    
    print("📦 Loading YOLOv8 Model...")
    print(f"📂 Current working directory: {os.getcwd()}")
    print(f"📂 Model path: {MODEL_PATH}")
    print(f"📂 Model exists: {os.path.exists(MODEL_PATH)}")
    
    try:
        if not os.path.exists(MODEL_PATH):
            model_load_error = f"Model file not found at {MODEL_PATH}"
            print(f"❌ {model_load_error}")
            return None
            
        if not os.path.isfile(MODEL_PATH):
            model_load_error = f"Model path exists but is not a file: {MODEL_PATH}"
            print(f"❌ {model_load_error}")
            return None
            
        # Check file size
        file_size = os.path.getsize(MODEL_PATH)
        print(f"📊 Model file size: {file_size / (1024*1024):.2f} MB")
        
        if file_size < 1000:
            model_load_error = f"Model file seems too small ({file_size} bytes), possibly corrupted"
            print(f"❌ {model_load_error}")
            return None
        
        # Attempt to load the model
        model = YOLO(MODEL_PATH)
        print("✅ Model loaded successfully!")
        print(f"📋 Model classes: {model.names}")
        return model
        
    except Exception as e:
        model_load_error = f"Error loading model: {str(e)}"
        print(f"❌ {model_load_error}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint to verify model status"""
    model_status = {
        'model_loaded': model is not None,
        'model_path': MODEL_PATH,
        'model_exists': os.path.exists(MODEL_PATH),
        'current_dir': os.getcwd(),
        'error': model_load_error
    }
    
    if os.path.exists(MODEL_PATH):
        model_status['model_size_mb'] = os.path.getsize(MODEL_PATH) / (1024*1024)
    
    # Try to load model if not loaded
    if model is None and model_load_error is None:
        get_model()
        model_status['model_loaded'] = model is not None
        model_status['error'] = model_load_error
    
    status_code = 200 if model is not None else 503
    return jsonify(model_status), status_code

# Error handlers to ensure JSON responses
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response"""
    return jsonify({'error': 'Not found', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with JSON response"""
    print(f"500 Error: {str(error)}")
    return jsonify({'error': 'Internal server error', 'status': 500}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions with JSON response"""
    print(f"Unhandled exception: {str(e)}")
    print(f"Traceback: {traceback.format_exc()}")
    return jsonify({
        'error': str(e),
        'type': type(e).__name__,
        'status': 500
    }), 500

@app.route('/detect', methods=['POST'])
def detect():
    """Main detection endpoint with comprehensive error handling"""
    try:
        # Check model is loaded
        current_model = get_model()
        if not current_model:
            error_msg = model_load_error or 'Model failed to load. Check server logs.'
            print(f"❌ Detection failed - Model not loaded: {error_msg}")
            return jsonify({
                'error': error_msg,
                'suggestion': 'Check /health endpoint for model status'
            }), 500
        
        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        print(f"📸 Processing image: {file.filename}")
        
        # Read and validate image
        try:
            img_bytes = file.read()
            if len(img_bytes) == 0:
                return jsonify({'error': 'Empty file uploaded'}), 400
                
            img = Image.open(io.BytesIO(img_bytes))
            img_np = np.array(img)
            print(f"📊 Image shape: {img_np.shape}")
            
        except Exception as e:
            print(f"❌ Image processing error: {str(e)}")
            return jsonify({'error': f'Invalid image file: {str(e)}'}), 400

        # Run inference
        try:
            print("🔍 Running YOLO inference...")
            results = current_model.predict(img_np, conf=0.25)
            result = results[0]
            print(f"✅ Inference complete. Found {len(result.boxes)} detections")
            
        except Exception as e:
            print(f"❌ Inference error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': f'Model inference failed: {str(e)}'}), 500
        
        # Process detections
        detections = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            name = result.names[cls_id]
            
            detections.append({
                'class': name,
                'confidence': f"{conf:.1%}",
                'bbox': box.xyxy[0].tolist()
            })
            print(f"  🎯 Detected: {name} ({conf:.1%})")

        # Convert plot to base64
        try:
            res_plotted = result.plot()
            res_plotted_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
            res_pil = Image.fromarray(res_plotted_rgb)
            
            buffered = io.BytesIO()
            res_pil.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
        except Exception as e:
            print(f"❌ Image encoding error: {str(e)}")
            return jsonify({'error': f'Failed to encode result image: {str(e)}'}), 500
        
        # Save original image temporarily for feedback reference
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_query.jpg"
            img.save(os.path.join(UPLOAD_FOLDER, filename))
            print(f"💾 Saved image: {filename}")
        except Exception as e:
            print(f"⚠️ Warning: Could not save image: {str(e)}")
            filename = "unsaved"

        return jsonify({
            'success': True,
            'image': img_str,
            'detections': detections,
            'image_id': filename
        })

    except Exception as e:
        # Catch-all for any unexpected errors
        print(f"❌ Unexpected error in /detect: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'type': type(e).__name__
        }), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Endpoint to collect user feedback for Continuous Learning.
    This simulates sending data back to Falcon for retraining.
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        image_id = data.get('image_id')
        correct_class = data.get('correct_class')
        notes = data.get('notes')
        
        # In a real scenario, this would upload to S3 or Duality's API
        # Here we save metadata locally
        feedback_entry = {
            'image_id': image_id,
            'timestamp': datetime.now().isoformat(),
            'user_correction': correct_class,
            'notes': notes,
            'status': 'queued_for_falcon_retraining'
        }
        
        with open(os.path.join(FEEDBACK_FOLDER, 'feedback_log.json'), 'a') as f:
            f.write(json.dumps(feedback_entry) + '\n')
            
        print(f"📝 Feedback received for {image_id}: {correct_class}")
        return jsonify({'success': True, 'message': 'Feedback received. Data queued for Falcon retraining loop.'})
        
    except Exception as e:
        print(f"❌ Feedback error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Preload model before starting server
    print("🚀 Starting Flask application...")
    get_model()
    
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🌐 Server will run on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
