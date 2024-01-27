import cv2
import numpy as np
from camera_pi import Camera
from flask import Flask, render_template, Response

# Load the MobileNetSSD model
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    try:
        while True:
            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                    "sofa", "train", "tvmonitor"]

            frame = camera.get_frame()
            frame = np.frombuffer(frame, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Prepare the frame to be fed to the network
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

            # Pass the blob through the network and obtain the detections and predictions
            net.setInput(blob)
            detections = net.forward()

            # Loop over the detections
            for i in range(0, detections.shape[2]):
                # Extract the confidence (i.e., probability) associated with the prediction
                confidence = detections[0, 0, i, 2]

                # Filter out weak detections by ensuring the `confidence` is greater than a minimum confidence
                if confidence > 0.2:
                    # Compute the (x, y)-coordinates of the bounding box for the object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # Extract the class label from the `detections`
                    class_id = int(detections[0, 0, i, 1])
                    label = CLASSES[class_id]

                    # Draw the bounding box and the confidence level on the frame
                    label = "{}: {:.2f}%".format(label, confidence * 100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Encode the frame into JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n--frame\r\n'
    except KeyboardInterrupt:
        camera.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)