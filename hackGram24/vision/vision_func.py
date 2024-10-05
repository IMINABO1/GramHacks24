import io
import os
from numpy import random
from google.cloud import vision
from google.cloud.vision_v1 import types
from Pillow_util import draw_borders, Image

# Set up Google Vision API credentials
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r""
client = vision.ImageAnnotatorClient()

# Function to process image and return the annotated image and detected objects as a set
def detect_objects(image_path):
    # Open the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create a Vision API Image object
    image = types.Image(content=content)

    # Perform object localization (detection)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations

    # Open the image with Pillow
    pillow_image = Image.open(image_path)

    # Create a set to store detected object names
    detected_objects_set = set()

    # Iterate over the detected objects and draw borders
    for obj in localized_object_annotations:
        # Add object name to the set (unique values only)
        detected_objects_set.add(obj.name)

        # Generate random color for the border
        r, g, b = random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)

        # Draw the bounding box on the image
        draw_borders(pillow_image, obj.bounding_poly, (r, g, b),
                     pillow_image.size, obj.name, obj.score)

    # Return the modified image and the set of detected objects
    return pillow_image, detected_objects_set


'''
# Example usage
if __name__ == "__main__":
    # Specify the path to the image file
    image_path = 'img/pic4.png'
    
    # Call the function and get the results
    annotated_image, detected_objects = detect_objects(image_path)
    
    # Display the set of detected objects
    print("Detected Objects:", detected_objects)
    # print(type(detected_objects))
    # Optionally save the image or use it further
    annotated_image.save('output_image_with_borders.png')
'''