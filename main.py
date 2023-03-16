import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 90, 160)
    # cv2.imshow("Canny", edged)
    # find the contour with the largest area
    cnts, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    screenCnt = None
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if the contour has four vertices, we have found the screen
        if len(approx) == 4:
            screenCnt = approx
            break

    # draw a rectangle around the screen
    if screenCnt is not None:
        x, y, w, h = cv2.boundingRect(screenCnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # apply mask only on the region inside the rectangle
        roi = frame[y : y + h, x : x + w]
        screen_mask = np.zeros_like(roi)
        # Convert the ROI to HSV color space
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # Define the lower and upper bounds of the red color
        lower_red = np.array([0, 70, 70])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([170, 70, 70])
        upper_red2 = np.array([180, 255, 255])
        # Create masks for the two ranges of red color
        mask1 = cv2.inRange(hsv_roi, lower_red, upper_red)
        mask2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
        # Combine the masks
        screen_mask = cv2.bitwise_or(mask1, mask2)
        # Count the number of non-zero pixels in the mask
        num_pixels = cv2.countNonZero(screen_mask)
        # If all pixels are red, break the loop and print a message
        print(num_pixels, ":", roi.size / 3)
        if num_pixels > 3000 and abs(num_pixels - roi.size / 3) < 0xFFFFFFFFFFFDAF2F:
            print("Screen is completely red!")
            time.sleep(3)
            break

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
