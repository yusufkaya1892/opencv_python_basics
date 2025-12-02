import cv2
import numpy as np

img = cv2.imread("pics/lm.jpg")

cv2.imshow("org", img)

height, width = img.shape[:2]

if len(img.shape) == 3:
    channels = img.shape[2]

else:
    channels = 1

print(f"image dimensions: {width}x{height}")
print(f"color channels: {channels}")

B, G, R = cv2.split(img)
cv2.imshow('Blue channel', B)
cv2.imshow('Green  channel', G)
cv2.imshow('Red channel', R)

swapped_img = img.copy()
swapped_img[:, :, [0, 2]] = swapped_img[:, :, [2, 0]] ## blue ve red swap için
cv2.imshow("Red-Blue Swapped", swapped_img)

cropped_img = img[50:300, 100:400]

resized_img = cv2.resize(cropped_img, (200, 200))

cv2.imshow('Cropped', cropped_img)
cv2.imshow('Resized', resized_img)



cv2.waitKey(0)
cv2.destroyAllWindows()