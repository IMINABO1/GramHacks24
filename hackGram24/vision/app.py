from flask import Flask, request, jsonify, render_template
import base64
import io
from PIL import Image
import tempfile
import os

# Import functions from other scripts
from vision_func import detect_objects
from guideline import get_recycling_info

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home_index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        # Save the file temporarily
        temp_filename = tempfile.mktemp(suffix='.png')
        file.save(temp_filename)
        
        try:
            # Process the image using the vision function
            annotated_image, detected_objects = detect_objects(temp_filename)
            
            # Save the annotated image
            annotated_filename = 'upload/annotated_image.png'
            annotated_image.save(annotated_filename)
            
            # Get recycling info for each detected object
            recycling_info = {}
            for obj in detected_objects:
                recycling_info[obj] = get_recycling_info(obj, "sunny")  # Assuming sunny weather
            
            print(f" The recycling info is {recycling_info}")
            return jsonify({
                'detected_objects': list(detected_objects)[:3],
                'recycling_info': recycling_info,
                'annotated_image': '/upload/annotated_image.png'
            })
        
        finally:
            # Clean up the temporary file
            os.unlink(temp_filename)

if __name__ == '__main__':
    app.run(debug=True)