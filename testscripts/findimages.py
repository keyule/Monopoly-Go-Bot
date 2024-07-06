import cv2
import numpy as np

def find_top_templates(large_image_path, template_path, top_n=3, min_distance=10, threshold=0.8):
    # Load the larger image
    large_image = cv2.imread(large_image_path)

    # Load the smaller image (template)
    template = cv2.imread(template_path)

    # Get the dimensions of the template
    template_height, template_width, _ = template.shape

    # Use template matching to find the smaller image in the larger one
    result = cv2.matchTemplate(large_image, template, cv2.TM_CCOEFF_NORMED)

    # Get the locations and their corresponding similarity scores
    sorted_results = []

    while len(sorted_results) < top_n:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if the similarity score is above the threshold
        if max_val < threshold:
            break
        
        # Check if the new location is sufficiently far from existing locations
        is_far_enough = True
        for _, existing_loc in sorted_results:
            distance = np.sqrt((existing_loc[0] - max_loc[0]) ** 2 + (existing_loc[1] - max_loc[1]) ** 2)
            if distance < min_distance:
                is_far_enough = False
                break
        
        if is_far_enough:
            sorted_results.append((max_val, max_loc))
        
        # Set the found location to a low value to find the next highest match
        result[max_loc[1], max_loc[0]] = -1

        # Break if there are no more valid matches
        if max_val < 0:
            break

    # Calculate the middle coordinates for the top N found locations
    middle_coords = []
    for score, pt in sorted_results:
        middle_x = pt[0] + template_width / 2
        middle_y = pt[1] + template_height / 2
        middle_coords.append((middle_x, middle_y))

        # Draw rectangles around found templates
        bottom_right = (pt[0] + template_width, pt[1] + template_height)
        cv2.rectangle(large_image, pt, bottom_right, (0, 255, 0), 2)

    # Save the result
    cv2.imwrite('result.png', large_image)

    return middle_coords

# Example usage:
large_image_path = 'screenshot.png'
template_path = 'greyCross.png'
middle_coords = find_top_templates(large_image_path, template_path, top_n=10, threshold=0.8)
print(middle_coords)