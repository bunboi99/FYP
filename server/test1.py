import numpy as np
from PIL import Image
from base_camera import BaseCamera
import io

class TestCamera(BaseCamera):
    @staticmethod
    def frames():
        while True:

            black_image= np.zeros((480,640,3),dtype=np.uint8)
            # Replace this with the logic to capture frames from your camera
            # For now, let's return a simple black image
            yield black_image.tobytes()

def display_camera():
    camera = TestCamera()

    while True:
        # Get the current frame from the camera
        frame = camera.get_frame()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera
    camera.release_camera()

if __name__ == '__main__':
    display_camera()