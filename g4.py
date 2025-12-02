import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

glasses = cv2.imread("pics/glasses.png", cv2.IMREAD_UNCHANGED)

def overlay_png(frame, png, x, y, w, h):
    
    png = cv2.resize(png, (w, h))

    # channel ayır
    b, g, r, a = cv2.split(png)
    overlay_color = cv2.merge((b, g, r))

    # mask oluştur
    mask = cv2.merge((a, a, a))

    roi = frame[y:y+h, x:x+w]

    roi = roi.astype(float)
    overlay_color = overlay_color.astype(float)
    mask = mask.astype(float) / 255

    blended = (mask * overlay_color + (1 - mask) * roi)
    blended = blended.astype("uint8")

    frame[y:y+h, x:x+w] = blended
    return frame

cap = cv2.VideoCapture(0)

print(f"press q to exit")

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3, 5)

    #yüzleri sayan kısım
    cv2.putText(frame, f"Faces: {len(faces)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)



    ## filtrelerin hepsi
    for (x, y, w, h) in faces:

        #Blur
        face_region = frame[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face_region, (35, 35), 30)
        frame[y:y+h, x:x+w] = blurred_face

        #Glass Filter
        if glasses is not None:
            gh = int(h * 0.4)
            gy = y + int(h * 0.25) 
            frame = overlay_png(frame, glasses, x, gy, w, gh)

    cv2.imshow("face filters", frame)

    

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()