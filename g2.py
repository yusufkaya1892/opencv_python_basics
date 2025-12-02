import cv2
import numpy as np

drawing = False
last_point = None

def draw(event, x, y, flags, param):
    global drawing, last_point, frame

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.line(frame, last_point, (x, y), (0, 255, 0), 3)
        last_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        last_point = None


cap = cv2.VideoCapture(0)
cv2.namedWindow("Video Wizard")
cv2.setMouseCallback("Video Wizard", draw)


video = cv2.VideoCapture("pics/vid.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame,1)


    cv2.rectangle(frame, (50, 50), (200, 200), (255, 0, 0), 3)
    cv2.circle(frame, (350, 150), 50, (0, 255, 0), 3)
    cv2.putText(frame, "Hello!", (50, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    
    cv2.imshow("Video wizard", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        cv2.imwrite("pics/screenshot.png", frame)
        print(f"screenshot taken")


    if key == ord('v'):
        while True:
            ret2, vid_frame = video.read()
            if not ret2:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0) #restart atıyor
                break

            cv2.imshow("Video wizard", vid_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    
    if key == ord('q'):
        break

cap.release()
video.release()
cv2.destroyAllWindows()

