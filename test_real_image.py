import requests
import io
from PIL import Image

# Create a real test image
img = Image.new('RGB', (256, 256), color='green')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes = img_bytes.getvalue()

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MkB0ZXN0LmNvbSIsIm5hbWUiOiJ0ZXN0IiwiZXhwIjoxNzczMjQ5OTU2fQ.bo_9lCqESNM0e2c1FLgDgp47UtrbSYcxG8ITd7TbR8o"

print("Testing Disease Prediction with real image...")
files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
r = requests.post("http://localhost:8000/api/disease/predict", files=files, headers={"Authorization": f"Bearer {token}"})
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")
