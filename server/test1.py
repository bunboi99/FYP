from PIL import Image
from base_camera import BaseCamera
import io

def display_camera():
    camera = BaseCamera()

    while True:
        # Get the current frame from the camera
        frame = camera.get_frame()

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