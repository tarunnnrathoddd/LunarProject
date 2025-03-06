from flask import Flask, render_template, request, jsonify, send_file, url_for, send_from_directory
import os
import time  # Add this import
from models.moon_analysis import MoonAnalyzer
from models.video_generator import VideoGenerator
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from a import generate_lunar_transition_video  # Import function from a.py

# Define constants first
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload-images', methods=['POST'])
def upload_images():
    if 'image1' not in request.files or 'image2' not in request.files:
        return "Please upload both images!", 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1.filename == '' or image2.filename == '':
        return "No selected files!", 400

    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    try:
        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_video.mp4')

        image1.save(image1_path)
        image2.save(image2_path)

        # Generate video
        generate_lunar_transition_video(image1_path, image2_path, video_path)

        # Clean up input images
        os.remove(image1_path)
        os.remove(image2_path)

        return send_file(
            video_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name='moon_transition.mp4'
        )

    except Exception as e:
        return str(e), 500

@app.route('/features', methods=['POST'])
def analyze_moon():
    try:
        if 'moon_image' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        moon_image = request.files['moon_image']
        
        if not moon_image.filename:
            return jsonify({'error': 'No selected file'}), 400
            
        if not allowed_file(moon_image.filename):
            return jsonify({'error': 'Invalid file type'}), 400
            
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(moon_image.filename))
        moon_image.save(image_path)
        
        # Perform moon analysis
        moon_analyzer = MoonAnalyzer()
        analysis_results = {
            'phase_angle': moon_analyzer.calculate_phase_angle(image_path),
            'sun_angle': moon_analyzer.calculate_sun_angle(image_path),
            'depth_estimation': moon_analyzer.estimate_depth(image_path),
            'terrain_mapping': moon_analyzer.generate_terrain_map(image_path),
            'crater_detection': moon_analyzer.detect_craters(image_path)
        }
        
        # Cleanup
        os.remove(image_path)
        
        return jsonify(analysis_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/features')
def features_page():
    return render_template('features.html')

@app.route('/video-generation')
def video_generation():
    return render_template('video.html')

@app.route('/generate-video', methods=['POST'])
def generate_video():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'error': 'Please upload both images!'}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1.filename == '' or image2.filename == '':
        return jsonify({'error': 'No selected files!'}), 400

    try:
        # Ensure directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Generate unique filename using timestamp
        timestamp = int(time.time())
        video_filename = f'output_{timestamp}.mp4'
        
        # Save uploaded files
        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], f'image1_{timestamp}.jpg')
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], f'image2_{timestamp}.jpg')
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)

        image1.save(image1_path)
        image2.save(image2_path)

        # Generate video
        generate_lunar_transition_video(image1_path, image2_path, video_path)

        # Clean up input images
        os.remove(image1_path)
        os.remove(image2_path)

        # Return video URL
        video_url = url_for('static', filename=f'uploads/{video_filename}')
        return jsonify({
            'success': True,
            'video_url': video_url,
            'message': 'Video generated successfully!'
        })

    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({'error': f"Error generating video: {str(e)}"}), 500

# Add this new route to serve the static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)