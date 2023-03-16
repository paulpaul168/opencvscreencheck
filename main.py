import cv2
import numpy as np
import time


def detect_cracks(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5:
            cv2.drawContours(img, contour, -1, (0, 0, 255), 3)
            print("Screen is cracked")
    return img


def find_screen_mask(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 90, 160)
    cnts, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break
    if screenCnt is not None:
        x, y, w, h = cv2.boundingRect(screenCnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi = frame[y : y + h, x : x + w]
        return roi
    else:
        return None


def is_frame_color(frame, color, threshold_percent):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the color range in HSV
    if color == "red":
        lower_color1 = np.array([0, 70, 70])
        upper_color1 = np.array([10, 255, 255])
        lower_color2 = np.array([170, 70, 70])
        upper_color2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_color1, upper_color1)
        mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
        mask = cv2.bitwise_or(mask1, mask2)
    elif color == "green":
        lower_color = np.array([40, 40, 40])
        upper_color = np.array([70, 255, 255])
        mask = cv2.inRange(hsv, lower_color, upper_color)
    elif color == "blue":
        lower_color = np.array([100, 50, 50])
        upper_color = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_color, upper_color)

    # Calculate the percentage of pixels in the mask
    num_blue_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    percent_blue = num_blue_pixels / total_pixels * 100

    # Check if the percentage of blue is greater than the threshold
    if percent_blue >= threshold_percent:
        return True
    else:
        return False


def get_red_mask(roi):
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 70, 70])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 70])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv_roi, lower_red, upper_red)
    mask2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
    screen_mask = cv2.bitwise_or(mask1, mask2)
    return screen_mask


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    screen_mask = find_screen_mask(frame)

    if screen_mask is not None and False:
        frame = detect_cracks(screen_mask)

    if screen_mask is not None and False:
        num_pixels = cv2.countNonZero(get_red_mask(screen_mask))
        if (
            num_pixels > 10000
            and abs(num_pixels - screen_mask.size / 3) < 0xFFFFFFFFFFFDAF2F
        ):
            print("Screen is completely red!")
            time.sleep(3)
            # break
    if screen_mask is not None:
        if is_frame_color(screen_mask, "blue", 90):
            print("Screen is blue")
        if is_frame_color(screen_mask, "red", 90):
            print("Screen is red")
        if is_frame_color(screen_mask, "green", 90):
            print("Screen is green")

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
