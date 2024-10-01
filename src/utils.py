from PIL import Image

def resize_image(img, max_width, max_height):
    """
    Resize an image to fit within the specified dimensions while maintaining aspect ratio.
    """
    ratio = min(max_width / img.width, max_height / img.height)
    new_size = (int(img.width * ratio), int(img.height * ratio))
    return img.resize(new_size, Image.LANCZOS)
