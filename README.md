# Lunar Analysis

AI Based Video generation of Lunar Analysis with Flask and OpenCV.

## Features

- Real-time face detection and recognition
- Automated attendance tracking
- User-friendly web interface
- Secure data storage
- Export attendance records

## Prerequisites

- Python 3.7+
- Web camera or integrated laptop camera
- Required Python packages:
  ```bash
  pip install flask opencv-python numpy werkzeug
  ```

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/tarunnnrathoddd/LunarProject.git
   cd face-recognition-attendance
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Register new students/staff by adding their photos
2. Start the attendance session
3. The system will automatically detect and mark attendance
4. View and export attendance records as needed

## Project Structure

```
├── app.py
├── templates/
├── static/
├── data/
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV team
- Flask community
- All contributors to this project
