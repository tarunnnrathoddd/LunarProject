document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('moonCanvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size
    canvas.width = 400;
    canvas.height = 400;

    // Moon properties
    const moonRadius = 150;
    let rotation = 0;

    // Create moon gradient
    function createMoonGradient() {
        const gradient = ctx.createRadialGradient(
            canvas.width / 2, canvas.height / 2, 0,
            canvas.width / 2, canvas.height / 2, moonRadius
        );
        gradient.addColorStop(0, '#a0a0a0');
        gradient.addColorStop(0.5, '#808080');
        gradient.addColorStop(1, '#606060');
        return gradient;
    }

    // Draw moon
    function drawMoon() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Save canvas state
        ctx.save();
        
        // Translate to center and rotate
        ctx.translate(canvas.width / 2, canvas.height / 2);
        ctx.rotate(rotation);
        
        // Draw moon body
        ctx.beginPath();
        ctx.arc(0, 0, moonRadius, 0, Math.PI * 2);
        ctx.fillStyle = createMoonGradient();
        ctx.fill();
        
        // Draw crater-like spots
        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        const craterPositions = [
            {x: -50, y: -30, size: 20},
            {x: 30, y: 40, size: 15},
            {x: -20, y: 60, size: 25},
            {x: 60, y: -50, size: 10}
        ];
        
        craterPositions.forEach(crater => {
            ctx.beginPath();
            ctx.arc(crater.x, crater.y, crater.size, 0, Math.PI * 2);
            ctx.fill();
        });
        
        // Restore canvas state
        ctx.restore();
    }

    // Animation loop
    function animate() {
        rotation += 0.01;
        drawMoon();
        requestAnimationFrame(animate);
    }

    // Start animation
    animate();
});