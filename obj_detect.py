from flask import Flask, render_template, Response
from camera_pi import Camera
import numpy as np
import cv2
import threading



# Load MobileNetSSD model
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def detect_objects(frame):
    # Define a list of labels for the classes that the model can detect
    classes = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    
    # Resize the frame to 300x300 pixels (the input size that the model expects)
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # Pass the blob through the network and obtain the detections and predictions
    net.setInput(blob)
    detections = net.forward()

    # Initialize an empty set to store the unique objects detected
    unique_objects = set()

    # Loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # Extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections by ensuring the confidence is greater than a minimum confidence
        if confidence > 0.2:
            # Extract the index of the class label from the detections
            idx = int(detections[0, 0, i, 1])

            # Add the class label to the set of unique objects
            unique_objects.add(classes[idx])

    # Print the unique objects detected
    print(unique_objects)

    # Return the unique objects
    return unique_objects



def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)  # Open the first camera connected to the computer.
    try:
        while True:
            ret, frame = cap.read()  # Read one frame from the camera
            if not ret:
                break  # If no frame could be read (camera disconnected, for example), break

            # Detect objects in the frame
            unique_objects= detect_objects(frame)

            # Encode the frame as a JPEG image
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:  # If the frame could not be encoded, continue with the next frame
                continue

            # Yield the encoded frame in the multipart HTTP response
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    except KeyboardInterrupt:
        cap.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

