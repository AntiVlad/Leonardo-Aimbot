import cv2
import numpy as np
# import serial
import time
from mss import mss

# arduino = serial.Serial('COM3', 9600) 

screen_width = 1920  
screen_height = 1080  
capture_width = 25  
capture_height = 25

# Centre of the screen
left = (screen_width - capture_width) // 2
top = (screen_height - capture_height) // 2

monitor = {"top": top, "left": left, "width": capture_width, "height": capture_height}
sct = mss()

# color range in HSV
lower_red = np.array([0, 120, 70])  
upper_red = np.array([10, 255, 255])  

while True:
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)  
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(largest_contour)
        target_x, target_y = x + w // 2, y + h // 2

        # arduino.write(f"{target_x},{target_y}\n".encode())
        print(f"Coordinates: {target_x}, {target_y}")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (target_x, target_y), 5, (255, 0, 0), -1)

    # Testing purposes
    cv2.imshow("Center Screen Capture", frame)
    cv2.imshow("Mask", mask)

    # Break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
# arduino.close()
