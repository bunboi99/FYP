# test1.py

import time
from move import setup, move, motorStop, destroy
from ultra import checkdist

def main():
    try:
        setup()  # Initialize motors

        while True:
            distance = checkdist()*100  # Convert distance to centimeters
            print("Distance: %.2f cm" % distance)

            if distance < 10:
                print("Obstacle detected. Stopping.")
                motorStop()
                break
            else:
                print("Moving forward.")
                move(50, 'forward', 'no', 0.8)
                time.sleep(0.1)  # Adjust the sleep duration as needed

    except KeyboardInterrupt:
        destroy()  # Clean up GPIO on Ctrl+C

if __name__ == "__main__":
    main()
