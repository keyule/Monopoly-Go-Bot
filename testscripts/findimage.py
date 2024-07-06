import cv2
import numpy as np

# Load the images
image = cv2.imread("screenshot.png")
template = cv2.imread("greyCross.png")

# Get dimensions of the template
h, w = template.shape[:2]

# Perform template matching
result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Check if the maximum match value is above a certain threshold
if max_val > 0.7:
    # If a match is found, calculate the top-left and bottom-right corners of the bounding box
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Calculate the center of the rectangle
    center_x = top_left[0] + w // 2
    center_y = top_left[1] + h // 2

    # Draw the rectangle around the matched region
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # Save the result
    cv2.imwrite('result2.png', image)
    print(f"Match center found: X={center_x}, Y={center_y}")
else:
    print("No sufficient match found.")