document.addEventListener('DOMContentLoaded', () => {
    const videoForm = document.getElementById('videoGenerationForm');
    const videoResult = document.getElementById('videoResult');

    videoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(videoForm);
        
        try {
            const response = await fetch('/video', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.video_path) {
                videoResult.innerHTML = `
                    <video controls class="w-full max-w-lg mx-auto">
                        <source src="${result.video_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                `;
            } else {
                videoResult.innerHTML = '<p class="text-red-500">Video generation failed</p>';
            }
        } catch (error) {
            console.error('Error:', error);
            videoResult.innerHTML = '<p class="text-red-500">An error occurred</p>';
        }
    });
});

// Feature analysis form
document.addEventListener('DOMContentLoaded', () => {
    const analysisForm = document.getElementById('moonAnalysisForm');
    
    analysisForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(analysisForm);
        
        try {
            const response = await fetch('/features', {
                method: 'POST',
                body: formData
            });
            
            const results = await response.json();
            
            // Update results on the page
            document.getElementById('phaseAngleResult').textContent = results.phase_angle || 'N/A';
            document.getElementById('sunAngleResult').textContent = results.sun_angle || 'N/A';
            document.getElementById('depthEstimationResult').textContent = results.depth_estimation || 'N/A';
            document.getElementById('terrainMappingResult').textContent = results.terrain_mapping || 'N/A';
            
            // Handle crater detection (might be an image or list)
            const craterResult = document.getElementById('craterDetectionResult');
            if (results.crater_detection) {
                if (typeof results.crater_detection === 'string') {
                    craterResult.textContent = results.crater_detection;
                } else if (Array.isArray(results.crater_detection)) {
                    craterResult.innerHTML = results.crater_detection.map(crater => 
                        `<p>Crater: ${crater.location}, Size: ${crater.size}</p>`
                    ).join('');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            craterResult.innerHTML = '<p class="text-red-500">Analysis failed</p>';
        }
    });
});