import os
import cv2
import numpy as np

def generate_lunar_transition_video(image1_path, image2_path, output_video_path):
    # Load images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    if img1 is None or img2 is None:
        raise ValueError("Error loading images. Ensure images exist in the specified path.")

    # Define video parameters
    frame_rate = 30  # FPS
    resolution = (800, 600)  # Ensure consistency

    # Resize images to match resolution
    img1 = cv2.resize(img1, resolution)
    img2 = cv2.resize(img2, resolution)

    # Convert images to grayscale for optical flow
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute dense optical flow (Farneback)
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Fix the shape order for grid mapping
    h, w = gray1.shape  # Ensure correct ordering
    grid_x, grid_y = np.meshgrid(np.arange(w), np.arange(h))  # Shape (600, 800)

    # Initialize video writer
    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, resolution)

    # Function to analyze craters and filter both large and small craters
    def analyze_lunar_surface(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (25, 25), 15)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(12, 12))
        gray = clahe.apply(blurred)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 41, 6)
        kernel = np.ones((7, 7), np.uint8)
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        small_craters = []
        large_craters = []

        for c in contours:
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if area > 100 and 0.7 < circularity < 1.3:
                if area > 300:
                    large_craters.append(c)
                else:
                    small_craters.append(c)

        cv2.drawContours(image, small_craters, -1, (255, 0, 0), 2)
        cv2.drawContours(image, large_craters, -1, (0, 255, 0), 3)
        return image

    # Hold the first image for 3 seconds (90 frames)
    for _ in range(90):
        crater_frame = analyze_lunar_surface(img1.copy())
        video_writer.write(crater_frame)

    # Smooth transition from first to last image using Optical Flow
    for alpha in np.linspace(0, 1, 720):
        warp_x = (grid_x + alpha * flow[..., 0]).astype(np.float32)
        warp_y = (grid_y + alpha * flow[..., 1]).astype(np.float32)
        warped_frame = cv2.remap(img1, warp_x, warp_y, cv2.INTER_LINEAR)
        blended = cv2.addWeighted(warped_frame, 1 - alpha**2, img2, alpha**2, 0)
        crater_frame = analyze_lunar_surface(blended.copy())
        video_writer.write(crater_frame)

    # Hold the last image for 3 seconds (90 frames)
    for _ in range(90):
        crater_frame = analyze_lunar_surface(img2.copy())
        video_writer.write(crater_frame)

    video_writer.release()
    print(f"Super smooth transition video with crater detection saved at {output_video_path}")

# Example usage
# generate_lunar_transition_video('image1.jpg', 'image2.jpg', 'Chandrayaan3_SuperSmoothTransition.mp4')