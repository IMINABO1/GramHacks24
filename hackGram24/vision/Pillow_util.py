from PIL import ImageDraw, Image, ImageFont


# def draw_borders(image, bounding_poly, color, image_size, name, score):
#     draw = ImageDraw.Draw(image)
#     vertices = [(vertex.x, vertex.y) for vertex in bounding_poly.vertices]
#     draw.polygon(vertices, outline=color)
#     draw.text((vertices[0]), f'{name} ({score:.2f})', fill=color)
#     return image

def draw_borders(pillow_image, bounding, color, image_size, caption='', confidence_score=0):

    width, height = image_size
    draw = ImageDraw.Draw(pillow_image)

    draw.polygon([
        bounding.normalized_vertices[0].x * width, bounding.normalized_vertices[0].y * height,
        bounding.normalized_vertices[1].x * width, bounding.normalized_vertices[1].y * height,
        bounding.normalized_vertices[2].x * width, bounding.normalized_vertices[2].y * height,
        bounding.normalized_vertices[3].x * width, bounding.normalized_vertices[3].y * height
    ],fill=None, outline=color)

    font_size=width * height //2200 if width * height > 400000 else 12
    font = ImageFont.truetype(r"font/AndersonGrotesk.otf", font_size)
    draw.text((bounding.normalized_vertices[0].x * width, bounding.normalized_vertices[0].y * height), font=font, text=caption, fill=color)

    #insert confidence score
    draw.text((bounding.normalized_vertices[0].x * width, bounding.normalized_vertices[0].y * height +20), font=font, text="Confidence score {:.2f}%".format(confidence_score), fill=color)

    return pillow_image

