import numpy as np
from PIL import Image
from base_camera import BaseCamera
import io

class TestCamera(BaseCamera):
    @staticmethod
    def frames():
        while True:
            # Replace this with the logic to capture frames from your camera
            # For now, let's return a simple black image
            yield (b'255' * 640 * 480 * 3)

def display_camera():
    camera = TestCamera()

    while True:
        # Get the current frame from the camera
        frame = camera.get_frame()

        # Convert the frame to a numpy array
        frame = np.frombuffer(frame, dtype=np.uint8).reshape((480, 640, 3))

        # Convert the OpenCV image to a Pillow image
        pillow_image = Image.fromarray(frame)

        # Display the Pillow image in a pop-up window
        pillow_image.show()

        # Check for the 'q' key to exit the loop and close the window
        key = input("Press 'q' to quit: ")
        if key.lower() == 'q':
            break

    # Release the camera
    camera.release_camera()

if __name__ == '__main__':
    display_camera()