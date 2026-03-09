# 🌱 CropAI – Smart Agriculture Platform

AI-powered platform for **Crop Recommendation, Plant Disease Detection, and AI Chatbot assistance** for farmers.

CropAI uses **Machine Learning and Deep Learning models** to help farmers make better decisions by analyzing soil conditions and plant images.

---

## 🚀 Features

### 🌾 Crop Recommendation
Recommends the best crop based on:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

Uses a trained **Machine Learning classification model**.

---

### 🍃 Plant Disease Detection

Upload a leaf image and the system will:

- Detect plant disease
- Provide prediction confidence
- Store prediction history in database

Powered by a **Deep Learning CNN model (ResNet based)**.

---

### 🤖 AI Chatbot for Farmers

An AI assistant that helps farmers with:

- Crop guidance
- Disease suggestions
- Farming tips
- General agriculture questions

Uses an **LLM-based chatbot integration**.

---

## 🏗 Project Architecture


Frontend (React / HTML)
|
v
FastAPI Backend (CropAI API)
|
|---- Crop Recommendation Service
|---- Disease Detection Service
|---- Chatbot Service
|
v
Machine Learning Models
|
v
MongoDB Database


---

## 📂 Project Structure


Crop Disease Detection
│
├── Crop-ai-backend
│ ├── app
│ │ ├── config
│ │ ├── database
│ │ ├── models
│ │ ├── routes
│ │ ├── services
│ │ └── utils
│ │
│ ├── run.py
│ └── requirements.txt
│
├── models
│ └── disease_model.pth
│
├── notebooks
│ └── training.ipynb
│
├── Data-processed
├── Data-raw
│
└── README.md

frontend
│
├── index.html
├── login.html
├── register.html
├── dashboard.html
├── crop.html
├── disease.html
├── chatbot.html
├── history.html
│
├── css
│   ├── style.css
│   ├── dashboard.css
│
├── js
│   ├── config.js
│   ├── auth.js
│   ├── crop.js
│   ├── disease.js
│   ├── chatbot.js
│   ├── history.js
│
└── assets
    ├── logo.png
    ├── hero-bg.jpg
    ├── crop-icon.png
    ├── disease-icon.png
    ├── chatbot-icon.png
    ├── upload-icon.png
    ├── leaf-icon.png
    ├── farmer-icon.png
    └── favicon.png

---

## ⚙️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### Machine Learning
- TensorFlow / Keras
- PyTorch
- NumPy

### Database
- MongoDB
- PyMongo

### Tools
- Git
- GitHub
- Kaggle (Model Training)

---

## 🧠 AI Models Used

### Crop Recommendation Model
- Input: Soil nutrients & environmental conditions
- Output: Recommended crop
- Model Type: **Machine Learning Classifier**

---

### Disease Detection Model
- Architecture: **ResNet based CNN**
- Input: Plant leaf image
- Output:
  - Disease name
  - Prediction confidence

---

## 🔧 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/crop-ai.git
cd crop-ai
2️⃣ Create virtual environment
python -m venv venv

Activate environment:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Setup environment variables

Create .env file:

MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=crop_ai
5️⃣ Run the server
python run.py

Server will start at:

http://127.0.0.1:8000
📡 API Endpoints
Crop Recommendation
POST /crop/recommend

Example Input

{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.5,
  "humidity": 80,
  "ph": 6.5,
  "rainfall": 200
}
Disease Detection
POST /disease/predict

Upload plant leaf image.

Returns:

{
  "predicted_label": "Tomato Late Blight",
  "confidence": 98.6
}
Chatbot
POST /chatbot/message

Example:

{
 "message": "What crop grows best in rainy season?"
}
📊 Dataset

Training dataset used from:

Kaggle Plant Disease Dataset

Crop Recommendation Dataset

Images were preprocessed and used to train a CNN model.

🔐 Environment Variables
MONGO_URI
DATABASE_NAME
MODEL_PATH
🧪 Future Improvements

Mobile application for farmers

Real-time weather integration

Multi-language chatbot

Fertilizer recommendation

Field disease detection using camera

👨‍💻 Author

Yug Sondagar

BTech Computer Science Engineering
AI & Machine Learning Enthusiast

⭐ Contribute

Pull requests are welcome.

For major changes please open an issue first to discuss what you would like to change.

📜 License

This project is licensed under the MIT License.


---

# ⭐ This README is already **industry level**, but we can make it **even better** by adding:

- Project **architecture diagram**
- **API documentation**
- **Demo screenshots**
- **badges**
- **model performance**

These make your GitHub look **very professional**.

If you want, I can also show you how to create a **🔥 top-tier README like big AI projects (with b# 🌱 CropAI – Smart Agriculture Platform

AI-powered platform for **Crop Recommendation, Plant Disease Detection, and AI Chatbot assistance** for farmers.

CropAI uses **Machine Learning and Deep Learning models** to help farmers make better decisions by analyzing soil conditions and plant images.

---

## 🚀 Features

### 🌾 Crop Recommendation
Recommends the best crop based on:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

Uses a trained **Machine Learning classification model**.

---

### 🍃 Plant Disease Detection

Upload a leaf image and the system will:

- Detect plant disease
- Provide prediction confidence
- Store prediction history in database

Powered by a **Deep Learning CNN model (ResNet based)**.

---

### 🤖 AI Chatbot for Farmers

An AI assistant that helps farmers with:

- Crop guidance
- Disease suggestions
- Farming tips
- General agriculture questions

Uses an **LLM-based chatbot integration**.

---

## 🏗 Project Architecture


Frontend (React / HTML)
|
v
FastAPI Backend (CropAI API)
|
|---- Crop Recommendation Service
|---- Disease Detection Service
|---- Chatbot Service
|
v
Machine Learning Models
|
v
MongoDB Database


---

## 📂 Project Structure


Crop Disease Detection
│
├── Crop-ai-backend
│ ├── app
│ │ ├── config
│ │ ├── database
│ │ ├── models
│ │ ├── routes
│ │ ├── services
│ │ └── utils
│ │
│ ├── run.py
│ └── requirements.txt
│
├── models
│ └── disease_model.pth
│
├── notebooks
│ └── training.ipynb
│
├── Data-processed
├── Data-raw
│
└── README.md


---

## ⚙️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### Machine Learning
- TensorFlow / Keras
- PyTorch
- NumPy

### Database
- MongoDB
- PyMongo

### Tools
- Git
- GitHub
- Kaggle (Model Training)

---

## 🧠 AI Models Used

### Crop Recommendation Model
- Input: Soil nutrients & environmental conditions
- Output: Recommended crop
- Model Type: **Machine Learning Classifier**

---

### Disease Detection Model
- Architecture: **ResNet based CNN**
- Input: Plant leaf image
- Output:
  - Disease name
  - Prediction confidence

---

## 🔧 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/crop-ai.git
cd crop-ai
2️⃣ Create virtual environment
python -m venv venv

Activate environment:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Setup environment variables

Create .env file:

MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=crop_ai
5️⃣ Run the server
python run.py

Server will start at:

http://127.0.0.1:8000
📡 API Endpoints
Crop Recommendation
POST /crop/recommend

Example Input

{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.5,
  "humidity": 80,
  "ph": 6.5,
  "rainfall": 200
}
Disease Detection
POST /disease/predict

Upload plant leaf image.

Returns:

{
  "predicted_label": "Tomato Late Blight",
  "confidence": 98.6
}
Chatbot
POST /chatbot/message

Example:

{
 "message": "What crop grows best in rainy season?"
}
📊 Dataset

Training dataset used from:

Kaggle Plant Disease Dataset

Crop Recommendation Dataset

Images were preprocessed and used to train a CNN model.

🔐 Environment Variables
MONGO_URI
DATABASE_NAME
MODEL_PATH
🧪 Future Improvements

Mobile application for farmers

Real-time weather integration

Multi-language chatbot

Fertilizer recommendation

Field disease detection using camera

👨‍💻 Author

Yug Sondagar

BTech Computer Science Engineering
AI & Machine Learning Enthusiast

⭐ Contribute

Pull requests are welcome.

For major changes please open an issue first to discuss what you would like to change.

📜 License

This project is licensed under the MIT License.


---

# ⭐ This README is already **industry level**, but we can make it **even better** by adding:

- Project **architecture diagram**
- **API documentation**
- **Demo screenshots**
- **badges**
- **model performance**

These make your GitHub look **very professional**.

If you want, I can also show you how to create a **🔥 top-tier README like big AI projects (with badges, diagrams, screenshots)** that will make recruiters notice your project instantly.