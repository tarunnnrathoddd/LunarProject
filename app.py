from flask import Flask, render_template, request, jsonify
import os
from models.moon_analysis import MoonAnalyzer
from models.video_generator import VideoGenerator

app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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