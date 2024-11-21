import cv2
import numpy as np

def detect_StopLine(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    roi = edges[frame.shape[0] // 2:, :]  # Only consider the bottom half of the frame

    # Find contours in the region of interest
    contours = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]


    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        # If the polygon has 4 sides, it might be a stop line
        if len(approx) == 4:
            # Compute the bounding box of the contour
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            # Check if the aspect ratio is within a reasonable range for a stop line
            if 2 < aspect_ratio < 10:
                return True

    return False