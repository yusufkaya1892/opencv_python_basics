import cv2
import numpy as np

frame = cv2.imread("pics/colored.png")

lower = np.array([100, 150, 0]) 
upper = np.array([140, 255, 255])

MIN_AREA = 800

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)

kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  
mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    
    contours = [c for c in contours if cv2.contourArea(c) > MIN_AREA]
    
    if contours:

        largest = max(contours, key = cv2.contourArea)

        x,y,w,h = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

        cv2.putText(frame, "Object detected", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        
        cv2.drawContours(frame, [largest], -1, (0,255,0), 2)



cv2.imshow("Org", frame)
cv2.imshow("mask", mask),

cv2.waitKey(0)
cv2.destroyAllWindows()