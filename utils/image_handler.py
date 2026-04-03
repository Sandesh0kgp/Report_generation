import base64
import io
from PIL import Image

def pil_image_to_base64(image: Image.Image, format: str = "JPEG") -> str:
    """Convert PIL Image to base64 string for LLM consumption."""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    # Get base64 representation
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def resize_image_for_llm(image: Image.Image, max_size: tuple = (1024, 1024)) -> Image.Image:
    """Resize image to avoid overloading the LLM payload limits."""
    img_copy = image.copy()
    img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img_copy

def process_and_encode_image(image: Image.Image, max_size: tuple = (1024, 1024)) -> str:
    """Resize and encode a single PIL image to base64."""
    resized_img = resize_image_for_llm(image, max_size)
    return pil_image_to_base64(resized_img)
