import requests

# Test crop recommendation
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MkB0ZXN0LmNvbSIsIm5hbWUiOiJ0ZXN0IiwiZXhwIjoxNzczMjQ5OTU2fQ.bo_9lCqESNM0e2c1FLgDgp47UtrbSYcxG8ITd7TbR8o"
headers = {"Authorization": f"Bearer {token}"}
data = {
    "nitrogen": 90,
    "phosphorus": 42,
    "potassium": 43,
    "temperature": 20,
    "humidity": 80,
    "ph": 6.5,
    "rainfall": 200
}

print("Testing Crop Recommendation API...")
r = requests.post("http://localhost:8000/api/crop/recommend", json=data, headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")
