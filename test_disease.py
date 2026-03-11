import requests
import base64

# Test disease prediction - we'll send a simple test image
# First let's create a small test image
from PIL import Image
import io

# Create a simple test image
img = Image.new('RGB', (224, 224), color='green')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes = img_bytes.getvalue()

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MkB0ZXN0LmNvbSIsIm5hbWUiOiJ0ZXN0IiwiZXhwIjoxNzczMjQ5OTU2fQ.bo_9lCqESNM0e2c1FLgDgp47UtrbSYcxG8ITd7TbR8o"
headers = {"Authorization": f"Bearer {token}"}

print("Testing Disease Prediction API...")
files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
r = requests.post("http://localhost:8000/api/disease/predict", files=files, headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")
