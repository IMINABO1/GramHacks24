import io, os
from numpy import random
from google.cloud import vision
from google.cloud.vision_v1 import types

from Pillow_util import draw_borders, Image
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"serviceAccountToken.json"
client = vision.ImageAnnotatorClient()

file_name = 'img/pic3.png'
# image_path = os.path.join('.\Images', file_name)
image_path = file_name

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)
response = client.object_localization(image=image)
localized_object_annotations = response.localized_object_annotations

pillow_image = Image.open(image_path)
df = pd.DataFrame(columns=['name', 'score'])
for obj in localized_object_annotations:
    df = df._append(
        dict(
            name=obj.name,
            score=obj.score
        ),
        ignore_index=True)
    
    r, g, b = random.randint(150, 255), random.randint(
        150, 255), random.randint(150, 255)

    draw_borders(pillow_image, obj.bounding_poly, (r, g, b),
                 pillow_image.size, obj.name, obj.score)

print(df)
pillow_image.show()