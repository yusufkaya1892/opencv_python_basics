import cv2
import numpy as np

backsub = cv2.createBackgroundSubtractorMOG2()

cap = cv2.VideoCapture(0)

pathpoints = []

print("press Q to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fg_mask = backsub.apply(frame)

    kernel = np.ones((5,5), np.uint8)
    fg_mask = cv2.erode(fg_mask, kernel, iterations=1)
    fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_area = 0
    largest_center = None

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 800: 
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        if area > largest_area:
            largest_area = area
            largest_center = (x + w//2, y + h//2)

    if largest_center is not None:
        pathpoints.append(largest_center)
        for i in range(1, len(pathpoints)):
            cv2.line(frame, pathpoints[i-1], pathpoints[i], (0,0,255), 2)

    zone_x1, zone_y1 = 200, 100
    zone_x2, zone_y2 = 440, 340
    cv2.rectangle(frame, (zone_x1, zone_y1), (zone_x2, zone_y2), (255,0,0), 2)

    if largest_center is not None:
        cx, cy = largest_center
        if zone_x1 < cx < zone_x2 and zone_y1 < cy < zone_y2:
            cv2.putText(frame, "Alert **** ", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

    cv2.imshow("Motion Tracking Security System", frame)
    cv2.imshow("Foreground Mask", fg_mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
