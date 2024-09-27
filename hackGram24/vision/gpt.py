from google.cloud import vision
from PIL import Image, ImageDraw
import io, os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'serviceAccountToken.json'

# Function to detect objects in an image using Google Vision API
def detect_trash_and_draw_borders(image_path, output_image_path):
    # Initialize the Vision client
    client = vision.ImageAnnotatorClient()

    # Load the image
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
        image = vision.Image(content=content)

    # Perform object detection on the image
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    # Load the image using Pillow
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    print('Objects detected in the image:')
    for obj in objects:
        print(f'{obj.name} (confidence: {obj.score})')
        
        # Filter for trash-related objects (e.g., 'Trash', 'Garbage')
        if any(keyword in obj.name.lower() for keyword in ['trash', 'garbage', 'waste', 'litter']):
            print(f'Drawing border around: {obj.name}')
            
            # Extract the vertices for bounding box
            vertices = [(vertex.x * img.width, vertex.y * img.height) for vertex in obj.bounding_poly.normalized_vertices]
            
            # Draw rectangle (bounding box) around detected object
            draw.line([*vertices, vertices[0]], width=5, fill='red')

    # Save the output image with borders
    img.save(output_image_path)

    # Handle any errors in the response
    if response.error.message:
        raise Exception(f'{response.error.message}')


# Example usage of the function
if __name__ == "__main__":
    image_path = 'img/pic2.png'  # Replace with the path to your input image
    output_image_path = 'output_with_borders.png'  # Replace with the path to your output image
    detect_trash_and_draw_borders(image_path, output_image_path)
