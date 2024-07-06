import cv2

def find_template(large_image_path, template_path):
    # Load the larger image
    large_image = cv2.imread(large_image_path)

    # Load the smaller image (template)
    template = cv2.imread(template_path)

    # Get the dimensions of the template
    template_height, template_width, _ = template.shape

    # Use template matching to find the smaller image in the larger one
    result = cv2.matchTemplate(large_image, template, cv2.TM_CCOEFF_NORMED)

    # Find the location of the template in the larger image
    

    # Calculate the middle coordinates
    middle_x = location[0] + template_width / 2
    middle_y = location[1] + template_height / 2

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    h, w = template.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(large_image, top_left, bottom_right, (0, 255, 0), 2)

    # Save the result
    cv2.imwrite('result.png', large_image)

    return (middle_x, middle_y)

# Example usage:
large_image_path = 'screen.png'
template_path = 'go.png'
middle_coords = find_template(large_image_path, template_path)
print(middle_coords)


