import numpy as np
from PIL import Image
import io
import torch
from torchvision import transforms
from app.utils.custom_exception import AppException


class ImageProcessor:

    @staticmethod
    def preprocess_image(image_bytes, target_size=(224, 224)):
        """
        Preprocess uploaded image for plant disease model using PyTorch.

        Steps:
        1. Convert bytes to PIL Image
        2. Convert to RGB
        3. Apply PyTorch transforms (resize, normalize)
        4. Convert to tensor and add batch dimension
        """

        try:
            # Convert bytes to PIL image
            image = Image.open(io.BytesIO(image_bytes))

            # Convert to RGB (important!)
            image = image.convert("RGB")

            # Define PyTorch transforms (ImageNet normalization)
            transform = transforms.Compose([
                transforms.Resize(target_size),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])

            # Apply transforms
            image_tensor = transform(image)

            # Add batch dimension (batch_size=1)
            image_tensor = image_tensor.unsqueeze(0)

            return image_tensor

        except Exception as e:
            raise AppException(
                f"Error processing image: {str(e)}",
                400
            )
