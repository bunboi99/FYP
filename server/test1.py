import cv2
from base_camera import BaseCamera

class MyCamera(BaseCamera):
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)  # You can change this to the appropriate camera index
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # Read current frame from the camera
            _, img = camera.read()

            # Encode the frame as JPEG
            if cv2.imencode('.jpg', img)[0]:
                yield cv2.imencode('.jpg', img)[1].tobytes()

if __name__ == '__main__':
    # Create an instance of the MyCamera class
    my_camera = MyCamera()

    while True:
        # Get the current frame from the camera
        frame = my_camera.get_frame()

        # Display the frame in a pop-up window
        cv2.imshow('Camera View', frame)

        # Check for the 'q' key to exit the loop and close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    my_camera.release_camera()
    cv2.destroyAllWindows()
