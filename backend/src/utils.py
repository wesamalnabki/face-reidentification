import base64
import os
from io import BytesIO

from PIL import Image


def numpy_to_base64(image_array, format="PNG"):
    """
    Convert a NumPy array (representing an image) to a base64-encoded string.

    Args:
        image_array (numpy.ndarray): The image as a NumPy array.
        format (str): The image format (e.g., "PNG", "JPEG"). Default is "PNG".

    Returns:
        str: The base64-encoded string representation of the image.
    """
    # Convert the NumPy array to a PIL Image
    image = Image.fromarray(image_array)

    # Create a BytesIO object to hold the image data
    img_byte_arr = BytesIO()

    # Save the PIL Image to the BytesIO object in the specified format
    image.save(img_byte_arr, format=format)

    # Encode the image bytes to a base64 string
    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

    return img_base64


def save_image(person_id, face_id, image_pil):
    folder_path = os.path.join(os.getenv("FACES_DB_PATH"), person_id)
    os.makedirs(folder_path, exist_ok=True)
    image_pil.save(os.path.join(folder_path, face_id + ".png"), "PNG")
