import numpy as np
from PIL import Image
import io
from app.utils.custom_exception import AppException


class ImageProcessor:

    @staticmethod
    def preprocess_image(image_bytes, target_size=(224, 224)):
        """
        Preprocess uploaded image for plant disease model.

        Steps:
        1. Convert bytes to PIL Image
        2. Convert to RGB
        3. Resize to target size
        4. Normalize pixel values (1/255)
        5. Expand dimensions for model
        """

        try:
            # Convert bytes to PIL image
            image = Image.open(io.BytesIO(image_bytes))

            # Convert to RGB (important!)
            image = image.convert("RGB")

            # Resize
            image = image.resize(target_size)

            # Convert to numpy array
            image_array = np.array(image)

            # Normalize (same as training)
            image_array = image_array / 255.0

            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)

            return image_array

        except Exception as e:
            raise AppException(
                f"Error processing image: {str(e)}",
                400
            )