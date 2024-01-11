import cv2
from base_camera import BaseCamera

def display_camera():
    camera = BaseCamera()

    while True:
        # Get the current frame from the camera
        frame = camera.get_frame()

        # Display the frame in a pop-up window
        cv2.imshow('Camera View', frame)

        # Check for the 'q' key to exit the loop and close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    camera.release_camera()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    display_camera()
