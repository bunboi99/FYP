from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)  # Open the first camera connected to the computer.

    while True:
        ret, frame = cap.read()  # Read one frame from the camera
        if not ret:  # If no frame could be read (camera disconnected, for example), break the loop
            break
        # Encode the frame as a JPEG image
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:  # If the frame could not be encoded, continue with the next frame
            continue
        # Yield the encoded frame in the multipart HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)