from flask import Flask, render_template, request, jsonify, send_file
import os
from models.moon_analysis import MoonAnalyzer
from models.video_generator import VideoGenerator
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/video', methods=['GET', 'POST'])
def video_generation():
    if request.method == 'POST':
        # Handle image upload and video generation
        try:
            image1 = request.files['image1']
            image2 = request.files['image2']
            
            # Save uploaded images
            image1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
            image2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')
            image1.save(image1_path)
            image2.save(image2_path)
            
            # Generate video (placeholder for actual implementation)
            video_generator = VideoGenerator()
            video_path = video_generator.generate_video(image1_path, image2_path)
            
            return jsonify({'video_path': video_path})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('video.html')

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        if 'image1' not in request.files or 'image2' not in request.files:
            return 'Missing files', 400
            
        image1 = request.files['image1']
        image2 = request.files['image2']
        
        if not image1.filename or not image2.filename:
            return 'No selected files', 400
            
        # Save uploaded images
        img1_path = os.path.join(UPLOAD_FOLDER, secure_filename(image1.filename))
        img2_path = os.path.join(UPLOAD_FOLDER, secure_filename(image2.filename))
        image1.save(img1_path)
        image2.save(img2_path)
        
        # Read images
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        
        if img1 is None or img2 is None:
            return 'Failed to read images', 500
        
        # Ensure same size
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        # Generate intermediate frames
        num_frames = 30
        frames = []
        for i in range(num_frames):
            alpha = i / (num_frames - 1)
            interpolated = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
            frames.append(interpolated)
        
        # Create video
        output_path = os.path.join(UPLOAD_FOLDER, 'interpolated_video.mp4')
        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 24, (width, height))
        
        for frame in frames:
            out.write(frame)
        out.release()
        
        # Cleanup
        os.remove(img1_path)
        os.remove(img2_path)
        
        return send_file(output_path, mimetype='video/mp4')
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Add logging
        return str(e), 500

@app.route('/features', methods=['POST'])
def analyze_moon():
    try:
        # Receive moon image
        moon_image = request.files['moon_image']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'moon_analysis.jpg')
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
        
        return jsonify(analysis_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/features')
def features_page():
    return render_template('features.html')

if __name__ == '__main__':
    app.run(debug=True)