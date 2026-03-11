import sys
sys.path.insert(0, "Crop-ai-backend")

import torch
import numpy as np
from PIL import Image
import io

# Import the model loader
from app.utils.model_loader import get_disease_model
from app.config.class_names import CLASS_NAMES

print("Loading disease model...")
model = get_disease_model()
print(f"Model loaded successfully!")
print(f"Model type: {type(model)}")

# Create a test image (256x256 RGB)
img = Image.new('RGB', (256, 256), color='green')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes = img_bytes.getvalue()

# Preprocess
image = Image.open(io.BytesIO(img_bytes))
image = image.convert("RGB")
image = image.resize((256, 256))
image_array = np.array(image) / 255.0
image_array = np.expand_dims(image_array, axis=0)
image_tensor = torch.from_numpy(image_array).float()

# Make sure shape is (1, 3, 256, 256) - need to transpose
image_tensor = image_tensor.permute(0, 3, 1, 2)

print(f"Input shape: {image_tensor.shape}")

# Predict
model.eval()
with torch.no_grad():
    output = model(image_tensor)
    probabilities = torch.nn.functional.softmax(output, dim=1)
    pred = torch.argmax(probabilities, dim=1).item()
    confidence = probabilities[0][pred].item()

print(f"Predicted class index: {pred}")
print(f"Class name: {CLASS_NAMES[pred]}")
print(f"Confidence: {round(confidence * 100, 2)}%")
print("\n✅ Disease model is working correctly!")
