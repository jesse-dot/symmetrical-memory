"""
Web Server for Real-Time Screen Streaming
Provides a web interface to view the Windows device screen in real-time.
"""

from flask import Flask, Response, render_template_string
import mss
from PIL import Image
import io
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
HOST = os.getenv('WEB_SERVER_HOST', '0.0.0.0')
PORT = int(os.getenv('WEB_SERVER_PORT', '5000'))
FPS = 10  # Frames per second for streaming


# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Windows Device Screen - Live View</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #1a1a1a;
            font-family: Arial, sans-serif;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        h1 {
            color: #5865F2;
            margin-bottom: 10px;
        }
        .info {
            color: #b9bbbe;
            margin-bottom: 20px;
            text-align: center;
        }
        .stream-container {
            max-width: 95vw;
            max-height: 80vh;
            border: 3px solid #5865F2;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        img {
            width: 100%;
            height: auto;
            display: block;
        }
        .controls {
            margin-top: 20px;
            text-align: center;
        }
        .status {
            display: inline-block;
            padding: 8px 16px;
            background-color: #43b581;
            border-radius: 4px;
            font-weight: bold;
        }
        .footer {
            margin-top: 20px;
            color: #72767d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>🖥️ Windows Device Screen - Live View</h1>
    <div class="info">
        Real-time screen streaming from Windows device<br>
        Updates: {{ fps }} FPS
    </div>
    <div class="stream-container">
        <img src="{{ url_for('video_feed') }}" alt="Live Screen Feed">
    </div>
    <div class="controls">
        <span class="status">🟢 LIVE</span>
    </div>
    <div class="footer">
        Control this device using Discord slash commands
    </div>
</body>
</html>
"""


def generate_frames():
    """Generate frames for MJPEG streaming."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        
        while True:
            try:
                # Capture screenshot
                screenshot = sct.grab(monitor)
                img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
                
                # Resize for better streaming performance (optional)
                # Uncomment the next line to resize to 1280x720
                # img.thumbnail((1280, 720), Image.Resampling.LANCZOS)
                
                # Convert to JPEG bytes
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG', quality=85, optimize=True)
                frame = img_bytes.getvalue()
                
                # Yield frame in MJPEG format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                
                # Control frame rate
                time.sleep(1.0 / FPS)
                
            except Exception as e:
                print(f"Error generating frame: {e}")
                time.sleep(0.1)


@app.route('/')
def index():
    """Render the main page with the video stream."""
    return render_template_string(HTML_TEMPLATE, fps=FPS)


@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'ok', 'service': 'screen_streaming'}


def run_server():
    """Run the Flask web server."""
    print(f"Starting web server on {HOST}:{PORT}")
    print(f"Access the screen viewer at: http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, threaded=True, debug=False)


if __name__ == "__main__":
    run_server()
