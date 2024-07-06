import pyscreeze
import PIL

# Load the images directly using pyscreeze
screenshot = PIL.Image.open("screenshot.png")
template = PIL.Image.open("test.png")

# Convert images to the correct format
#screenshot = pyscreeze._load_cv2(screenshot, grayscale=False)
#template = pyscreeze._load_cv2(template, grayscale=False)

# Perform template matching using pyscreeze's internal method
matched_box = pyscreeze.locate(template, screenshot, confidence=0.5)

if matched_box:
    # Print the coordinates of the top-left corner of the matched area
    print("X coordinate:", matched_box.left)
    print("Y coordinate:", matched_box.top)
else:
    print("Template not found in the image.")



locations = pyscreeze.locateAll(screenshot, template)
for location in locations:
    # calculate absolute screen x/y from the game's x/y
    x = location[0]
    y = location[1]
    print(x, y)